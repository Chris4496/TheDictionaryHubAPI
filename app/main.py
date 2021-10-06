import cambridge
from fastapi import FastAPI

app = FastAPI()


dictList = ["cambridge"]


# TODO error when search for result HI
@app.get("/cambridge/")
async def cambridgeSearch(search: str):
    entries = cambridge.wsearch(search)
    if entries == None:
        return {"response": "No result"}
    result = cambridge.compileResult(entries)
    return result


@app.get("/")
async def getList():
    return dictList
