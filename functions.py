import json
import inspect

class FunctionInterface:
    def __init__(self, function):
        self.name = function.__name__
        self.description = inspect.getdoc(function)
        self.parameters = {
            'type': 'object',
            'properties': {},
            'required': []
        }
        for parameter in function.__code__.co_varnames:
            param_type = function.__annotations__[parameter].__name__
            self.parameters['properties'][parameter] = {'type': param_type}
        self.json = json.dumps(
            {
                'name': self.name,
                'parameters': self.parameters,
                'description': self.description if self.description else ''
            }
        )
    
    def __str__(self):
        return self.json
    
    def __repr__(self):
        return self.json

    def to_json(self):
        return self.json