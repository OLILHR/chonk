import os
from unittest.mock import mock_open, patch

from alloy.filter import DEFAULT_IGNORE_LIST, ignore_comments, read_alloyignore


def test_read_alloyignore(
    mock_alloyignore,
    mock_alloyignore_content,
    project_root,
):
    print("Starting test_read_alloyignore")
    print(f"mock_alloyignore: {mock_alloyignore}")
    print(f"mock_alloyignore_content: {mock_alloyignore_content}")
    print(f"project_root: {project_root}")
    print(f"DEFAULT_IGNORE_LIST: {DEFAULT_IGNORE_LIST}")

    assert ".png" in mock_alloyignore_content
    assert ".svg" in mock_alloyignore_content

    expected_path = os.path.join(project_root, ".alloyignore")
    print(f"Expected .alloyignore path: {expected_path}")

    def mock_read_alloyignore(project_root, extension_filter):
        print(f"mock_read_alloyignore called with project_root: {project_root}, extension_filter: {extension_filter}")
        exclude_func = read_alloyignore(project_root, extension_filter)
        print(f"Exclude function created: {exclude_func}")
        return exclude_func

    with patch("alloy.filter.read_alloyignore", side_effect=mock_read_alloyignore):
        with patch("builtins.open", mock_open(read_data=mock_alloyignore)) as mock_file:
            print("Calling read_alloyignore")
            exclude = read_alloyignore(project_root, [])
            print(f"Exclude function: {exclude}")

            print("Testing exclude function")
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
                print(f"exclude('{file}') = {result}")
                if file in ["test.png", "test.svg", "test.log"] or file.startswith("node_modules/"):
                    assert result is True, f"Expected exclude('{file}') to be True, but got False"
                else:
                    assert result is False, f"Expected exclude('{file}') to be False, but got True"

    print("Finished test_read_alloyignore")

    # Check if the mock file was opened with the correct arguments
    mock_file.assert_called_once_with(expected_path, "r", encoding="utf-8")


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
