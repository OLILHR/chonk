import os
import re

import pytest

from codebase.utilities import consolidate, escape_markdown_characters, remove_trailing_whitespace


def test_consolidate_excludes_ignored_files(
    project_root, mock_project, mock_operations
):  # pylint: disable=unused-argument
    codebase, *_ = consolidate(project_root)
    codebaseignore = mock_project[os.path.join(project_root, ".codebaseignore")]

    assert ".png" in codebaseignore
    assert ".svg" in codebaseignore
    assert not re.search(rf"#### {re.escape(escape_markdown_characters('image.png'))}", codebase)
    assert not re.search(rf"#### {re.escape(escape_markdown_characters('vector.svg'))}", codebase)

    assert ".markdown.md" not in codebaseignore
    assert ".python.py" not in codebaseignore
    assert "text.txt" not in codebaseignore
    assert re.search(rf"#### {re.escape(escape_markdown_characters('markdown.md'))}", codebase)
    assert re.search(rf"#### {re.escape(escape_markdown_characters('python.py'))}", codebase)
    assert re.search(rf"#### {re.escape(escape_markdown_characters('text.txt'))}", codebase)


def test_consolidate_considers_subdirectories(
    project_root, mock_project, mock_operations
):  # pylint: disable=unused-argument
    codebase, *_ = consolidate(project_root)

    print(f"Mock project structure: {mock_project}")
    print(f"Consolidated codebase:\n{codebase}")

    assert re.search(rf"#### {re.escape(escape_markdown_characters('markdown.md'))}", codebase)
    assert re.search(rf"#### {re.escape(escape_markdown_characters('text.txt'))}", codebase)
    assert re.search(rf"#### {re.escape(escape_markdown_characters('python.py'))}", codebase)

    subdir_yml_path = os.path.join("subdirectory", "markup.yml")
    assert re.search(
        rf"#### {re.escape(escape_markdown_characters(subdir_yml_path))}", codebase
    ), f"File {subdir_yml_path} not found in consolidated output"

    subdir_svg_path = os.path.join("subdirectory", "vector.svg")
    assert not re.search(
        rf"#### {re.escape(escape_markdown_characters(subdir_svg_path))}", codebase
    ), f"File {subdir_svg_path} should be excluded as per .codebaseignore"


def test_consolidate_file_token_count(project_root, mock_project, mock_operations):  # pylint: disable=unused-argument
    _, file_count, token_count, *_ = consolidate(project_root)

    expected_file_count = len(
        [
            f
            for f in mock_project.keys()
            if not f.endswith(".codebaseignore") and not f.endswith(".png") and not f.endswith(".svg")
        ]
    )

    assert file_count == expected_file_count
    assert token_count > 0


def test_consolidate_line_of_code_count(project_root, mock_project, mock_operations):  # pylint: disable=unused-argument
    _, lines_of_code_count, *_ = consolidate(project_root)

    expected_lines_of_code_count = sum(
        len(content.split("\n"))
        for file_path, content in mock_project.items()
        if not file_path.endswith((".codebaseignore", ".png", ".svg"))
    )

    assert lines_of_code_count == expected_lines_of_code_count


def test_consolidate_file_type_distribution(
    project_root, mock_project, mock_operations
):  # pylint: disable=unused-argument
    codebase, file_count, *_ = consolidate(project_root)

    expected_types = {
        "py": 1,  # mock_project/python.py
        "md": 1,  # mock_project/markdown.md
        "txt": 1,  # mock_project/text.txt
        "yml": 1,  # mock_project/subdirectory/markup.yml
    }
    file_type_distribution = sum(expected_types.values())

    assert file_count == file_type_distribution

    for file_type in expected_types:
        assert re.search(rf"#### .*\.{file_type.lower()}", codebase, re.IGNORECASE)


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
