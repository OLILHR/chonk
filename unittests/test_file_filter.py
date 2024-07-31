from alloy.collector import consolidate


def test_consolidate_specified_filter_extensions(setup_paths, alloyignore_path):
    filtered_codebase = consolidate(setup_paths["test_data"], extensions=["md", "txt"])
    with open(alloyignore_path, encoding="utf-8") as f:
        alloyignore = f.read()

    assert not any(ext in alloyignore for ext in [".md", ".txt", ".py", ".yml"])
    assert "dummy_md.md" in filtered_codebase
    assert "dummy_txt.txt" in filtered_codebase
    assert "dummy_py.py" not in filtered_codebase
    assert "dummy_yml.yml" not in filtered_codebase

    assert ".png" in alloyignore
    assert "dummy_png.png" not in filtered_codebase
    assert ".svg" in alloyignore
    assert "dummy_svg.svg" not in filtered_codebase


def test_extension_filter_bypasses_alloyignore(setup_paths, alloyignore_path):
    filtered_codebase = consolidate(setup_paths["test_data"], extensions=["svg"])
    with open(alloyignore_path, encoding="utf-8") as f:
        alloyignore = f.read()

    assert ".svg" in alloyignore
    assert "dummy_svg.svg" in filtered_codebase

    assert "dummy_md.md" not in filtered_codebase
    assert "dummy_txt.txt" not in filtered_codebase
    assert "dummy_py.py" not in filtered_codebase
    assert "dummy_yml.yml" not in filtered_codebase
    assert "dummy_png.png" not in filtered_codebase
