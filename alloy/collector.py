import logging
import os
import re

import tiktoken

from .filter import filter_extensions, read_alloyignore

_logger = logging.getLogger(__name__)


def remove_trailing_whitespace(content):
    content = re.sub(r"\n{3,}", "\n\n", content)
    content = re.sub(r" +$", "", content, flags=re.MULTILINE)
    return content


def escape_markdown_characters(file_name):
    """
    Escapes special characters in file names such as "__init__.py"
    in order to display paths correctly inside the output markdown file.
    """
    special_chars = r"([*_`\[\]()~>#+=|{}.!-])"
    return re.sub(special_chars, r"\\\1", file_name)


def count_tokens(text):
    """
    Encoding for GPT-3.5/GPT-4.0.
    """
    encoding = tiktoken.get_encoding("cl100k_base")
    return len(encoding.encode(text))


# pylint: disable=too-many-locals
def consolidate(path, extensions=None):
    """
    Gathers and formats the content and metadata of all files inside a provided input directory,
    while taking into account optional extension filters as well as .alloyignore specific exceptions.
    """
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    exclude_files = read_alloyignore(project_root, extensions)
    codebase = ""
    file_count = 0
    token_count = 0

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
            file_content = f"\n#### {escaped_relative_path}\n\n```{file_extension[1:]}\n{content.rstrip()}\n```\n"
            codebase += file_content
            file_count += 1
            token_count += count_tokens(file_content)

    codebase = remove_trailing_whitespace(codebase)

    return codebase, file_count, token_count
