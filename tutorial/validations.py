from pydantic import BaseModel, Field
from typing import Optional


class ValidateBook(BaseModel):
    id: Optional[int] = Field(description='ID is not a required field',
                              default=None)
    title: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0, lt=6)
