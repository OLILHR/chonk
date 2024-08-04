from alloy.collector import consolidate
from alloy.filter import read_alloyignore


def test_read_alloyignore(project_root, mock_alloyignore):
    exclude = read_alloyignore(project_root, [])

    with open(mock_alloyignore, encoding="utf-8") as f:
        alloyignore = f.read()

    assert ".png" in alloyignore
    assert exclude("test.png") is True
    assert ".svg" in alloyignore
    assert exclude("test.svg") is True

    assert exclude("test.md") is False
    assert exclude("test.txt") is False
    assert exclude("test.py") is False
    assert exclude("test.yml") is False


def test_consolidate_excludes_png_and_svg(unittests_directory, mock_alloyignore):
    codebase = consolidate(unittests_directory["mock_data"])

    with open(mock_alloyignore, encoding="utf-8") as f:
        alloyignore = f.read()

    assert "dummy_md.md" in codebase
    assert "dummy_txt.txt" in codebase
    assert "dummy_py.py" in codebase
    assert "dummy_yml.yml" in codebase

    assert ".png" in alloyignore
    assert "dummy_png.png" not in codebase
    assert ".svg" in alloyignore
    assert "dummy_svg.svg" not in codebase
