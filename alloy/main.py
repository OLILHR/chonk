import logging
import os

import click

from alloy.collector import consolidate
from alloy.filter import parse_extensions

GLOBAL_LOG_LEVEL = logging.INFO
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

_logger = logging.getLogger(__name__)
_logger.setLevel(GLOBAL_LOG_LEVEL)


@click.command()
@click.option("-i", "--input-path", type=click.Path(exists=True), help="Input path for the codebase")
@click.option("-o", "--output-path", type=click.Path(), help="Output path for the generated markdown")
@click.option(
    "--filter",
    "-f",
    "extensions",
    callback=parse_extensions,
    multiple=True,
    help="OPTIONAL FILTERING BY EXTENSIONS; FOR INSTANCE: -f py,json",  # consolidates only .py and .json files
)
def generate_markdown(input_path, output_path, extensions):
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    current_dir = os.getcwd()

    if input_path is None:
        input_path = click.prompt("INPUT PATH:", type=click.Path(exists=True), default=current_dir)
    else:
        input_path = os.path.abspath(os.path.join(current_dir, input_path))

    if output_path is None:
        output_path = click.prompt("OUTPUT PATH:", type=click.Path(), default=project_root)
    else:
        output_path = os.path.abspath(os.path.join(current_dir, output_path))

    extensions = list(extensions) if extensions else None

    markdown_content = consolidate(input_path, extensions)
    output_file = os.path.join(output_path, "codebase.md")

    os.makedirs(output_path, exist_ok=True)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(markdown_content)

    _logger.info("CODEBASE CONSOLIDATED AT %s", output_file)


if __name__ == "__main__":
    generate_markdown.main()
