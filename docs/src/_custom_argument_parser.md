## ClassDef CustomArgumentParser
**CustomArgumentParser**: The function of CustomArgumentParser is to customize the argument parsing behavior by converting certain string values to boolean during argument parsing.

**attributes**:
- add_argument: A method that customizes the behavior of adding arguments by converting specific string values to boolean.

**Code Description**:
The CustomArgumentParser class extends the argparse.ArgumentParser class and overrides the add_argument method to handle boolean values passed as strings. When adding an argument, if the argument type is identified as bool, the method _str2bool is called to convert string representations of boolean values to actual boolean values. This customization allows for more flexible argument handling in the parser.

In the calling situation within the project, the CustomArgumentParser class is utilized in the parse_arguments function defined in the Config.py file. The parse_arguments function creates an instance of CustomArgumentParser and customizes the argument parsing behavior based on the configuration class provided. It iterates over the model fields of the configuration class, adds arguments to the parser with specific configurations, and finally parses the arguments based on the defined settings.

**Note**: Developers can leverage the CustomArgumentParser class to enhance the argument parsing capabilities of their applications, especially when dealing with boolean values passed as strings.

**Output Example**:
An example of using CustomArgumentParser to parse arguments with customized boolean handling:
```python
parser = CustomArgumentParser(description="Custom Argument Parser Example")
parser.add_argument("--enable_feature", type=str, help="Enable a specific feature")
args = parser.parse_args(["--enable_feature", "true"])
print(args.enable_feature)  # Output: True
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
