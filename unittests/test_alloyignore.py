import logging
import os
from unittest.mock import mock_open, patch

from alloy.filter import DEFAULT_IGNORE_LIST, ignore_comments, read_alloyignore

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def test_read_alloyignore(
    mock_alloyignore,
    mock_alloyignore_content,
    project_root,
):
    logger.info("Starting test_read_alloyignore")
    logger.debug("mock_alloyignore: %s", mock_alloyignore)
    logger.debug("mock_alloyignore_content: %s", mock_alloyignore_content)
    logger.debug("project_root: %s", project_root)
    logger.debug("DEFAULT_IGNORE_LIST: %s", DEFAULT_IGNORE_LIST)

    assert ".png" in mock_alloyignore_content
    assert ".svg" in mock_alloyignore_content

    expected_path = os.path.join(project_root, ".alloyignore")
    logger.debug("Expected .alloyignore path: %s", expected_path)

    def mock_read_alloyignore(project_root, extension_filter):
        logger.debug(
            "mock_read_alloyignore called with project_root: %s, extension_filter: %s", project_root, extension_filter
        )
        exclude_func = read_alloyignore(project_root, extension_filter)
        logger.debug("Exclude function created: %s", exclude_func)
        return exclude_func

    with patch("alloy.filter.read_alloyignore", side_effect=mock_read_alloyignore):
        with patch("builtins.open", mock_open(read_data=mock_alloyignore)) as mock_file:
            logger.info("Calling read_alloyignore")
            exclude = read_alloyignore(project_root, [])
            logger.debug("Exclude function: %s", exclude)

            logger.info("Testing exclude function")
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
                logger.debug("exclude('%s') = %s", file, result)
                if file in ["test.png", "test.svg", "test.log"] or file.startswith("node_modules/"):
                    assert result is True, f"Expected exclude('{file}') to be True, but got False"
                else:
                    assert result is False, f"Expected exclude('{file}') to be False, but got True"

    logger.info("Finished test_read_alloyignore")

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
