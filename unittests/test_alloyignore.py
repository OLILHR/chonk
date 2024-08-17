import os
from unittest.mock import mock_open, patch

from alloy.filter import ignore_comments, read_alloyignore


def test_read_alloyignore(
    mock_alloyignore,
    mock_alloyignore_content,
    project_root,
):

    assert ".png" in mock_alloyignore_content
    assert ".svg" in mock_alloyignore_content

    with patch("builtins.open", mock_open(read_data=mock_alloyignore)):
        exclude = read_alloyignore(project_root, [])

        assert exclude("test.png") is True
        assert exclude("test.svg") is True
        assert exclude("test.log") is True
        assert exclude("node_modules/test.json") is True
        assert exclude("subdirectory/node_modules/test.json") is True

        assert exclude("test.md") is False
        assert exclude("test.txt") is False
        assert exclude("test.py") is False
        assert exclude("test.yml") is False

        assert exclude("# comment") is False


def test_ignore_comments(mock_alloyignore, mock_alloyignore_content, project_root):
    alloyignore_path = os.path.join(project_root, ".alloyignore")

    with patch("builtins.open", mock_open(read_data=mock_alloyignore)) as mock_file:
        result = ignore_comments(alloyignore_path)

    mock_file.assert_called_once_with(alloyignore_path, "r", encoding="utf-8")
    expected_result = [line for line in mock_alloyignore_content if line and not line.startswith("#")]

    assert result == expected_result, f"Expected {expected_result}, but got {result}"

    for content in mock_alloyignore_content:
        if content and not content.startswith("#"):
            assert content in result

    assert "# comment" not in result
