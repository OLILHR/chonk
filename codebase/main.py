import logging
import os

import click
from prompt_toolkit import prompt
from prompt_toolkit.completion import PathCompleter

from .collector import consolidate
from .filter import parse_extensions

GLOBAL_LOG_LEVEL = logging.INFO
logging.basicConfig(level=logging.INFO, format="%(message)s")

_logger = logging.getLogger(__name__)
_logger.setLevel(GLOBAL_LOG_LEVEL)

MAX_FILE_SIZE = 1024 * 1024 * 10  # 10 MB


def get_project_root():
    """
    Required for input/output path prompts to display the project root as default path.
    """

    current_dir = os.path.abspath(os.getcwd())

    root_indicators = [
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


def path_prompt(message, default, exists=False):
    """
    Enables basic shell features, like autocompletion, for CLI prompts.
    """
    path_completer = PathCompleter(only_directories=False, expanduser=True)

    if not default.endswith(os.path.sep):
        default += os.path.sep

    while True:
        path = prompt(f"{message} ", default=default, completer=path_completer)
        path = os.path.abspath(os.path.expanduser(path))
        if not exists or os.path.exists(path):
            return path
        print(f"🔴 {path} DOES NOT EXIST.")


@click.command()
@click.option("-i", "--input-path", type=click.Path(exists=True), help="input path for the files to be consolidated")
@click.option("-o", "--output-path", type=click.Path(), help="output path for the generated markdown file")
@click.option(
    "--filter",
    "-f",
    "extension_filter",
    callback=parse_extensions,
    multiple=True,
    help="enables optional filtering by extensions, for instance: -f py,json",  # markdown contains only .py/.json files
)
# pylint: disable=too-many-locals
def generate_markdown(input_path, output_path, extension_filter):
    no_flags_provided = input_path is None and output_path is None and not extension_filter
    project_root = get_project_root()

    if input_path is None:
        input_path = path_prompt("📁 INPUT PATH OF YOUR TARGET DIRECTORY -", default=project_root, exists=True)
    else:
        input_path = os.path.abspath(input_path)

    if output_path is None:
        output_path = path_prompt("📁 OUTPUT PATH FOR THE MARKDOWN FILE -", default=project_root)
    else:
        output_path = os.path.abspath(output_path)

    extensions = extension_filter
    if no_flags_provided:
        extensions_input = click.prompt(
            "🔎 (OPTIONAL) FILTER FOR SPECIFIC EXTENSIONS (COMMA-SEPARATED)",
            default="",
            show_default=False,
        )
        if extensions_input:
            extensions = parse_extensions(None, None, [extensions_input])

    extensions = list(extensions) if extensions else None
    markdown_content, file_count, token_count, lines_of_code_count, type_distribution = consolidate(
        input_path, extensions
    )

    if len(markdown_content.encode("utf-8")) > MAX_FILE_SIZE:
        _logger.error(
            "\n" + "🔴 GENERATED CONTENT EXCEEDS 10 MB. CONSIDER ADDING LARGER FILES TO YOUR .codebaseignore."
        )
        return

    codebase = os.path.join(output_path, "codebase.md")

    os.makedirs(output_path, exist_ok=True)
    with open(codebase, "w", encoding="utf-8") as f:
        f.write(markdown_content)

    codebase_size = os.path.getsize(codebase)
    if codebase_size < 1024:
        file_size = f"{codebase_size} bytes"
    elif codebase_size < 1024 * 1024:
        file_size = f"{codebase_size / 1024:.2f} KB"
    else:
        file_size = f"{codebase_size / (1024 * 1024):.2f} MB"

    file_type_distribution = " ".join(
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
        codebase,
        file_size,
        file_count,
        file_type_distribution,
        lines_of_code_count,
        token_count,
    )


# to run the script during local development, either execute $ python -m codebase
# or install codebase locally via `pdm install` and simply run $ codebase
if __name__ == "__main__":
    generate_markdown.main(standalone_mode=False)
