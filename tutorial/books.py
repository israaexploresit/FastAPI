from fastapi import FastAPI
from tutorial.models import Book
from tutorial.validations import ValidateBook
from tutorial.utils import reform_to_book_class, assign_book_id

app = FastAPI()

BOOKS = [
    Book(1, 'The Midnight Library', 'Scientific Fiction', 3),
    Book(2, 'Pride and Prejudice', 'Romance set in 80s', 3),
    Book(3, 'Atomic Habits', 'Guide to building habits for lifetime', 5),
    Book(4, 'Ignited Minds', "India's Development Plan", 2),
]


@app.get('/books')
async def get_books():
    return BOOKS


@app.post('/books')
async def create_book(request_data: ValidateBook):
    request_data = reform_to_book_class(request_data)
    request_data = assign_book_id(request_data, BOOKS)
    BOOKS.append(request_data)


@app.get('/books/{book_id}')
async def get_book(book_id: int):
    response = list(filter(lambda x: x.id == book_id, BOOKS))
    return response


@app.get('/books/')
async def fetch_books_by_rating(rating: int):
    response = list(filter(lambda x: x.rating == rating, BOOKS))
    return response
