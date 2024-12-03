from fastapi import FastAPI
from tutorial.models import Book
from tutorial.validations import ValidateBook

app = FastAPI()

BOOKS = [
    Book(1, 'The Midnight Library', 'Scientific Fiction', 3),
    Book(2, 'Pride and Prejudice', 'Romance set in 80s', 4),
    Book(3, 'Atomic Habits', 'Guide to building habits for lifetime', 5),
    Book(4, 'Ignited Minds', "India's Development Plan", 2),
]


@app.get('/books')
async def get_books():
    return BOOKS


@app.post('/books')
async def create_book(body: ValidateBook):
    BOOKS.append(body)