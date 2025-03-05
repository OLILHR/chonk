import logging
import os
import re
from collections import Counter
from dataclasses import dataclass
from typing import List, Optional, Tuple

import tiktoken
from tqdm import tqdm

from .filter import filter_extensions, read_chonkignore

_logger = logging.getLogger(__name__)


def remove_trailing_whitespace(content: str) -> str:
    content = re.sub(r"\n{3,}", "\n\n", content)
    content = re.sub(r" +$", "", content, flags=re.MULTILINE)
    return content


def escape_markdown_characters(file_name: str) -> str:
    """
    Escapes special characters in file names such as "__init__.py"
    in order to display paths correctly inside the output markdown file.
    """
    special_chars = r"([*_`\[\]()~>#+=|{}.!-])"
    return re.sub(special_chars, r"\\\1", file_name)


def count_lines_of_code(content: str) -> int:
    """
    Counts the lines of code within each code blocks in the output markdown file.
    """
    codeblocks = re.findall(r"```[\s\S]*?```", content)
    lines_of_code = sum(len(block.split("\n")) - 2 for block in codeblocks)  # subtracts 2x ``` from codeblocks
    return lines_of_code


def get_file_type_distribution(markdown_content: str) -> List[Tuple[str, float]]:
    """
    Returns a distribution of the four most common file types in the output markdown file.
    """
    file_types = [line.split(".")[-1] for line in markdown_content.split("\n") if line.startswith("####")]
    type_counter = Counter(file_types)
    total_files = len(file_types)

    most_common_types = type_counter.most_common(4)
    type_distribution = [(file_type, count / total_files * 100) for file_type, count in most_common_types]

    if len(type_counter) > 4:
        other_count = sum(
            count for file_type, count in type_counter.items() if file_type not in dict(most_common_types)
        )
        type_distribution.append(("other", other_count / total_files * 100))

    return type_distribution


def count_tokens(text: str) -> int:
    """
    Encoding for GPT-3.5/GPT-4.0.
    """
    encoding = tiktoken.get_encoding("cl100k_base")
    return len(encoding.encode(text))


@dataclass
class NoMatchingExtensionError(Exception):
    """
    Raised when no files match the specified extensions (optional filter argument).
    """

    exception: str


# pylint: disable=too-many-locals
def consolidate(
    path: str, extensions: Optional[List[str]] = None
) -> Tuple[str, int, int, int, List[Tuple[str, float]]]:
    """
    Gathers and formats the content and metadata of all files inside a provided input directory,
    while taking into account optional extension filters as well as .chonkignore specific exceptions.
    """
    exclude_files = read_chonkignore(path, extensions)
    chonk = ""
    file_count = 0
    token_count = 0
    lines_of_code_count = 0

    matching_filter_extensions: List[str] = []
    for root, dirs, files in os.walk(path):
        dirs[:] = [d for d in dirs if not exclude_files(os.path.relpath(str(os.path.join(root, d)), path))]
        for file in files:
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(str(file_path), path)
            if not exclude_files(relative_path) and (not extensions or filter_extensions(file_path, extensions)):
                matching_filter_extensions.append(file_path)
                file_count += 1

    if not matching_filter_extensions:
        raise NoMatchingExtensionError("⚠️ NO FILES MATCH THE SPECIFIED EXTENSIONS.")

    with tqdm(
        total=file_count,
        unit="file",
        ncols=100,
        bar_format="▶️ | {desc}: {bar:45} {percentage:3.0f}% | {n_fmt}/{total_fmt}",
    ) as progress_bar:
        for file_path in matching_filter_extensions:
            relative_path = os.path.relpath(str(file_path), path)
            _, file_extension = os.path.splitext(file_path)

            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
            except UnicodeDecodeError:
                try:
                    with open(file_path, "r", encoding="iso-8859-1") as f:
                        content = f.read()
                except (OSError, IOError) as e:
                    _logger.warning(file_path, str(e))
                    continue

            escaped_relative_path = escape_markdown_characters(relative_path)
            file_content = f"\n#### {escaped_relative_path}\n\n```{file_extension[1:]}\n{content.rstrip()}\n```\n"
            chonk += file_content
            token_count += count_tokens(file_content)
            lines_of_code_count += len(content.split("\n"))

            progress_bar.update(1)

    chonk = remove_trailing_whitespace(chonk)
    type_distribution = get_file_type_distribution(chonk)

    return chonk, file_count, token_count, lines_of_code_count, type_distribution
