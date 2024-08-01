import os

import pytest


@pytest.fixture
def unittests_directory(request):
    unittests_dir = os.path.dirname(request.module.__file__)
    return {
        "test_data": os.path.join(unittests_dir, "data"),
    }


@pytest.fixture
def alloyignore_path(unittests_directory):
    return os.path.join(unittests_directory["test_data"], ".alloyignore")
