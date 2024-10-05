# diff-parser

diff-parser is a Python package for parsing and representing diff files.

Parse a `git diff` data or `.diff` file. Access a list of properties including filenames, filepath, source-hash, target-hash and more for every file changed.

## Installation

You can install `diff-parser` using pip:

```
pip install diff-parser
```


## Usage

To use diff-parser, simply import the required modules and classes:

```python
from diff_parser import Diff

# Example usage:
diff = Diff("path/to/diff/file.diff")
for block in diff:
    print(block.new_filename)           # main.py
    print(block.new_filepath)           # /path/to/main.py
    print(block.old_filename)           # main.py
    print(block.old_filepath)           # /path/to/main.py
    print(block.source_hash)            # abcdef
    print(block.target_hash)            # uvwxyz
    print(block.type)                   # modified
    print(block.file_mode)              # 100644
    print(block.content)                # None (to be implemented)
    print(block.original_line_start)    # 1
    print(block.original_line_count)    # 2
    print(block.modified_line_start)    # 2
    print(block.modified_line_count)    # 3
```

## Contributing
Contributions are welcome! If you find any bugs or have suggestions for improvements, please open an issue on the [GitHub repository](https://github.com/shaiksamad/diff-parser/issues).

## License
This project is licensed under the MIT License - see the [LICENSE](https://github.com/shaiksamad/diff-parser/blob/main/LICENSE) file for details.

