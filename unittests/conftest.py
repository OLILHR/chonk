import os
from unittest.mock import mock_open

import pytest


@pytest.fixture(scope="session")
def project_root():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


@pytest.fixture(scope="function")
def mock_alloyignore():
    return ".png\n.svg\n"


@pytest.fixture(scope="function")
def mock_project(project_root, mock_alloyignore):
    files = {
        os.path.join(project_root, "markdown.md"): "# markdown content",
        os.path.join(project_root, "python.py"): 'print("python content")',
        os.path.join(project_root, "text.txt"): "text content",
        os.path.join(project_root, "image.png"): "<image content>",
        os.path.join(project_root, "subdirectory", "markup.yml"): "key: value",
        os.path.join(project_root, "subdirectory", "vector.svg"): "<svg></svg>",
        os.path.join(project_root, ".alloyignore"): mock_alloyignore,
    }
    return files


@pytest.fixture(scope="function")
def mock_operations(monkeypatch, mock_project):
    def _mock_open(file, mode="r", encoding=None):
        return mock_open(read_data=mock_project[file])(file, mode, encoding)

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
            elif len(parts) == 1 and parts[0] != ".alloyignore":
                files.append(parts[0])

        yield top, list(directories), files

        for directory in directories:
            subdir = os.path.join(top, directory)
            subdir_files = [os.path.basename(f) for f in mock_project.keys() if os.path.dirname(f) == subdir]
            yield subdir, [], subdir_files

    monkeypatch.setattr("builtins.open", _mock_open)
    monkeypatch.setattr("os.path.exists", _mock_exists)
    monkeypatch.setattr("os.walk", _mock_walk)
