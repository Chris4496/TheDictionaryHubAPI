import cambridge
import oxford
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


dictList = ["cambridge", "oxford"]


@app.get("/cambridge/")
async def cambridgeSearch(search: str):
    entries = cambridge.wsearch(search)
    if entries == None:
        return {"response": "No result"}
    result = cambridge.compileResult(entries)
    return result


@app.get("/oxford/")
async def oxfordSearch(search: str):
    entry = oxford.wsearch(search)
    if entry == None:
        return {"response": "No result"}
    result = oxford.compileResult(entry)
    return result


@app.get("/")
async def getList():
    return dictList
