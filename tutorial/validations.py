from pydantic import BaseModel, Field


class ValidateBook(BaseModel):
    id: int
    title: str
    description: str
    rating: int
