from turtle import st
from fastapi import Body, FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

class Book:
    def __init__(self, id, author, title, rating):
        self.id = id
        self.author = author
        self.title = title
        self.rating = rating
    
class BookRequest(BaseModel):   ## Inheriting from pydantic BaseModel
    id: int = Field(gt=-1, lt=20)
    author: str = Field(min_length=2)
    title: str = Field(max_length=100)
    rating: int = Field(gt=-1,lt=11)

all_books = [
    Book(1, "David", "Winning and Losing", 7),
    Book(2, "Scott", "Losing and Then Winning", 9),
    Book(1, "Roby", "FastAPI", 8),
    Book(1, "Kobe", "Basketball", 5)
]

@app.get("/books")
async def read_all_books():
    if all_books == []:
        return "There are no books"
    return all_books

@app.post("/create-book")
async def create_book(book_request : BookRequest):
    # print(type(book_request))
    new_book = Book(**book_request.model_dump())
    # print(type(new_book))
    all_books.append(new_book)



## {     "id": 77,     "author": "Bobby",     "title": "Arrakis",     "rating": 10  }
