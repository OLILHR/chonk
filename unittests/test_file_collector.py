from alloy.collector import consolidate, read_alloyignore


def test_consolidate_excludes_png_and_svg(setup_paths):
    codebase = consolidate(setup_paths["test_data"])

    assert "dummy_md.md" in codebase
    assert "dummy_txt.txt" in codebase
    assert "dummy_py.py" in codebase
    assert "dummy_yml.yml" in codebase

    assert "dummy_png.png" not in codebase
    assert "dummy_svg.svg" not in codebase


def test_read_alloyignore(setup_paths):
    exclude = read_alloyignore(setup_paths["test_data"], [])

    assert exclude("test.png") is True
    assert exclude("test.svg") is True

    assert exclude("test.md") is False
    assert exclude("test.txt") is False
    assert exclude("test.py") is False
    assert exclude("test.yml") is False
