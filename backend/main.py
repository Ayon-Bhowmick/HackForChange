import datetime
from typing import Union

from fastapi import Body, FastAPI
import database

app = FastAPI()
db = database.getDatatbase()

@app.get("/ping")
async def read_root():
    return {"pong"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.get("/pins")
async def getAllPins():
    return database.getAllPinData(db)

@app.post("/addpin")
async def postPin(imageURL: str = Body(...,embed=True),
                  name: str = Body(...,embed=True),
                  isToxic: bool = Body(...,embed=True),
                  location: str = Body(...,embed=True), 
                  # harvestDate: datetime = Body(...,embed=True), # --> not needed if user does not edit this
                  note: str = Body(...,embed=True)
                  ):
    ret = database.postPinData(db,{"imageUrl":imageURL,"name":name,"isToxic":isToxic,"location":location,"note":note})
    if ret == 1:
        return {"Status Code": "200 OK"}
