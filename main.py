import uvicorn
from fastapi import FastAPI
from starlette.requests import Request
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates("templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def index(request: Request):
    message = "Hello World!"

    return templates.TemplateResponse(
        name="index.html",
        context={
            "request": request,
            "message": message,
        },
    )


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
