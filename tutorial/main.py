from fastapi import FastAPI

app = FastAPI()


BOOKS = [
    {'title': 'Atomic Habits', 'author': 'James Clear', 'category': 'life'},
    {'title': 'Twisted Love', 'author': 'Ana Huang', 'category': 'romance'},
    {'title': 'The Midnight Library', 'author': 'Matt Heig', 'category': 'fiction'},

]

@app.get('/')
def welcome_page():
    return {'message': 'Hello World'}


@app.get('/books/')
def list_books(category):
    if category:
        return list(filter(lambda x: x.get('category') == category, BOOKS))
    return BOOKS


"""
Picks up the function that is first ahead
"""


@app.get('/books/{book_title}')
def get_book(book_title, category):
    response = list(filter(lambda x: x.get('title').casefold() ==
                           book_title.casefold(), BOOKS))
    if category:
        return list(filter(lambda x: x.get('category') == category, response))
    return response


@app.get('/books/The Midnight Library')
def get_book():
    return {'message': 'The Midnight Library'}
