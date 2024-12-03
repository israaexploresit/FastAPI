

class Book:
    id: int
    title: str
    description: str
    rating: int

    def __init__(self, id, title, description, rating):
        self.id = id
        self.title = title
        self.description = description
        self.rating = rating
