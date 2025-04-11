from typing import Annotated
from fastapi import FastAPI, Form, Request, Response
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse
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


@app.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    return FileResponse("./www/about.html")


@app.get("/signin", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(request=request, name="signin.html", context={})


@app.post("/signin")
async def signin(name: Annotated[str, Form()]):
    name = name.strip()
    client.set("name", name)
    headers = {
        "Content-type": "text/html;charset=UTF-8",
        "Content-Length": "0",
        "Location": "/"
    }
    return Response(status_code=303, headers=headers, content="")


@app.get("/notebook")
async def notebook(request: Request):
    return templates.TemplateResponse(request=request, name="notebook.html", context={})
