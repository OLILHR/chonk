import os
import re

from src import filter_extensions, parse_extensions
from src import consolidate, escape_markdown_characters


def test_consolidate_only_specified_filters(
    project_root, mock_project, mock_operations, mock_chonkignore
):  # pylint: disable=unused-argument
    filtered_chonk, *_ = consolidate(project_root, extensions=["md", "txt"])

    assert not any(extension in mock_chonkignore for extension in [".md", ".txt", ".py", ".yml"])
    assert re.search(rf"#### {re.escape(escape_markdown_characters('markdown.md'))}", filtered_chonk)
    assert re.search(rf"#### {re.escape(escape_markdown_characters('text.txt'))}", filtered_chonk)

    assert not re.search(rf"#### {re.escape(escape_markdown_characters('python.py'))}", filtered_chonk)
    assert not re.search(
        rf"#### {re.escape(escape_markdown_characters(os.path.join('subdirectory', 'markup.yml')))}",
        filtered_chonk,
    )

    assert ".png" in mock_chonkignore
    assert not re.search(rf"#### {re.escape(escape_markdown_characters('image.png'))}", filtered_chonk)
    assert ".svg" in mock_chonkignore
    assert not re.search(
        rf"#### {re.escape(escape_markdown_characters(os.path.join('subdirectory', 'vector.svg')))}",
        filtered_chonk,
    )


def test_filter_bypasses_chonkignore(
    project_root, mock_project, mock_operations, mock_chonkignore
):  # pylint: disable=unused-argument
    filtered_chonk, *_ = consolidate(project_root, extensions=["svg"])

    assert ".svg" in mock_chonkignore
    assert re.search(
        rf"#### {re.escape(escape_markdown_characters(os.path.join('subdirectory', 'vector.svg')))}",
        filtered_chonk,
    )

    assert not re.search(rf"#### {re.escape(escape_markdown_characters('markdown.md'))}", filtered_chonk)
    assert not re.search(rf"#### {re.escape(escape_markdown_characters('text.txt'))}", filtered_chonk)
    assert not re.search(rf"#### {re.escape(escape_markdown_characters('python.py'))}", filtered_chonk)
    assert not re.search(
        rf"#### {re.escape(escape_markdown_characters(os.path.join('subdirectory', 'markup.yml')))}",
        filtered_chonk,
    )
    assert not re.search(rf"#### {re.escape(escape_markdown_characters('image.png'))}", filtered_chonk)


def test_filter_extensions_edge_cases():
    assert filter_extensions("test.py", []) is True
    assert filter_extensions("test.py", None) is True
    assert filter_extensions("test.py", ["py"]) is True

    assert filter_extensions("test", ["py"]) is False
    assert filter_extensions(".gitignore", ["py"]) is False


def test_parse_extensions_edge_cases():
    assert parse_extensions(None, None, []) is None
    assert parse_extensions(None, None, ["py, js, css"]) == ["py", "js", "css"]
    assert parse_extensions(None, None, ["py", "js", "css"]) == ["py", "js", "css"]
