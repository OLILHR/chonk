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


def path_prompt(message, default, exists=False):
    """
    Provides basic shell features, like autocompletion, during prompts.
    """

    completer = PathCompleter(only_directories=False, expanduser=True)

    if not default.endswith(os.path.sep):
        default += os.path.sep

    while True:
        path = prompt(f"{message} ", default=default, completer=completer)
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
def generate_markdown(input_path, output_path, extension_filter):
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    current_dir = os.getcwd()

    if input_path is None:
        input_path = path_prompt("📁 INPUT PATH OF YOUR TARGET DIRECTORY -", default=current_dir, exists=True)
    else:
        input_path = os.path.abspath(os.path.join(current_dir, input_path))

    if output_path is None:
        output_path = path_prompt("📁 OUTPUT PATH FOR THE MARKDOWN FILE -", default=project_root)
    else:
        output_path = os.path.abspath(os.path.join(current_dir, output_path))

    extensions = extension_filter
    if not extensions and input_path is None and output_path is None:
        extensions_input = click.prompt(
            "🔎 (OPTIONAL) FILTER FOR SPECIFIC EXTENSIONS (COMMA-SEPARATED)",
            default="",
            show_default=False,
        )
        if extensions_input:
            extensions = parse_extensions(None, None, [extensions_input])

    extensions = list(extensions) if extensions else None
    markdown_content, file_count = consolidate(input_path, extensions)

    if len(markdown_content.encode("utf-8")) > MAX_FILE_SIZE:
        _logger.error("\n" + "🔴 GENERATED CONTENT EXCEEDS 10 MB. CONSIDER ADDING LARGER FILES TO YOUR .alloyignore.")
        return

    output_file = os.path.join(output_path, "alloy.md")

    os.makedirs(output_path, exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(markdown_content)

    output_file_size = os.path.getsize(output_file)
    if output_file_size < 1024:
        file_size = f"{output_file_size} bytes"
    elif output_file_size < 1024 * 1024:
        file_size = f"{output_file_size / 1024:.2f} KB"
    else:
        file_size = f"{output_file_size / (1024 * 1024):.2f} MB"

    _logger.info(
        "\n"
        + "🟢 CODEBASE CONSOLIDATED SUCCESSFULLY \n"
        + "\n"
        + "📁 MARKDOWN FILE LOCATION: %s"
        + "\n"
        + "💾 MARKDOWN FILE SIZE: %s"
        + "\n"
        + "📄 FILES PROCESSED: %d"
        + "\n"
        + "\n",
        output_file,
        file_size,
        file_count,
    )


if __name__ == "__main__":
    generate_markdown.main()
