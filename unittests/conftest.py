import os

import pytest


@pytest.fixture(scope="session")
def project_root():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


@pytest.fixture(scope="session")
def unittests_directory(project_root):
    return {
        "mock_data": os.path.join(project_root, "unittests", "data"),
    }


@pytest.fixture(scope="function")
def mock_alloyignore(monkeypatch, project_root):
    """
    Ensures unittests use the .alloyignore.mock file and returns its path.
    """
    mock_alloyignore_path = os.path.join(project_root, ".alloyignore.mock")
    original_join = os.path.join

    def mock_join(*args):
        if args[-1] == ".alloyignore":
            return mock_alloyignore_path
        return original_join(*args)

    monkeypatch.setattr(os.path, "join", mock_join)

    return mock_alloyignore_path
