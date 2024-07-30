import logging
import os

_logger = logging.getLogger(__name__)


def read_alloyignore(project_root):
    """
    Excludes all files, extensions and directories specified in .alloyignore.
    """
    alloyignore = os.path.join(project_root, ".alloyignore")

    if not os.path.exists(alloyignore):
        return lambda _: False

    ignore_list = []
    with open(alloyignore, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                ignore_list.append(line)  # ignore comments in .alloyignore

    def exclude_files(file_path):
        for pattern in ignore_list:
            if pattern.startswith("/"):  # covers absolute paths from the root
                if file_path.startswith(pattern[1:]):
                    return True
            elif pattern.endswith("/"):  # ignores certain directories
                if any(part == pattern[:-1] for part in file_path.split(os.sep)):
                    return True
            elif pattern.startswith("*."):  # ignores certain file extensions
                if file_path.endswith(pattern[1:]):
                    return True
            elif pattern.endswith("*"):  # ignores certain files with depending on their prefixes
                if os.path.basename(file_path).startswith(pattern[:-1]):
                    return True
            elif pattern in file_path or pattern == os.path.basename(file_path):
                return True
        return False

    return exclude_files


def consolidate(path):
    """
    Consolidates the content of all files from a given directory into a single markdown file.
    """
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    exclude_files = read_alloyignore(project_root)
    codebase = ""

    for root, dirs, files in os.walk(path):
        dirs[:] = [d for d in dirs if not exclude_files(os.path.relpath(str(os.path.join(root, d)), path))]

        for file in files:
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(str(file_path), path)

            if exclude_files(relative_path):
                continue

            _, file_extension = os.path.splitext(file)

            try:
                with open(file_path, "r", encoding="utf-8") as p:
                    content = p.read().rstrip()
            except UnicodeDecodeError as e:
                _logger.error(str(e))
                continue

            codebase += f"\n#### {relative_path}\n\n```{file_extension[1:]}\n{content}\n```\n"

    return codebase
