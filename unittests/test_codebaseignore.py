import os
from unittest.mock import mock_open, patch

from codebase.filter import skip_ignore_list_comments, read_codebaseignore


def test_read_codebaseignore(
    mock_codebaseignore,
    mock_codebaseignore_content,
    project_root,
):

    assert ".png" in mock_codebaseignore_content
    assert ".svg" in mock_codebaseignore_content

    expected_path = os.path.join(project_root, ".codebaseignore")

    with patch("os.path.exists", return_value=True):
        with patch("builtins.open", mock_open(read_data=mock_codebaseignore)) as mock_file:
            exclude = read_codebaseignore(project_root, [])

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


def test_skip_ignore_list_comments(mock_codebaseignore, mock_codebaseignore_content, project_root):
    codebaseignore_path = os.path.join(project_root, ".codebaseignore")

    with patch("builtins.open", mock_open(read_data=mock_codebaseignore)) as mock_file:
        result = skip_ignore_list_comments(codebaseignore_path)

    mock_file.assert_called_once_with(codebaseignore_path, "r", encoding="utf-8")
    expected_result = [line for line in mock_codebaseignore_content if line and not line.startswith("#")]

    assert result == expected_result, f"Expected {expected_result}, but got {result}"

    for content in mock_codebaseignore_content:
        if content and not content.startswith("#"):
            assert content in result

    assert "# comment" not in result
