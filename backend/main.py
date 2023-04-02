import base64
import datetime
from typing import Union
from fastapi.middleware.cors import CORSMiddleware

from fastapi import Body, FastAPI
import database
import uvicorn
#from google.cloud import storage

# import socketserver
# import http.server
# import logging
# import cgi

# PORT = 80

# class ServerHandler(http.server.SimpleHTTPRequestHandler):

#     def do_GET(self):
#         logging.error(self.headers)
#         http.server.SimpleHTTPRequestHandler.do_GET(self)

#     def do_POST(self):
#         logging.error(self.headers)
#         form = cgi.FieldStorage(
#             fp=self.rfile,
#             headers=self.headers,
#             environ={'REQUEST_METHOD':'POST',
#                      'CONTENT_TYPE':self.headers['Content-Type'],
#                      })
#         for item in form.list:
#             logging.error(item)
#         http.server.SimpleHTTPRequestHandler.do_GET(self)

#         with open("data.txt", "w") as file:
#             for key in form.keys(): 
#                 file.write(str(form.getvalue(str(key))) + ",")

#if __name__ == "__main__":
db = database.getDatatbase()
PROJECT_ID = "hackforchange-382500"
KEY_FILE_NAME = "mykey.json"
STORAGE_ID = "sllabstorage"
    #uvicorn.run("main:app", host='0.0.0.0', workers=2)

app = FastAPI()
app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
)

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
                  isEdible: bool = Body(...,embed=True),
                  location: str = Body(...,embed=True), 
                  # harvestDate: datetime = Body(...,embed=True), # --> not needed if user does not edit this
                  note: str = Body(...,embed=True)
                  ):
    with open("image.png","rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    # print(f"encoded_string: {encoded_string}")
    # encodedImage = ""
    # aa = imageURL.encode("utf-8")
   # print(aa)
    image_binary = base64.decodebytes(encoded_string)   
    print(f"image_binary: {image_binary}") 
    ret = database.postPinData(db,{"imageUrl":imageURL,"name":name,"isEdible":isEdible,"location":location,"note":note})
    if ret == 1:
        return {"Status Code": "200 OK"}
    else:
        return {"Error"}

@app.post("/addphoto")
async def addPhoto(imageURL: str=Body(...,embed=True)):
    print(imageURL)

# Handler = ServerHandler

# httpd = socketserver.TCPServer(("", PORT), Handler)

# print("serving at port", PORT)
# httpd.serve_forever()

