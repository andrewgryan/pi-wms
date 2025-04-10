from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles


app = FastAPI()

app.mount("/static", StaticFiles(directory="./www/static"), name="static") 

@app.get("/")
async def index():
    return FileResponse("./www/index.html")
