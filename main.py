import os
from typing import Optional

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.params import Depends
from httpx import AsyncClient
from pydantic import BaseModel
from starlette.requests import Request
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

load_dotenv()

OPENWEATHERMAPS_API_KEY = os.getenv("OPENWEATHERMAPS_API_KEY", None)

app = FastAPI()
templates = Jinja2Templates("templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# CORS
origins = [
    "https://zg9oso.deta.dev/",
    "http://localhost",
    "http://localhost:8080",
    "http://127.0.0.1",
    "http://127.0.0.1:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def index(request: Request):
    message = "Hello World!"

    return templates.TemplateResponse(
        name="index.html",
        context={"request": request},
    )


class Location(BaseModel):
    city: str
    state: Optional[str] = None
    country: str = "US"


async def get_report(
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

    async with AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()

    data = response.json()
    forecast = data["main"]

    return forecast


@app.get("/api/weather")
async def weather(location: Location = Depends(), units: Optional[str] = "metric"):
    report = await get_report(**location.dict(), units=units)
    return report


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
