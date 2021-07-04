import os
from typing import Optional

import requests
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.params import Depends
from pydantic import BaseModel
from starlette.requests import Request
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

load_dotenv()

OPENWEATHERMAPS_API_KEY = os.getenv("OPENWEATHERMAPS_API_KEY", None)

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


def get_report(
    city: str,
    country: str,
    state: Optional[str] = None,
    units: Optional[str] = "metric",
):
    if state is not None:
        q = f"{city},{state},{country}"
    else:
        q = f"{city},{country}"

    url = f"https://api.openweathermap.org/data/2.5/weather?q={q}&appid={OPENWEATHERMAPS_API_KEY}&units={units}"

    response = requests.get(url)
    response.raise_for_status()

    data = response.json()
    forecast = data["main"]

    return forecast


@app.get("/api/weather")
def weather(location: Location = Depends(), units: Optional[str] = "metric"):
    report = get_report(**location.dict(), units=units)
    return report


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
