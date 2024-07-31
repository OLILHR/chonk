import logging
import os

import click
from collector import consolidate
from filter import parse_extensions

GLOBAL_LOG_LEVEL = logging.INFO
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

_logger = logging.getLogger(__name__)
_logger.setLevel(GLOBAL_LOG_LEVEL)


@click.command()
@click.argument("path", type=click.Path(exists=True))
@click.option(
    "--filter",
    "-f",
    "extensions",
    callback=parse_extensions,
    multiple=True,
    help="Filter files by extension, e.g. -f py,json,yml",
)
def generate_markdown(path, extensions):
    extensions = list(extensions) if extensions else None
    markdown_content = consolidate(path, extensions)
    project_root = os.path.dirname(os.path.abspath(__file__))
    output_file = os.path.join(project_root, "../codebase.md")

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(markdown_content)

    _logger.info("Markdown file generated at %s", output_file)


if __name__ == "__main__":
    generate_markdown()  # pylint: disable=no-value-for-parameter

# to do:
# if extension is in .alloyignore, generate the markdown file anyway
# if no extension is given, just ignore the files in .alloyignore and consolidate the rest
