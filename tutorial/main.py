from fastapi import FastAPI, Body, Query

app = FastAPI()


BOOKS = [
    {'id': 1, 'title': 'Atomic Habits', 'author': 'James Clear', 'category': 'life'},
    {'id': 2, 'title': 'Twisted Love', 'author': 'Ana Huang', 'category': 'romance'},
    {'id': 3, 'title': 'The Midnight Library', 'author': 'Matt Heig', 'category': 'fiction'},

]

@app.get('/')
def welcome_page():
    return {'message': 'Hello World'}


@app.get('/books/')
def list_books(category: str = Query(None)):
    if category:
        return list(filter(lambda x: x.get('category') == category, BOOKS))
    return BOOKS


"""
Picks up the function that is first ahead
"""


@app.get('/books/{book_title}')
def get_book(book_title, category: str = Query(None)):
    response = list(filter(lambda x: x.get('title').casefold() ==
                           book_title.casefold(), BOOKS))
    if category:
        return list(filter(lambda x: x.get('category') == category, response))
    return response


@app.get('/books/The Midnight Library')
def get_book():
    return {'message': 'The Midnight Library'}


def validate_data(data):
    book_ids = list(map(lambda x: x['id'], BOOKS))
    data['id'] = max(book_ids) + 1
    return data, None


@app.post('/books/')
def create_book(body=Body()):
    if body:
        body, message = validate_data(body)
        if message:
            return {'message': message}
        BOOKS.append(body)
        return {'message': 'Book created successfully.'}


def validate_update_data(book_id):
    book_ids = list(map(lambda x: x['id'], BOOKS))
    if int(book_id) not in book_ids:
        message = 'Invalid ID'
        return book_id, message
    book_index = get_book_index(int(book_id))
    return book_index, None


@app.put('/books/{book_id}')
def update_book(book_id, body=Body()):
    if book_id:
        book, message = validate_update_data(book_id)
        if message:
            return {'message': message}
        book.update(body)
        return {'message': book}


def get_book_index(book_id):
    for book in BOOKS:
        if book_id == book.get('id'):
            return book


@app.delete('/books/{book_id}')
def delete_book(book_id):
    if book_id:
        book, message = validate_update_data(book_id)
        if message:
            return {'message': message}
        BOOKS.pop(BOOKS.index(book))
        return {'message': 'Book deleted successfully.'}
