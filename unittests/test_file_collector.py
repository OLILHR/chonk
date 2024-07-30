from alloy.collector import consolidate, read_alloyignore


def test_consolidate_excludes_png_and_svg(setup_paths):
    codebase = consolidate(setup_paths["test_data"])

    assert "dummy.md" in codebase
    assert "dummy.txt" in codebase
    assert "dummy.py" in codebase
    assert "dummy.yml" in codebase

    assert "dummy.png" not in codebase
    assert "dummy.svg" not in codebase


def test_read_alloyignore(setup_paths):
    exclude = read_alloyignore(setup_paths["test_data"])

    assert exclude("test.png") is True
    assert exclude("test.svg") is True

    assert exclude("test.md") is False
    assert exclude("test.txt") is False
    assert exclude("test.py") is False
    assert exclude("test.yml") is False
