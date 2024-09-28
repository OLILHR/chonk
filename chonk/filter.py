import os
from typing import Any, Callable, List, Optional


def get_project_root(start_path: str) -> str:
    """
    Find the project root directory based on common project files.
    """
    current_dir = os.path.abspath(start_path)
    root_indicators = [
        ".git",
        "package.json",
        "pdm.lock",
        "pyproject.toml",
        "setup.py",
        "tox.ini",
    ]

    while current_dir != os.path.dirname(current_dir):
        if any(os.path.exists(os.path.join(current_dir, indicator)) for indicator in root_indicators):
            return current_dir
        current_dir = os.path.dirname(current_dir)

    return start_path


def skip_ignore_list_comments(file_path: str) -> List[str]:
    ignore_list: List[str] = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):  # ignore comments in .chonkignore and DEFAULT_IGNORE_LIST
                ignore_list.append(line)
    return ignore_list


def read_chonkignore(input_path: str, extension_filter: Optional[List[str]]) -> Callable[[str], bool]:
    """
    Excludes all files, extensions and directories specified in .chonkignore, located inside the input directory.
    """
    project_root = get_project_root(input_path)
    chonkignore = os.path.join(project_root, ".chonkignore")
    default_ignore_list = DEFAULT_IGNORE_LIST.copy()

    ignore_list: List[str] = []
    if os.path.exists(chonkignore):
        ignore_list = skip_ignore_list_comments(chonkignore)

    default_ignore_list.extend(ignore_list)

    def exclude_files(file_path: str) -> bool:
        file_path = file_path.replace(os.sep, "/")

        if extension_filter:
            _, file_extension = os.path.splitext(file_path)
            if file_extension[1:] in extension_filter:
                return False

        for pattern in default_ignore_list:
            pattern = pattern.replace(os.sep, "/")
            if pattern.startswith("/"):  # covers absolute paths from the root
                if file_path.startswith(pattern[1:]):
                    return True
            elif pattern.endswith("/"):  # handles directories
                if any(part == pattern[:-1] for part in file_path.split("/")):
                    return True
            elif "*" in pattern:  # handle wildcard patterns
                parts = pattern.split("*")
                if len(parts) == 2:
                    if file_path.startswith(parts[0]) and file_path.endswith(parts[1]):
                        return True
            elif (
                pattern == file_path
                or pattern == os.path.basename(file_path)
                or (pattern.startswith(".") and file_path.endswith(pattern))
            ):
                return True

        return False

    return exclude_files


def filter_extensions(file_path: str, extensions: Optional[List[str]]) -> bool:
    """
    Optional filter to include only certain provided extensions in the consolidated markdown file. If no extensions are
    provided, all files are considered except files, extensions and directories that are explicitly excluded in the
    specified .chonkignore file, located inside the root directory.
    """
    if not extensions:
        return True
    _, file_extension = os.path.splitext(file_path)
    return file_extension[1:] in extensions


def parse_extensions(_csx: Any, _param: Any, value: Optional[List[str]]) -> Optional[List[str]]:
    """
    Converts a comma-separated string of file extensions into a list of individual extensions, which - in turn - is
    parsed to the main function to filter files during the consolidation process.
    """
    if not value:
        return None
    return [ext.strip() for item in value for ext in item.split(",")] if value else None


DEFAULT_IGNORE_LIST: List[str] = [
    ".cache/",
    ".coverage",
    "dist/",
    ".DS_Store",
    ".git",
    ".idea",
    "Thumbs.db",
    ".venv/",
    ".vscode/",
    # JS
    "node_modules/",
    # Python
    "*.pyc",
    # chonk specific files
    ".chonkignore",
    ".chonkignore.example",
    "chonk.md",
]
