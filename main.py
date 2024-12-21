from fastapi import FastAPI
from typing import Optional

app = FastAPI()

items = []

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/items") 
def create_item(item:str):
    items.append(item)
    return item

@app.get("/items/{item_id}") #Useful for querying the items
def get_item(item_id:int) -> str:
    item = items[item_id]
    return item
