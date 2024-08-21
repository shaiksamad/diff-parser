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
        print(block.filename)    # main.py
        print(block.filepath)   # /path/to/main.py
        print(block.source_hash)# abcdef
        print(block.target_hash)# uvwxyz
        print(block.type)       # modified
        print(block.content)    # None (to be implemented)

"""


import os


class DiffBlock:
    """
        Represents a single block of change in diff.

        Parameters:
        - filename (str): The name of the file being modified.
        - filepath (str): The path of the file being modified.
        - type (str): The type of modification: 'new', 'deleted', or 'modified'.
        - source_hash (str): The source hash of the file.
        - target_hash (str): The target hash of the file.
        - content (str): The content of the diff block.

    """

    def __init__(self, filename=None, filepath=None, type="modified", source_hash=None, target_hash=None, content=None) -> None:
        self.filename = filename
        self.filepath = filepath
        self.type = type
        self.source_hash = source_hash
        self.target_hash = target_hash
        self.content = content

    def __repr__(self) -> str:
        return f"{self.source_hash} -> {self.filename} ({self.type}) -> {self.target_hash}"


class Diff:
    """
        Represents a diff file containing multiple blocks of changes.

        Parameters:
        - diff (str): The content of the diff file or the path to the diff file.

        Raises:
        - FileNotFoundError: If the specified file does not exist.

    """

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
                block = [line,]
            else:
                block.append(line)
        
        filediffs = list()

        for block in blocks:
            filediff = DiffBlock()
            
            for line in block:
                # getting filename and filepath
                if line.startswith("diff --git"):
                    filenames = line[12:].strip().split(" b/")
                    if filenames[0][1:] == filenames[1]:
                        filename = filenames[0]
                        filediff.filepath = filename
                        filediff.filename = filename.split("/")[-1]
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
                
            filediffs.append(filediff)

        self.diffs: tuple[DiffBlock] = tuple(filediffs)

    def __iter__(self):
        return iter(self.diffs)
    
    def __len__(self):
        return len(self.diffs)
            
    def __repr__(self) -> str:
        return f"{self.diffs}"

