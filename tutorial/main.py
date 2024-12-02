from fastapi import FastAPI

app = FastAPI()


@app.get('/')
def welcome_page():
    return {'message': 'Hello World'}
