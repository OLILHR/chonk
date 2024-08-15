import os
import re

from alloy.collector import consolidate, escape_markdown_characters
from alloy.filter import read_alloyignore


def test_read_alloyignore(project_root, mock_alloyignore):
    exclude = read_alloyignore(project_root, [])

    with open(mock_alloyignore, encoding="utf-8") as f:
        alloyignore = f.read()

    assert ".png" in alloyignore
    assert exclude("test.png") is True
    assert ".svg" in alloyignore
    assert exclude("test.svg") is True

    assert exclude("test.md") is False
    assert exclude("test.txt") is False
    assert exclude("test.py") is False
    assert exclude("test.yml") is False


def test_consolidate_excludes_png_files(unittests_directory, mock_alloyignore):
    codebase = consolidate(unittests_directory["mock_data"])

    with open(mock_alloyignore, encoding="utf-8") as f:
        alloyignore = f.read()

    assert re.search(rf"#### {re.escape(escape_markdown_characters('dummy_md.md'))}", codebase)
    assert re.search(rf"#### {re.escape(escape_markdown_characters('dummy_txt.txt'))}", codebase)
    assert re.search(rf"#### {re.escape(escape_markdown_characters('dummy_py.py'))}", codebase)

    assert ".png" in alloyignore
    assert not re.search(rf"#### {re.escape(escape_markdown_characters('dummy_png.png'))}", codebase)


def test_consolidate_considers_subdirectories(unittests_directory, mock_alloyignore):
    codebase = consolidate(unittests_directory["mock_data"])

    assert re.search(rf"#### {re.escape(escape_markdown_characters('dummy_md.md'))}", codebase)
    assert re.search(rf"#### {re.escape(escape_markdown_characters('dummy_txt.txt'))}", codebase)
    assert re.search(rf"#### {re.escape(escape_markdown_characters('dummy_py.py'))}", codebase)

    subdir_yml_path = os.path.join("dummy_subdirectory", "dummy_yml.yml")
    assert re.search(
        rf"#### {re.escape(escape_markdown_characters(subdir_yml_path))}", codebase
    ), f"File {subdir_yml_path} not found in consolidated output"

    subdir_svg_path = os.path.join("dummy_subdirectory", "dummy_svg.svg")
    assert not re.search(
        rf"#### {re.escape(escape_markdown_characters(subdir_svg_path))}", codebase
    ), f"File {subdir_svg_path} should be excluded as per .alloyignore"
