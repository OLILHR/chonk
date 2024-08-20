import os
from unittest.mock import mock_open, patch

from epitaxy.filter import read_epitaxyignore, skip_ignore_list_comments


def test_read_epitaxyignore(
    mock_epitaxyignore,
    mock_epitaxyignore_content,
    project_root,
):

    assert ".png" in mock_epitaxyignore_content
    assert ".svg" in mock_epitaxyignore_content

    expected_path = os.path.join(project_root, ".epitaxyignore")

    with patch("os.path.exists", return_value=True):
        with patch("builtins.open", mock_open(read_data=mock_epitaxyignore)) as mock_file:
            exclude = read_epitaxyignore(project_root, [])

            test_files = [
                "test.png",
                "test.svg",
                "test.log",
                "node_modules/test.json",
                "test.md",
                "test.txt",
                "test.py",
                "test.yml",
            ]
            for file in test_files:
                result = exclude(file)
                if file in ["test.png", "test.svg", "test.log"] or file.startswith("node_modules/"):
                    assert result is True
                else:
                    assert result is False

    mock_file.assert_called_once_with(expected_path, "r", encoding="utf-8")


def test_skip_ignore_list_comments(mock_epitaxyignore, mock_epitaxyignore_content, project_root):
    epitaxyignore_path = os.path.join(project_root, ".epitaxyignore")

    with patch("builtins.open", mock_open(read_data=mock_epitaxyignore)) as mock_file:
        result = skip_ignore_list_comments(epitaxyignore_path)

    mock_file.assert_called_once_with(epitaxyignore_path, "r", encoding="utf-8")
    expected_result = [line for line in mock_epitaxyignore_content if line and not line.startswith("#")]

    assert result == expected_result, f"Expected {expected_result}, but got {result}"

    for content in mock_epitaxyignore_content:
        if content and not content.startswith("#"):
            assert content in result

    assert "# comment" not in result
