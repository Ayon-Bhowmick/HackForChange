from typing import Union

from fastapi import FastAPI
import database

app = FastAPI()
db = database.getDatatbase()

@app.get("/ping")
def read_root():
    return {"pong"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.get("/pins")
def getAllPins():
    print(database.getAllPinData(db))
    return database.getAllPinData(db)


# Routes
# 
# 
# 
# 
# 
# 
