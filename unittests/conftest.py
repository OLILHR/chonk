import os

import pytest


@pytest.fixture
def setup_paths(request):
    unittests_dir = os.path.dirname(request.module.__file__)
    return {
        "test_data": os.path.join(unittests_dir, "data"),
    }


@pytest.fixture
def alloyignore_path(setup_paths):
    return os.path.join(setup_paths["test_data"], ".alloyignore")
