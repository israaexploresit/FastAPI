from tutorial.models import Book


def reform_to_book_class(data):
    return Book(**data.dict())


def assign_book_id(book: Book, BOOKS):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book