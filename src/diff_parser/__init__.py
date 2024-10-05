"""
This module provides classes for parsing and representing diff files.

Classes:
- Diff: Represents a diff file containing multiple blocks of changes.
- DiffBlock: Represents a single block of changes in a diff file.

Usage:
The Diff class can be used to parse a diff file and access its individual blocks.
Each DiffBlock represents a single block of changes in the diff file, containing information about the modified file, the type of modification, and the source and target hashes.

Example:
    diff = Diff("path/to/diff/file.diff")
    for block in diff:
        print(block.new_filename)   # main.py
        print(block.new_filepath)   # /path/to/main.py
        print(block.old_filename)   # main.py
        print(block.old_filepath)   # /path/to/main.py
        print(block.source_hash)    # abcdef
        print(block.target_hash)    # uvwxyz
        print(block.type)           # modified
        print(block.file_mode)      # 100644
        print(block.content)        # None (to be implemented)
        print(block.original_line_start) # 1
        print(block.original_line_count) # 2
        print(block.modified_line_start) # 2
        print(block.modified_line_count) # 3
"""

import os
import re
from dataclasses import dataclass


@dataclass
class DiffBlock:
    """
        Represents a single block of change in diff.

        Parameters:
        - filename (str): The name of the file being modified.
        - filepath (str): The path of the file being modified.
        - type (str): The type of modification: 'new', 'deleted', or 'modified'.
        - file_mode (int): The file mode represent the type and permissions of a file in a Unix-like system.
        - source_hash (str): The source hash of the file.
        - target_hash (str): The target hash of the file.
        - content (str): The content of the diff block.
        - original_line_start (int): The starting line number in the old file where the diff block starts.
        - original_line_count (int): The number of lines in the old file that the diff block spans.
        - modified_line_start (int): The starting line number in the new file where the diff block starts.
        - modified_line_count (int): The number of lines in the new file that the diff block spans.

    """
    new_filename = None
    new_filepath = None
    old_filename = None
    old_filepath = None
    type = "modified"
    file_mode = None
    source_hash = None
    target_hash = None
    content = None
    original_line_start = None
    original_line_count = None
    modified_line_start = None
    modified_line_count = None

    def __repr__(self) -> str:
        return f"{self.source_hash} -> {self.old_filename} ({self.type}) -> {self.new_filename} {self.target_hash}"


class Diff:
    """
        Represents a diff file containing multiple blocks of changes.

        Parameters:
        - diff (str): The content of the diff file or the path to the diff file.

        Raises:
        - FileNotFoundError: If the specified file does not exist.

    """

    change_line_pattern = r"@@ -(\d+),?(\d*) \+(\d+),?(\d*) @@"

    def __init__(self, diff: str) -> None:
        if not diff.startswith("diff --git"):
            if not os.path.exists(diff):
                raise FileNotFoundError(diff)
            else:
                with open(diff) as file:
                    diff = file.readlines()
        else:
            diff = diff.splitlines()

        blocks = list()
        block = None

        for line in diff:
            if line.startswith("diff --git"):
                if block:
                    blocks.append(block)
                block = [line, ]
            else:
                block.append(line)
        blocks.append(block)
        filediffs = list()

        for block in blocks:
            filediff = DiffBlock()

            for line in block:
                # getting filename and filepath
                if line.startswith("diff --git"):
                    filenames = line[12:].strip().split(" b/")
                    if len(filenames) == 2:
                        filename = filenames[0]
                        filediff.old_filepath = filename
                        filediff.old_filename = filename.split("/")[-1]

                        filename = f"/{filenames[1]}"
                        filediff.new_filepath = filename
                        filediff.new_filename = filename.split("/")[-1]
                    else:
                        raise Exception(f"Invalid file name {filenames}")

                # getting file diff type - new/deleted/modified
                if "file mode" in line:
                    filediff.type = line.split()[0]

                # getting source and target hash
                if line.startswith('index'):
                    source, target = line.split()[1].split("..")
                    filediff.source_hash = source
                    filediff.target_hash = target

                    # setting file mode for modified files
                    if filediff.file_mode is None:
                        filediff.file_mode = int(line.split()[-1])

                # getting file mode
                if filediff.type in ['new', 'deleted'] and filediff.file_mode is None:
                    filediff.file_mode = int(line.split()[-1])

                # getting change line info
                if line.startswith('@@ '):
                    match = re.match(self.change_line_pattern, line)

                    if match:
                        filediff.original_line_start = int(match.group(1))
                        filediff.original_line_count = int(match.group(2)) if match.group(2) else 1
                        filediff.modified_line_start = int(match.group(3))
                        filediff.modified_line_count = int(match.group(4)) if match.group(4) else 1

            filediffs.append(filediff)

        self.diffs: tuple[DiffBlock] = tuple(filediffs)

    def __iter__(self):
        return iter(self.diffs)

    def __len__(self):
        return len(self.diffs)

    def __repr__(self) -> str:
        return f"{self.diffs}"
