from fastapi import FastAPI

app = FastAPI()


BOOKS = [
    {'title': 'Atomic Habits', 'author': 'James Clear'},
    {'title': 'Twisted Love', 'author': 'Ana Huang'},
    {'title': 'The Midnight Library', 'author': 'Matt Heig'},

]

@app.get('/')
def welcome_page():
    return {'message': 'Hello World'}


@app.get('/books/')
def list_books():
    return BOOKS

"""
Picks up the function that is first ahead
"""
@app.get('/books/{book_title}')
def get_book(book_title):
    response = list(map(lambda x: {'message': f"{x.get('title')} by {x.get('author')}"}
                    if x.get('title').casefold() == book_title.casefold()
                    else None, BOOKS))
    return list(filter(lambda x: x is not None, response))


@app.get('/books/The Midnight Library')
def get_book():
    return {'message': 'The Midnight Library'}
