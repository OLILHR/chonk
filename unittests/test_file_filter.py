import os
import re

from alloy.collector import consolidate, escape_markdown_characters


def test_consolidate_specified_filter_extensions(
    project_root, mock_project, mock_operations, mock_alloyignore
):  # pylint: disable=unused-argument
    filtered_codebase = consolidate(project_root, extensions=["md", "txt"])

    assert not any(extension in mock_alloyignore for extension in [".md", ".txt", ".py", ".yml"])
    assert re.search(rf"#### {re.escape(escape_markdown_characters('markdown.md'))}", filtered_codebase)
    assert re.search(rf"#### {re.escape(escape_markdown_characters('text.txt'))}", filtered_codebase)
    assert not re.search(rf"#### {re.escape(escape_markdown_characters('python.py'))}", filtered_codebase)
    assert not re.search(
        rf"#### {re.escape(escape_markdown_characters(os.path.join('subdirectory', 'markup.yml')))}",
        filtered_codebase,
    )

    assert ".png" in mock_alloyignore
    assert not re.search(rf"#### {re.escape(escape_markdown_characters('image.png'))}", filtered_codebase)
    assert ".svg" in mock_alloyignore
    assert not re.search(
        rf"#### {re.escape(escape_markdown_characters(os.path.join('subdirectory', 'vector.svg')))}",
        filtered_codebase,
    )


def test_extension_filter_bypasses_alloyignore(
    project_root, mock_project, mock_operations, mock_alloyignore
):  # pylint: disable=unused-argument
    filtered_codebase = consolidate(project_root, extensions=["svg"])

    assert ".svg" in mock_alloyignore
    assert re.search(
        rf"#### {re.escape(escape_markdown_characters(os.path.join('subdirectory', 'vector.svg')))}",
        filtered_codebase,
    )

    assert not re.search(rf"#### {re.escape(escape_markdown_characters('markdown.md'))}", filtered_codebase)
    assert not re.search(rf"#### {re.escape(escape_markdown_characters('text.txt'))}", filtered_codebase)
    assert not re.search(rf"#### {re.escape(escape_markdown_characters('python.py'))}", filtered_codebase)
    assert not re.search(
        rf"#### {re.escape(escape_markdown_characters(os.path.join('subdirectory', 'markup.yml')))}",
        filtered_codebase,
    )
    assert not re.search(rf"#### {re.escape(escape_markdown_characters('image.png'))}", filtered_codebase)
