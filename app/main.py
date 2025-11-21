# app/main.py
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.schemas import ConvertResponse
from app.services import get_rate, get_currency_list

app = FastAPI(title="Currency Converter API")
templates = Jinja2Templates(directory="app/templates")


@app.get("/convert", response_model=ConvertResponse)
async def convert(from_currency: str, to_currency: str, amount: float):
    rate = await get_rate(from_currency, to_currency)
    if rate is None:
        raise HTTPException(status_code=400, detail="Invalid currency pair")

    converted = amount * rate
    return ConvertResponse(from_currency=from_currency,
                           to_currency=to_currency,
                           rate=rate, amount=amount,
                           converted=converted)


@app.get("/currencies")
async def currencies():
    return await get_currency_list()


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
