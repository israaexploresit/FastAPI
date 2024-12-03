from pydantic import BaseModel, Field


class ValidateBook(BaseModel):
    id: int
    title: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0, lt=6)
