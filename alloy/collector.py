import logging
import os

from filter import filter_extensions, read_alloyignore

_logger = logging.getLogger(__name__)


def consolidate(path, extensions=None):
    """
    Consolidates the content of all files from a given directory into a single markdown file. Any files, directories and
    extensions specified in .alloyignore are excluded. If optional file extensions are provided, only files with these
    extensions will be included in the consolidated markdown file, regardless of whether they are listed in .alloyignore
    or not.
    """
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    exclude_files = read_alloyignore(project_root)
    codebase = ""

    for root, dirs, files in os.walk(path):
        dirs[:] = [d for d in dirs if not exclude_files(os.path.relpath(str(os.path.join(root, d)), path))]

        for file in files:
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(str(file_path), path)

            if exclude_files(relative_path) or not filter_extensions(file_path, extensions):
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
