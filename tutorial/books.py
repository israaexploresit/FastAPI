from fastapi import FastAPI, Path, Query, HTTPException
from tutorial.models import Book
from tutorial.validations import ValidateBook
from tutorial.utils import reform_to_book_class, assign_book_id
from starlette import status

app = FastAPI()

BOOKS = [
    Book(1, 'The Midnight Library', 'Scientific Fiction', 3),
    Book(2, 'Pride and Prejudice', 'Romance set in 80s', 3),
    Book(3, 'Atomic Habits', 'Guide to building habits for lifetime', 5),
    Book(4, 'Ignited Minds', "India's Development Plan", 2),
]


@app.get('/books', status_code=status.HTTP_200_OK)
async def get_books():
    return BOOKS


@app.post('/books', status_code=status.HTTP_201_CREATED)
async def create_book(request_data: ValidateBook):
    request_data = reform_to_book_class(request_data)
    request_data = assign_book_id(request_data, BOOKS)
    BOOKS.append(request_data)


@app.get('/books/{book_id}',status_code=status.HTTP_200_OK)
async def get_book(book_id: int = Path(gt=0)):
    response = list(filter(lambda x: x.id == book_id, BOOKS))
    if not response:
        raise HTTPException(status_code=404, detail='Book not found')
    return response


@app.get('/books/', status_code=status.HTTP_200_OK)
async def fetch_books_by_rating(rating: int = Query(gt=0, lt=6)):
    response = list(filter(lambda x: x.rating == rating, BOOKS))
    return response


@app.put('/books/', status_code=status.HTTP_204_NO_CONTENT)
async def update_book(request_data: ValidateBook):
    is_book_updated = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == request_data.id:
            BOOKS[i] = request_data
            is_book_updated = True
    if not is_book_updated:
        raise HTTPException(status_code=404, detail='Book not found')


@app.delete('/books/{book_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int = Path(gt=0)):
    is_book_deleted = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            is_book_deleted = True
            break
    if not is_book_deleted:
        raise HTTPException(status_code=404, detail='Book not found')
