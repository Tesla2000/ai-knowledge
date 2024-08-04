## ClassDef CustomArgumentParser
**CustomArgumentParser**: The function of CustomArgumentParser is to extend the functionality of the argparse.ArgumentParser class by customizing the behavior of adding arguments, specifically handling boolean types and converting string values to boolean.

**attributes**:
- add_argument(*args, **kwargs): Adds arguments to the parser with customized handling for boolean types.

**Code Description**:
The CustomArgumentParser class inherits from argparse.ArgumentParser and overrides the add_argument method to modify the behavior of adding arguments. When adding an argument, if the argument type is bool, it converts the string values "yes", "true", "t", "y", "1" to True and "no", "false", "f", "n", "0" to False. This customization allows for more flexible handling of boolean arguments during argument parsing.

In the project, the CustomArgumentParser class is utilized to create a specialized argument parser that can handle boolean values more intuitively, enhancing the parsing capabilities of the application settings configuration process.

The parse_arguments function in the Config module utilizes the CustomArgumentParser class to create a custom argument parser tailored to the fields of a configuration class. By leveraging the capabilities of CustomArgumentParser, developers can efficiently parse and process configuration arguments based on the specified field types and values.

**Note**:
Developers can leverage the CustomArgumentParser class to enhance the argument parsing functionality of argparse.ArgumentParser, particularly for handling boolean values in a more user-friendly manner.

**Output Example**:
An example of using CustomArgumentParser to add and parse boolean arguments:
```python
parser = CustomArgumentParser()
parser.add_argument("--enable_feature", type=bool, help="Enable a specific feature.")
args = parser.parse_args()
print(args.enable_feature)
```
### FunctionDef add_argument(self)
**add_argument**: The function of add_argument is to add a new argument to the argument parser. 

**parameters**:
- self: The instance of the class.
- *args: Variable length argument list.
- **kwargs: Arbitrary keyword arguments.

**Code Description**: 
The `add_argument` function first checks if the `type` parameter in the keyword arguments (`kwargs`) is a boolean. If it is a boolean, the function replaces it with the `_str2bool` function from the `CustomArgumentParser` class. This allows the function to correctly handle boolean arguments by converting string representations to boolean values. Finally, the function calls the `add_argument` method from the superclass with the provided arguments and keyword arguments.

This function is utilized in the `parse_arguments` function in the `Config.py` module. In `parse_arguments`, a new argument is added to the argument parser for each model field in the provided `config_class`. The type, default value, and help message for each argument are set based on the attributes of the model fields. 

**Note**: 
- Ensure that the `type` parameter in the keyword arguments represents a valid boolean value to avoid errors.
- The `add_argument` function is essential for dynamically adding arguments to the argument parser based on the configuration class provided.
***
### FunctionDef _str2bool(self, v)
**_str2bool**: The function of _str2bool is to convert a string representation of a boolean value to a boolean type.

**parameters**:
- self: The instance of the class.
- v: The string value to be converted to a boolean.

**Code Description**: 
The `_str2bool` function first checks if the input value is already a boolean. If not, it converts the string representation of a boolean value to a boolean type. It accepts common string representations of boolean values like "yes", "true", "t", "y", "1" for True, and "no", "false", "f", "n", "0" for False. If the input value does not match any of these representations, it raises an `argparse.ArgumentTypeError` with an appropriate message.

In the project, this function is utilized in the `add_argument` method of the `CustomArgumentParser` class. When the `type` parameter in the `kwargs` dictionary is a boolean, it replaces it with the `_str2bool` function. This allows the `add_argument` method to handle boolean arguments correctly by converting string representations to boolean values.

**Note**: 
- Ensure that the input string represents a valid boolean value to avoid raising an error.
- Use this function when dealing with boolean arguments that are provided as strings.

**Output Example**: 
If the input string is "yes", the function will return `True`.
***
