## ClassDef Config
**Config**: The function of Config is to define a configuration class that stores the root path of the current file.

**attributes**:
- _root: Path = Path(__file__).parent

**Code Description**: 
The Config class inherits from BaseModel and contains a single attribute "_root" of type Path. The "_root" attribute is initialized with the parent directory path of the current file (__file__).

The purpose of the Config class is to provide a structured way to store and access configuration settings within the application. By defining the root path attribute, the class enables easy reference to the parent directory of the current file, which can be useful for file operations, path resolutions, and other configuration-related tasks.

The class serves as a foundational component for managing configuration data and can be extended to include additional attributes or methods as needed for specific application requirements.

**Note**:
Developers utilizing the Config class should be aware that it primarily focuses on defining configuration-related attributes. The "_root" attribute, in particular, stores the path information related to the current file's parent directory. When working with configuration settings or file paths in the application, accessing the "_root" attribute of an instance of the Config class can provide a convenient way to reference the root path dynamically.
## FunctionDef parse_arguments(config_class)
**parse_arguments**: The function of parse_arguments is to create a custom argument parser based on the provided configuration class, add arguments dynamically for each model field (excluding those starting with an underscore), and parse the arguments to return the parsed values.

**parameters**:
- config_class: Type[Config] - The configuration class from which the model fields are extracted to create arguments for the argument parser.

**Code Description**:
The parse_arguments function takes a configuration class as input and initializes a CustomArgumentParser with a description for configuring application settings. It then iterates over the model fields of the config_class, excluding private fields, and adds arguments to the parser based on the field name, type, default value, and help message. Finally, it parses the arguments and returns the parsed values.

This function is utilized in the project to facilitate the configuration of application settings. By leveraging the parse_arguments function, developers can easily generate an argument parser tailored to the fields of a specific configuration class, allowing for flexible and customizable configuration options.

**Note**:
Developers should ensure that the provided config_class parameter is of type Config to correctly extract the model fields for argument creation. Additionally, the function skips private fields (starting with an underscore) during argument generation to focus on public configuration options.

**Output Example**:
An example of using parse_arguments to parse configuration arguments:
```python
args = parse_arguments(Config)
print(args)
```
## FunctionDef create_config_with_args(config_class, args)
**create_config_with_args**: The function of create_config_with_args is to instantiate a configuration class with arguments, map the arguments to the model fields of the class, and create directories if necessary for Path attributes that do not exist.

**parameters**:
- config_class: Type[Config] (class): The configuration class to instantiate.
- args: Arguments to map to the model fields of the configuration class.

**Code Description**:
The create_config_with_args function takes a configuration class and arguments as input. It creates an instance of the configuration class by mapping the arguments to the model fields of the class. Subsequently, it checks if any Path attribute in the instance requires directory creation if it does not exist. Finally, the function returns the configured instance.

This function is utilized in conjunction with the Config class, where the model_fields attribute is accessed to map arguments to the corresponding fields. The function ensures that the configuration instance is properly initialized with the provided arguments and handles directory creation for Path attributes as needed.

**Note**:
Developers should ensure that the config_class parameter is of type Config or a subclass of Config to instantiate the configuration class correctly. It is essential to provide the necessary arguments that match the model fields of the configuration class to ensure proper initialization.

**Output Example**:
config = create_config_with_args(Config, args)
