import io
import os
from unittest.mock import MagicMock, mock_open

import pytest


@pytest.fixture(scope="session")
def project_root():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


@pytest.fixture(scope="function")
def mock_chonkignore_content():
    return [
        ".png",
        ".svg",
        "*.log",
        "/node_modules/",
        # comment
    ]


@pytest.fixture(scope="function")
def mock_chonkignore(mock_chonkignore_content):
    return "\n".join(mock_chonkignore_content) + "\n"


@pytest.fixture(scope="function")
def mock_project(project_root, mock_chonkignore):
    files = {
        os.path.join(project_root, "markdown.md"): "# markdown content",
        os.path.join(project_root, "python.py"): 'print("python content")',
        os.path.join(project_root, "text.txt"): "text content",
        os.path.join(project_root, "image.png"): "<image content>",
        os.path.join(project_root, "subdirectory", "markup.yml"): "key: value",
        os.path.join(project_root, "subdirectory", "vector.svg"): "<svg></svg>",
        os.path.join(project_root, ".chonkignore"): mock_chonkignore,
    }
    return files


@pytest.fixture(scope="function")
def mock_operations(monkeypatch, mock_project):
    def _mock_open(file, mode="r", encoding=None):
        if file in mock_project:
            return mock_open(read_data=mock_project[file])(file, mode, encoding)
        return io.StringIO("")  # Return empty file-like object for unknown files

    def _mock_exists(path):
        return path in mock_project

    def _mock_walk(top):
        directories = set()
        files = []
        for path in mock_project.keys():
            relpath = os.path.relpath(path, top)
            parts = relpath.split(os.sep)
            if len(parts) > 1:
                directories.add(parts[0])
            elif len(parts) == 1 and parts[0] != ".chonkignore":
                files.append(parts[0])

        yield top, list(directories), files

        for directory in directories:
            subdir = os.path.join(top, directory)
            subdir_files = [os.path.basename(f) for f in mock_project.keys() if os.path.dirname(f) == subdir]
            yield subdir, [], subdir_files

    monkeypatch.setattr("builtins.open", _mock_open)
    monkeypatch.setattr("os.path.exists", _mock_exists)
    monkeypatch.setattr("os.walk", _mock_walk)

    # Fully mock tiktoken
    mock_tiktoken = MagicMock()
    mock_encoding = MagicMock()
    mock_encoding.encode.return_value = [1, 2, 3]  # Dummy token ids
    mock_tiktoken.get_encoding.return_value = mock_encoding
    monkeypatch.setattr("tiktoken.get_encoding", mock_tiktoken.get_encoding)

    # Mock the entire tiktoken module
    monkeypatch.setattr("chonk.utilities.tiktoken", mock_tiktoken)
