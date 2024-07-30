import logging
import os

import click

from alloy.collector import consolidate

GLOBAL_LOG_LEVEL = logging.INFO
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

_logger = logging.getLogger(__name__)
_logger.setLevel(GLOBAL_LOG_LEVEL)


@click.command()
@click.argument("path", type=click.Path(exists=True))
def main(path):
    """
    Generates a consolidated markdown file.
    """
    markdown_content = consolidate(path)
    project_root = os.path.dirname(os.path.abspath(__file__))
    output_file = os.path.join(project_root, "../codebase.md")

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(markdown_content)

    _logger.info("Markdown file generated at %s", output_file)


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
