import cambridge
import oxford
import merriamwebster
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

dictList = [{"name": "cambridge", "searchQuery": "https://dictionary.cambridge.org/dictionary/english/"},
            {"name": "oxford", "searchQuery": "https://www.oxfordlearnersdictionaries.com/definition/english/"},
            {"name": "merriamwebster", "searchQuery": "https://www.merriam-webster.com/dictionary/"}]


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


@app.get("/merriamwebster/")
async def merriamWebsterSearch(search: str):
    entries = merriamwebster.wsearch(search)
    if entries == None:
        return {"response": "No result"}
    result = merriamwebster.compileResult(entries)
    return result


@app.get("/")
async def getList():
    return dictList
