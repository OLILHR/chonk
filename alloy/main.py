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
@click.argument("input_path", type=click.Path(exists=True), required=False)
@click.option(
    "--filter",
    "-f",
    "extensions",
    callback=parse_extensions,
    multiple=True,
    help="OPTIONAL FILTERING BY EXTENSIONS; FOR INSTANCE: -f py,json,yml",  # consolidates only py, json and yml files
)
def generate_markdown(input_path, extensions):
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    current_dir = os.getcwd()

    if input_path is None:
        input_path = click.prompt("INPUT PATH:", type=click.Path(exists=True), default=current_dir)
        output_path = click.prompt("OUTPUT PATH:", type=click.Path(exists=True), default=project_root)
        extensions_input = click.prompt("FILTER FOR EXTENSIONS:", default="")
        extensions = parse_extensions(None, None, [extensions_input]) if extensions_input else None
    else:
        output_path = project_root
        extensions = list(extensions) if extensions else None

    input_path = os.path.abspath(os.path.join(current_dir, input_path))

    markdown_content = consolidate(input_path, extensions)
    output_file = os.path.join(output_path, "codebase.md")

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(markdown_content)

    _logger.info("CODEBASE CONSOLIDATED AT %s", output_file)


if __name__ == "__main__":
    generate_markdown()
