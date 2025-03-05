import os
import re

import pytest

<<<<<<< Updated upstream
from chonk.utilities import consolidate, escape_markdown_characters, remove_trailing_whitespace
=======
from src import (
    consolidate,
    escape_markdown_characters,
    remove_trailing_whitespace,
)
>>>>>>> Stashed changes


def test_consolidate_excludes_ignored_files(
    project_root, mock_project, mock_operations
):  # pylint: disable=unused-argument
    chonk, *_ = consolidate(project_root)
    chonkignore = mock_project[os.path.join(project_root, ".chonkignore")]

    assert ".png" in chonkignore
    assert ".svg" in chonkignore
    assert not re.search(rf"#### {re.escape(escape_markdown_characters('image.png'))}", chonk)
    assert not re.search(rf"#### {re.escape(escape_markdown_characters('vector.svg'))}", chonk)

    assert ".markdown.md" not in chonkignore
    assert ".python.py" not in chonkignore
    assert "text.txt" not in chonkignore
    assert re.search(rf"#### {re.escape(escape_markdown_characters('markdown.md'))}", chonk)
    assert re.search(rf"#### {re.escape(escape_markdown_characters('python.py'))}", chonk)
    assert re.search(rf"#### {re.escape(escape_markdown_characters('text.txt'))}", chonk)


def test_consolidate_considers_subdirectories(
    project_root, mock_project, mock_operations
):  # pylint: disable=unused-argument
    chonk, *_ = consolidate(project_root)

    print(f"Mock project structure: {mock_project}")
    print(f"Consolidated chonk:\n{chonk}")

    assert re.search(rf"#### {re.escape(escape_markdown_characters('markdown.md'))}", chonk)
    assert re.search(rf"#### {re.escape(escape_markdown_characters('text.txt'))}", chonk)
    assert re.search(rf"#### {re.escape(escape_markdown_characters('python.py'))}", chonk)

    subdir_yml_path = os.path.join("subdirectory", "markup.yml")
    assert re.search(
        rf"#### {re.escape(escape_markdown_characters(subdir_yml_path))}", chonk
    ), f"File {subdir_yml_path} not found in consolidated output"

    subdir_svg_path = os.path.join("subdirectory", "vector.svg")
    assert not re.search(
        rf"#### {re.escape(escape_markdown_characters(subdir_svg_path))}", chonk
    ), f"File {subdir_svg_path} should be excluded as per .chonkignore"


def test_consolidate_file_token_count(project_root, mock_project, mock_operations):  # pylint: disable=unused-argument
    _, file_count, token_count, *_ = consolidate(project_root)

    expected_file_count = len(
        [
            f
            for f in mock_project.keys()
            if not f.endswith(".chonkignore") and not f.endswith(".png") and not f.endswith(".svg")
        ]
    )

    assert file_count == expected_file_count
    assert token_count > 0


def test_consolidate_line_of_code_count(project_root, mock_project, mock_operations):  # pylint: disable=unused-argument
    _, lines_of_code_count, *_ = consolidate(project_root)

    expected_lines_of_code_count = sum(
        len(content.split("\n"))
        for file_path, content in mock_project.items()
        if not file_path.endswith((".chonkignore", ".png", ".svg"))
    )

    assert lines_of_code_count == expected_lines_of_code_count


def test_consolidate_file_type_distribution(
    project_root, mock_project, mock_operations
):  # pylint: disable=unused-argument
    chonk, file_count, *_ = consolidate(project_root)

    expected_types = {
        "py": 1,  # mock_project/python.py
        "md": 1,  # mock_project/markdown.md
        "txt": 1,  # mock_project/text.txt
        "yml": 1,  # mock_project/subdirectory/markup.yml
    }
    file_type_distribution = sum(expected_types.values())

    assert file_count == file_type_distribution

    for file_type in expected_types:
        assert re.search(rf"#### .*\.{file_type.lower()}", chonk, re.IGNORECASE)


def test_consolidate_removes_trailing_whitespace():
    input_content = "trailing whitespace         "
    expected_output = "trailing whitespace"

    output = remove_trailing_whitespace(input_content)

    assert output == expected_output
    assert not re.search(r"\n{3,}", output)
    assert not re.search(r" +$", output, re.MULTILINE)


def test_remove_trailing_whitespace_multiple_newlines():
    input_content = "test\n\n\n\ntest\n\n\n"
    expected_output = "test\n\ntest\n\n"
    assert remove_trailing_whitespace(input_content) == expected_output


@pytest.mark.parametrize(
    "file, expected",
    [
        ("normal.py", "normal\\.py"),
        ("__init__.py", "\\_\\_init\\_\\_\\.py"),
        ("test-[file].md", "test\\-\\[file\\]\\.md"),
        ("test_file.txt", "test\\_file\\.txt"),
        ("!important.test", "\\!important\\.test"),
        ("(test).js", "\\(test\\)\\.js"),
    ],
)
def test_escape_markdown_characters(file, expected):
    assert escape_markdown_characters(file) == expected
