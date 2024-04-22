import os

class Diff:
    def __init__(self, blocks=None) -> None:
        self.blocks = blocks or list()

    def __iter__(self):
        return iter(self.blocks)
    
    def __len__(self):
        return len(self.blocks)
            
    def __repr__(self) -> str:
        return f"{self.blocks}"


class DiffBlock:
    def __init__(self, filename=None, filepath=None, type="modified", source_hash=None, target_hash=None, content=None) -> None:
        self.filename = filename
        self.filepath = filepath
        self.type = type
        self.source_hash = source_hash
        self.target_hash = target_hash
        self.content = content

    def __repr__(self) -> str:
        return f"{self.source_hash} -> {self.filename} ({self.type}) -> {self.target_hash}"



diffs = [a for a in os.listdir() if a.endswith(".diff")]

blocks : list[str] = []

for diff in diffs:
    with open(diff) as file:
        difflines = file.readlines()
        block = None
        i=1
        for line in difflines:
            if line.startswith("diff --git"):
                if block:
                    blocks.append(block)
                block = [line,]
                i=1
            else:
                # if i>7: # if no need diff file content
                #     break
                block.append(line)

diff = Diff()

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
        
        # getting source and target file
        if line.startswith('index'):
            source, target = line.split()[1].split("..")
            filediff.source_hash = source
            filediff.target_hash = target
        
    diff.blocks.append(filediff)



for d in diff:
    print(d)