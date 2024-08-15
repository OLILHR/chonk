import os
import re

from alloy.collector import consolidate, escape_markdown_characters


def test_consolidate_specified_filter_extensions(unittests_directory, mock_alloyignore):
    filtered_codebase = consolidate(unittests_directory["mock_data"], extensions=["md", "txt"])
    with open(mock_alloyignore, encoding="utf-8") as f:
        alloyignore = f.read()

    assert not any(ext in alloyignore for ext in [".md", ".txt", ".py", ".yml"])
    assert re.search(rf"#### {re.escape(escape_markdown_characters('dummy_md.md'))}", filtered_codebase)
    assert re.search(rf"#### {re.escape(escape_markdown_characters('dummy_txt.txt'))}", filtered_codebase)
    assert not re.search(rf"#### {re.escape(escape_markdown_characters('dummy_py.py'))}", filtered_codebase)
    assert not re.search(
        rf"#### {re.escape(escape_markdown_characters(os.path.join('dummy_subdirectory', 'dummy_yml.yml')))}",
        filtered_codebase,
    )

    assert ".png" in alloyignore
    assert not re.search(rf"#### {re.escape(escape_markdown_characters('dummy_png.png'))}", filtered_codebase)
    assert ".svg" in alloyignore
    assert not re.search(
        rf"#### {re.escape(escape_markdown_characters(os.path.join('dummy_subdirectory', 'dummy_svg.svg')))}",
        filtered_codebase,
    )


def test_extension_filter_bypasses_alloyignore(unittests_directory, mock_alloyignore):
    filtered_codebase = consolidate(unittests_directory["mock_data"], extensions=["svg"])
    with open(mock_alloyignore, encoding="utf-8") as f:
        alloyignore = f.read()

    assert ".svg" in alloyignore
    assert re.search(
        rf"#### {re.escape(escape_markdown_characters(os.path.join('dummy_subdirectory', 'dummy_svg.svg')))}",
        filtered_codebase,
    )

    assert not re.search(rf"#### {re.escape(escape_markdown_characters('dummy_md.md'))}", filtered_codebase)
    assert not re.search(rf"#### {re.escape(escape_markdown_characters('dummy_txt.txt'))}", filtered_codebase)
    assert not re.search(rf"#### {re.escape(escape_markdown_characters('dummy_py.py'))}", filtered_codebase)
    assert not re.search(
        rf"#### {re.escape(escape_markdown_characters(os.path.join('dummy_subdirectory', 'dummy_yml.yml')))}",
        filtered_codebase,
    )
    assert not re.search(rf"#### {re.escape(escape_markdown_characters('dummy_png.png'))}", filtered_codebase)
