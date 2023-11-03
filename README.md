# DevRev OpenAI Tooling

## FunctionInterface Class Documentation

### Overview
The `FunctionInterface` class is a Python class that provides a structured representation of a function. It includes the function's name, description, and parameters. It also provides a method to convert this information into a JSON format.

### Attributes
- `name` (str): The name of the function.
- `description` (str): The docstring of the function.
- `parameters` (dict): A dictionary representing the parameters of the function. Each key is a parameter name, and the value is a dictionary with a single key 'type' and the type of the parameter as the value.
- `json` (str): A JSON representation of the function's information.

### Methods
- `__init__(self, function)`: Initializes the FunctionInterface object with the provided function. It extracts the function's name, docstring, and parameters, and creates a JSON representation of this information.
- `__str__(self)`: Returns the JSON representation of the function's information as a string.
- `__repr__(self)`: Returns the JSON representation of the function's information as a string.
- `to_json(self)`: Returns the JSON representation of the function's information.

## OpenAIHandler Class Documentation

### Overview
The `OpenAIHandler` class is a Python class that serves as a handler for OpenAI's GPT-3 model. It is designed to facilitate the interaction with the model by providing a structured way to send queries and receive responses.

### Attributes
- `api_base` (str): The base URL for the OpenAI API.
- `api_key` (str): The API key for authenticating with the OpenAI API.
- `functions` (list): A list of functions that the model can call.
- `model` (str, optional): The model to use for the chat. Defaults to 'llama-13b-chat'.
- `history` (list): A list to keep track of the conversation history.

### Methods
- `__init__(self, api_base: str, api_key: str, functions: list, model: str = 'llama-13b-chat')`: Initializes the OpenAIHandler object with the provided API base, API key, functions, and model.
- `query(self, message: str) -> Union[dict, str]`: Sends a message to the OpenAI API and returns the response. If the response indicates a function call, it returns the function call as a dictionary. Otherwise, it returns the content of the response as a string.