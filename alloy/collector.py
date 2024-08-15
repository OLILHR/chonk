import logging
import os
import re

from .filter import filter_extensions, read_alloyignore

_logger = logging.getLogger(__name__)


def remove_trailing_whitespace(content):
    content = re.sub(r"\n{3,}", "\n\n", content)
    content = re.sub(r" +$", "", content, flags=re.MULTILINE)
    return content


def escape_markdown_characters(file_name):
    special_chars = r"([*_`\[\]()~>#+=|{}.!-])"
    return re.sub(special_chars, r"\\\1", file_name)


# pylint: disable=too-many-locals
def consolidate(path, extensions=None):
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    exclude_files = read_alloyignore(project_root, extensions)
    codebase = ""

    for root, dirs, files in os.walk(path):
        dirs[:] = [d for d in dirs if not exclude_files(os.path.relpath(str(os.path.join(root, d)), path))]

        for file in files:
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(str(file_path), path)

            if (extensions and not filter_extensions(file_path, extensions)) or exclude_files(relative_path):
                continue
            _, file_extension = os.path.splitext(file)

            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
            except UnicodeDecodeError:
                try:
                    with open(file_path, "r", encoding="iso-8859-1") as f:
                        content = f.read()
                except (OSError, IOError) as e:
                    _logger.warning("Unable to read %s: %s. Skipping this file.", file_path, str(e))
                    continue

            escaped_relative_path = escape_markdown_characters(relative_path)
            codebase += f"\n#### {escaped_relative_path}\n\n```{file_extension[1:]}\n{content.rstrip()}\n```\n"

    codebase = remove_trailing_whitespace(codebase)

    return codebase
