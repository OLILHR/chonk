import os


def read_alloyignore(project_root, extension_filter):
    """
    Excludes all files, extensions and directories specified in .alloyignore, located inside the root directory.
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

    # pylint: disable=too-many-return-statements
    def exclude_files(file_path):
        file_path = file_path.replace(os.sep, "/")
        if extension_filter:
            _, file_extension = os.path.splitext(file_path)
            if file_extension[1:] in extension_filter:
                return False

        for pattern in ignore_list:
            pattern = pattern.replace(os.sep, "/")
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


def filter_extensions(file_path, extensions):
    """
    Optional filter to include only certain provided extensions in the consolidated markdown file. If no extensions are
    provided, all files are considered except files, extensions and directories that are explicitly excluded in the
    specified .alloyignore file, located inside the root directory.
    """
    if not extensions:
        return True
    _, file_extension = os.path.splitext(file_path)
    return file_extension[1:] in extensions


def parse_extensions(_csx, _param, value):
    """
    Converts a comma-separated string of file extensions into a list of individual extensions, which - in turn - is
    parsed to the main function to filter files during the consolidation process.
    """
    if not value:
        return None
    return [ext.strip() for item in value for ext in item.split(",")]
