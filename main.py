from typing import Optional

import uvicorn
from fastapi import FastAPI
from fastapi.params import Depends
from pydantic import BaseModel
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


class Location(BaseModel):
    city: str
    state: Optional[str] = None
    country: str = "US"


@app.get("/api/weather")
def weather(location: Location = Depends(), units: Optional[str] = "metric"):
    return {
        "city": location.city,
        "state": location.state,
        "country": location.country,
        "units": units,
    }


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
