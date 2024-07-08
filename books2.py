import enum
from turtle import st
from typing import Optional         ## For optional in validation
from fastapi import Body, FastAPI, HTTPException, Path, Query
from pydantic import BaseModel, Field
from starlette import status

app = FastAPI()

## CRUD operations i.e., Get, Post etc. are API-endpoints

class Book:
    def __init__(self, id, author, title, rating):
        self.id = id
        self.author = author
        self.title = title
        self.rating = rating
    
class BookRequest(BaseModel):   ## Inheriting from pydantic BaseModel
    # id: Optional[int] = None
    # id: Optional[int] = Field(description="ID is not needed on Create", default= None)
    id: int | None = None
    author: str #= Field(min_length=2)
    title: str #= Field(max_length=100)
    rating: int = Field(gt=-1,lt=11)

all_books = [
    Book(1, "David", "Winning and Losing", 7),
    Book(2, "Scott", "Losing and Then Winning", 9),
    Book(3, "Roby", "FastAPI", 8),
    Book(4, "Kobe", "Basketball", 5)
]

# @app.get("/books")
# async def read_all_books():
#     if all_books == []:
#         return "There are no books"
#     return all_books

@app.post("/create-book", status_code=status.HTTP_201_CREATED)
async def create_book(book_request : BookRequest):
    # print(type(book_request))
    new_book = Book(**book_request.model_dump())
    # print(type(new_book))
    all_books.append(assignbookid(new_book))

@app.get("/books/{book_id}")
async def fetch_book_by_id(book_id:int = Path(gt=0,lt=10)):
    # if book_id < 1 or book_id > len(all_books):
    #     return "Book does not exist in current collection"
    for book in all_books:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Item not found")

@app.get("/books/")
async def fetch_books_by_rating(book_rating:int = Query(default=None, gt=0,lt=11)):
    if book_rating == None:
        return all_books
    else:
        rated = []
        for book in all_books:
            if book.rating == book_rating:
                rated.append(book)
        return rated

@app.put("/books/update_book", status_code= status.HTTP_204_NO_CONTENT)
async def update_book(book:BookRequest):
    for i,b in enumerate(all_books):
        if b.id == book.id:
            all_books[i] = book   
    raise HTTPException(status_code=404)  

@app.delete("/books/{book_id}", status_code = status.HTTP_204_NO_CONTENT)
async def delete_book_by_id(book_id:int =   Path(gt=0,lt=1+len(all_books))):
    ## Will not update other IDs after popping though
    for i, book in enumerate(all_books):
        if book.id == book_id:
            all_books.pop(i)
            break

def assignbookid(book: Book):
    if len(all_books)==0:
        book.id = 1
    else:
        book.id = all_books[-1].id + 1
    return book

## {     "id": 77,     "author": "Bobby",     "title": "Arrakis",     "rating": 10  }
