import logging
import os

import click

from .collector import consolidate
from .filter import parse_extensions

GLOBAL_LOG_LEVEL = logging.INFO
logging.basicConfig(level=logging.INFO, format="%(message)s")

_logger = logging.getLogger(__name__)
_logger.setLevel(GLOBAL_LOG_LEVEL)

MAX_FILE_SIZE = 1024 * 1024 * 10  # 10 MB


@click.command()
@click.option("-i", "--input-path", type=click.Path(exists=True), help="input path for the files to be consolidated")
@click.option("-o", "--output-path", type=click.Path(), help="output path for the generated markdown file")
@click.option(
    "--filter",
    "-f",
    "extension_filter",
    callback=parse_extensions,
    multiple=True,
    help="enables optional filtering by extensions, for instance: -f py,json",  # consolidates only .py and .json files
)
def generate_markdown(input_path, output_path, extension_filter):
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    current_dir = os.getcwd()

    if input_path is None:
        input_path = click.prompt(
            "📁 INPUT PATH OF YOUR TARGET DIRECTORY -", type=click.Path(exists=True), default=current_dir
        )
    else:
        input_path = os.path.abspath(os.path.join(current_dir, input_path))

    if output_path is None:
        output_path = click.prompt(
            "📁 OUTPUT PATH FOR THE MARKDOWN FILE -", type=click.Path(), default=project_root
        )
    else:
        output_path = os.path.abspath(os.path.join(current_dir, output_path))

    extensions = extension_filter
    if not extensions:
        extensions_input = click.prompt(
            "🔎 (OPTIONAL) FILTER ONLY FOR SPECIFIC EXTENSIONS (COMMA-SEPARATED)",
            default="",
            show_default=False,
        )
        if extensions_input:
            extensions = parse_extensions(None, None, [extensions_input])

    extensions = list(extensions) if extensions else None

    markdown_content = consolidate(input_path, extensions)

    if len(markdown_content.encode("utf-8")) > MAX_FILE_SIZE:
        _logger.error("\n" + "🔴 GENERATED CONTENT EXCEEDS 10 MB. CONSIDER ADDING LARGER FILES TO YOUR .alloyignore.")
        return

    output_file = os.path.join(output_path, "alloy.md")

    os.makedirs(output_path, exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(markdown_content)

    _logger.info("\n" + "🟢 CODEBASE CONSOLIDATED SUCCESSFULLY\n" + "📁 MARKDOWN FILE LOCATION: %s" + "\n", output_file)


# execute via "python -m alloy"
if __name__ == "__main__":
    generate_markdown.main()
