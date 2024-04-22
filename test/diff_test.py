from diff_parser import Diff

# checking file
diff = Diff("./v1.0.0...v1.2.0.diff")

print(diff)

for block in diff:
    print(block.type, block.filepath)

# checking with data
with open('./v1.0.0...v1.2.0.diff') as file:
    diff1 = Diff(file.read())

    print(diff1)

    for block in diff1:
        print(block.type, block.filepath)
