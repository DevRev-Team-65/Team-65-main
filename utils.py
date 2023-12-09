import json
from typing import List
from pydantic import BaseModel, Field, ValidationError, validator

class ArgumentData(BaseModel):
    argument_name: str
    argument_value: str

class ToolData(BaseModel):
    tool_name: str
    arguments: List[ArgumentData]

class OutputParser(BaseModel):
    tools: List[ToolData]

    @validator('tools', each_item=True)
    def validate_arguments(cls, value):
        if 'arguments' in value:
            for argument in value['arguments']:
                if 'argument_value' in argument and isinstance(argument['argument_value'], list):
                    raise ValueError('argument_value should be a string, not a list')
        return value

    @classmethod
    def parse_and_validate(cls, json_str: str):
        json_data = json.loads(json_str)
        return cls(tools=json_data)