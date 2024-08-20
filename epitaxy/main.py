import logging
import os
from dataclasses import dataclass
from typing import Any, Iterable, List, Optional

import click
from prompt_toolkit import prompt
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.document import Document

from .filter import parse_extensions
from .utilities import NoMatchingExtensionError, consolidate

GLOBAL_LOG_LEVEL = logging.INFO
logging.basicConfig(level=logging.INFO, format="%(message)s")

_logger = logging.getLogger(__name__)
_logger.setLevel(GLOBAL_LOG_LEVEL)

MAX_FILE_SIZE: int = 1024 * 1024 * 10  # 10 MB


def get_project_root() -> str:
    current_dir: str = os.path.abspath(os.getcwd())

    root_indicators: List[str] = [
        ".git",
        "package.json",
        "pdm.lock",
        "pyproject.toml",
        "setup.py",
        "tox.ini",
    ]

    while current_dir != os.path.dirname(current_dir):
        if any(os.path.exists(os.path.join(current_dir, indicator)) for indicator in root_indicators):
            return current_dir
        current_dir = os.path.dirname(current_dir)

    return os.getcwd()


@dataclass
class CaseInsensitivePathCompleter(Completer):
    only_directories: bool = False

    def get_completions(self, document: Document, complete_event: Any) -> Iterable[Completion]:
        text: str = os.path.expanduser(document.text_before_cursor)
        if not text:
            return

        directory: str = os.path.dirname(text)
        prefix: str = os.path.basename(text)

        full_directory: str = os.path.abspath(directory)

        try:
            suggestions: List[str] = os.listdir(full_directory)
        except OSError:
            return

        for suggestion in suggestions:
            if suggestion.lower().startswith(prefix.lower()):
                if self.only_directories and not os.path.isdir(os.path.join(full_directory, suggestion)):
                    continue
                yield Completion(suggestion[len(prefix) :], start_position=0, display=suggestion)


def path_prompt(message: str, default: str, exists: bool = False) -> str:
    """
    Required by prompt_toolkit to enable basic shell features for CLI prompts, like path suggestion and autocompletion.
    """
    path_completer = CaseInsensitivePathCompleter()

    if not default.endswith(os.path.sep):
        default += os.path.sep

    while True:
        path: str = prompt(f"{message} ", default=default, completer=path_completer)
        full_path: str = os.path.abspath(os.path.expanduser(path))
        if not exists or os.path.exists(full_path):
            return full_path
        logging.error("🔴 %s DOES NOT EXIST.", full_path)


@click.command()
@click.option("-i", "--input-path", type=click.Path(exists=True), help="input path for the files to be consolidated")
@click.option("-o", "--output-path", type=click.Path(), help="output path for the generated markdown file")
@click.option(
    "--filter",
    "-f",
    "extension_filter",
    callback=parse_extensions,
    multiple=True,
    help="enables optional filtering by extensions, for instance: -f py,json",
)
# pylint: disable=too-many-locals
def generate_markdown(
    input_path: Optional[str], output_path: Optional[str], extension_filter: Optional[List[str]]
) -> None:
    no_flags_provided: bool = input_path is None and output_path is None and not extension_filter
    project_root: str = get_project_root()

    input_path = input_path or path_prompt(
        "📁 INPUT PATH OF YOUR TARGET DIRECTORY -", default=project_root, exists=True
    )
    output_path = output_path or path_prompt("📁 OUTPUT PATH FOR THE MARKDOWN FILE -", default=project_root)

    extensions: Optional[List[str]] = extension_filter
    if no_flags_provided:
        extensions_input: str = click.prompt(
            "🔎 OPTIONAL FILTER FOR SPECIFIC EXTENSIONS (COMMA-SEPARATED)",
            default="",
            show_default=False,
        )
        if extensions_input:
            extensions = parse_extensions(None, None, [extensions_input])

    extensions = list(extensions) if extensions else None

    try:
        markdown_content, file_count, token_count, lines_of_code_count, type_distribution = consolidate(
            input_path, extensions
        )
    except NoMatchingExtensionError:
        _logger.error("\n⚠️ NO FILES MATCH THE SPECIFIED EXTENSION(S) - PLEASE REVIEW YOUR .epitaxyignore FILE.")
        _logger.error("🔴 NO MARKDOWN FILE GENERATED.\n")
        return

    if len(markdown_content.encode("utf-8")) > MAX_FILE_SIZE:
        _logger.error("\n" + "🔴 GENERATED CONTENT EXCEEDS 10 MB. CONSIDER ADDING LARGER FILES TO YOUR .epitaxyignore.")
        return

    epitaxy: str = os.path.join(output_path, "epitaxy.md")

    os.makedirs(output_path, exist_ok=True)
    with open(epitaxy, "w", encoding="utf-8") as f:
        f.write(markdown_content)

    epitaxy_size: int = os.path.getsize(epitaxy)
    if epitaxy_size < 1024:
        file_size: str = f"{epitaxy_size} bytes"
    elif epitaxy_size < 1024 * 1024:
        file_size = f"{epitaxy_size / 1024:.2f} KB"
    else:
        file_size = f"{epitaxy_size / (1024 * 1024):.2f} MB"

    file_type_distribution: str = " ".join(
        f".{file_type} ({percentage:.0f}%)" for file_type, percentage in type_distribution
    )

    _logger.info(
        "\n"
        + "🟢 CODEBASE CONSOLIDATED SUCCESSFULLY.\n"
        + "\n"
        + "📁 MARKDOWN FILE LOCATION: %s"
        + "\n"
        + "💾 MARKDOWN FILE SIZE: %s"
        + "\n"
        + "📄 FILES PROCESSED: %d"
        + "\n"
        + "📊 TYPE DISTRIBUTION: %s"
        + "\n"
        + "📈 LINES OF CODE: %d"
        + "\n"
        + "🪙 TOKEN COUNT: %d"
        + "\n",
        epitaxy,
        file_size,
        file_count,
        file_type_distribution,
        lines_of_code_count,
        token_count,
    )


# to run the script during local development, either execute $ python -m epitaxy
# or install epitaxy locally via `pdm install` and simply run $ epitaxy
if __name__ == "__main__":
    generate_markdown.main(standalone_mode=False)
