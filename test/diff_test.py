from diff_parser import Diff

# checking file
diff = Diff("./v1.0.0...v1.2.0.diff")

print(diff)

for block in diff:
    print(block.new_filename, block.new_filepath, block.old_filename, block.old_filepath, block.type, block.source_hash, block.target_hash, block.file_mode)
    for change in block.changes:
        print(change.content, change.original_line_start, change.original_line_count, change.modified_line_start, change.modified_line_count)

# checking with data
with open('./v1.0.0...v1.2.0.diff') as file:
    diff1 = Diff(file.read())

    print(diff1)

    for block in diff1:
        print(block.new_filename, block.new_filepath, block.old_filename, block.old_filepath, block.type, block.source_hash, block.target_hash, block.file_mode)
        for change in block.changes:
            print(change.content, change.original_line_start, change.original_line_count, change.modified_line_start, change.modified_line_count)
