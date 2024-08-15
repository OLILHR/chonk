import io
import os

import pytest


@pytest.fixture(scope="session")
def project_root():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


@pytest.fixture(scope="session")
def mock_project_structure():
    files = {
        "markdown.md": "# markdown content",
        "python.py": 'print("python content")',
        "text.txt": "text content",
        "image.png": "<image content>",
        "dummy_directory/markup.yml": "key: value",
        "dummy_directory/vector.svg": "<svg></svg>",
    }
    return files


@pytest.fixture(scope="function")
def mock_alloyignore():
    return ".png\n.svg\n"


@pytest.fixture(scope="function")
def mock_open(mock_project_structure):
    def _mock_open(file, mode="r", encoding=None):
        if file in mock_project_structure:
            return io.StringIO(mock_project_structure[file])
        raise FileNotFoundError(f"Mock file not found: {file}")

    return _mock_open


@pytest.fixture(scope="function")
def mock_os_walk(mock_project_structure):
    def _mock_walk(top, topdown=True, onerror=None, followlinks=False):
        yield "", ["dummy_directory"], [f for f in mock_project_structure if "/" not in f]
        yield "dummy_directory", [], [f.split("/")[-1] for f in mock_project_structure if "/" in f]

    return _mock_walk


@pytest.fixture(scope="function")
def patch_file_operations(monkeypatch, mock_open, mock_os_walk, mock_alloyignore, mock_project_structure):
    monkeypatch.setattr("builtins.open", mock_open)
    monkeypatch.setattr("os.walk", mock_os_walk)
    monkeypatch.setattr("os.path.exists", lambda path: path == ".alloyignore" or path in mock_project_structure)
    return mock_alloyignore
