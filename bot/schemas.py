"""Pydantic models"""

from pydantic import BaseModel, Field
from typing import Union
from typing_extensions import Annotated


class OptionsTest(BaseModel):    #options in a test
    option_id: int
    option_text: str

class GettedTests(BaseModel):   #the model for processing of getted tests from the api
    ID: int
    Question: str
    Options: list[OptionsTest]
    correct_option_id: int
    explanation: str
    datetime_shown: Annotated[Union[str, None], Field(default=None)]








