import os

import pytest


@pytest.fixture
def setup_paths(request):
    unittests_dir = os.path.dirname(request.module.__file__)
    return {
        "test_data": os.path.join(unittests_dir, "data"),
    }
