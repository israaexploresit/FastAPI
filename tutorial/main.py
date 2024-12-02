from fastapi import FastAPI

app = FastAPI()


books = [
    {'title': 'Atomic Habits', 'author': 'James Clear'},
    {'title': 'Twisted Love', 'author': 'Ana Huang'},
    {'title': 'The Midnight Library', 'author': 'Matt Heig'},

]

@app.get('/')
def welcome_page():
    return {'message': 'Hello World'}


@app.get('/books/')
def list_books():
    return books
