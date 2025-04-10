from typing import Annotated
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pymemcache.client import base
from fastapi.templating import Jinja2Templates

client = base.Client(("cache", 11211))


app = FastAPI()

app.mount("/static", StaticFiles(directory="./www/static"), name="static") 

templates = Jinja2Templates(directory="./www")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    name = client.get("name", default=b"World").decode("utf-8")
    return templates.TemplateResponse(request=request, name="index.html", context={"name": name})

@app.post("/signin")
async def signin(name: Annotated[str, Form()]):
    client.set("name", name)
    return {"name": name}
