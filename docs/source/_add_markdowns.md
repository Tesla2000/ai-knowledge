## FunctionDef add_markdowns
**add_markdowns**: The function of add_markdowns is to add references to Markdown files in specified reStructuredText files.

**parameters**:
- markdown_file_path: A Path object representing the path to the Markdown file.
- source_path: A Path object representing the source directory containing reStructuredText and Markdown files.

**Code Description**:
The add_markdowns function first defines an inner function _conv2ref, which converts the Markdown file path to a relative reference. It then sets the source_path to the "docs/source" directory. The function iterates over all .rst files in the source_path, excluding "index.rst" and "modules.rst". For each file, it reads the content, splits it based on the additional_documents_header, and retrieves the content before and after the header. It determines the documentation path based on the file name and searches for Markdown files in the corresponding directory. The function then generates additional_docs by mapping the _conv2ref function to the Markdown files, formats the updated content with the additional documents header and the references to Markdown files, and writes the modified content back to the file.

**Note**:
- Ensure that the additional_documents_header is correctly defined before using this function.
- Make sure that the source_path directory structure matches the expected layout for referencing Markdown files.

**Output Example**:
If the original content of a .rst file is:
```
Some content here.
.. additional_documents_header
```
and there are Markdown files "file1.md" and "file2.md" in the "docs/source/subdirectory" directory, the updated content after running add_markdowns may look like:
```
Some content here.
.. additional_documents_header
   file1
   file2
```
### FunctionDef _conv2ref(markdown_file_path)
**_conv2ref**: The function of _conv2ref is to convert the input markdown file path to a relative path from a specified source path without a file extension.

**parameters**:
- markdown_file_path: The path to the markdown file.
  
**Code Description**:
The _conv2ref function takes a markdown file path as input and returns the relative path of the file from a specified source path without the file extension. It uses the relative_to method to get the relative path from the source path and the with_suffix method to remove the file extension.

**Note**:
Ensure that the source_path variable is defined before calling this function to get the correct relative path.

**Output Example**:
If markdown_file_path = "/path/to/file/example.md" and source_path = "/path/to", the function will return "file/example".
***
