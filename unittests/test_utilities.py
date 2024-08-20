import os
import re

import pytest

from epitaxy.utilities import consolidate, escape_markdown_characters, remove_trailing_whitespace


def test_consolidate_excludes_ignored_files(
    project_root, mock_project, mock_operations
):  # pylint: disable=unused-argument
    epitaxy, *_ = consolidate(project_root)
    epitaxyignore = mock_project[os.path.join(project_root, ".epitaxyignore")]

    assert ".png" in epitaxyignore
    assert ".svg" in epitaxyignore
    assert not re.search(rf"#### {re.escape(escape_markdown_characters('image.png'))}", epitaxy)
    assert not re.search(rf"#### {re.escape(escape_markdown_characters('vector.svg'))}", epitaxy)

    assert ".markdown.md" not in epitaxyignore
    assert ".python.py" not in epitaxyignore
    assert "text.txt" not in epitaxyignore
    assert re.search(rf"#### {re.escape(escape_markdown_characters('markdown.md'))}", epitaxy)
    assert re.search(rf"#### {re.escape(escape_markdown_characters('python.py'))}", epitaxy)
    assert re.search(rf"#### {re.escape(escape_markdown_characters('text.txt'))}", epitaxy)


def test_consolidate_considers_subdirectories(
    project_root, mock_project, mock_operations
):  # pylint: disable=unused-argument
    epitaxy, *_ = consolidate(project_root)

    assert re.search(rf"#### {re.escape(escape_markdown_characters('markdown.md'))}", epitaxy)
    assert re.search(rf"#### {re.escape(escape_markdown_characters('text.txt'))}", epitaxy)
    assert re.search(rf"#### {re.escape(escape_markdown_characters('python.py'))}", epitaxy)

    subdir_yml_path = os.path.join("subdirectory", "markup.yml")
    assert re.search(rf"#### {re.escape(escape_markdown_characters(subdir_yml_path))}", epitaxy)

    subdir_svg_path = os.path.join("subdirectory", "vector.svg")
    assert not re.search(rf"#### {re.escape(escape_markdown_characters(subdir_svg_path))}", epitaxy)


def test_consolidate_file_token_count(project_root, mock_project, mock_operations):  # pylint: disable=unused-argument
    _, file_count, token_count, *_ = consolidate(project_root)

    expected_file_count = len(
        [
            f
            for f in mock_project.keys()
            if not f.endswith(".epitaxyignore") and not f.endswith(".png") and not f.endswith(".svg")
        ]
    )

    assert file_count == expected_file_count
    assert token_count > 0


def test_consolidate_line_of_code_count(project_root, mock_project, mock_operations):  # pylint: disable=unused-argument
    _, lines_of_code_count, *_ = consolidate(project_root)

    expected_lines_of_code_count = sum(
        len(content.split("\n"))
        for file_path, content in mock_project.items()
        if not file_path.endswith((".epitaxyignore", ".png", ".svg"))
    )

    assert lines_of_code_count == expected_lines_of_code_count


def test_consolidate_file_type_distribution(
    project_root, mock_project, mock_operations
):  # pylint: disable=unused-argument
    epitaxy, file_count, *_ = consolidate(project_root)

    expected_types = {
        "py": 1,  # mock_project/python.py
        "md": 1,  # mock_project/markdown.md
        "txt": 1,  # mock_project/text.txt
        "yml": 1,  # mock_project/subdirectory/markup.yml
    }
    file_type_distribution = sum(expected_types.values())

    assert file_count == file_type_distribution

    for file_type in expected_types:
        assert re.search(rf"#### .*\.{file_type.lower()}", epitaxy, re.IGNORECASE)


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
