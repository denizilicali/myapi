from fastapi import APIRouter, HTTPException
import requests

router = APIRouter()

@router.get("/")
async def convert_currency(from_currency: str, to_currency: str, amount: float):
    url = "https://api.exchangerate.host/latest?base=EUR"
    resp = requests.get(url)
    if resp.status_code != 200:
        raise HTTPException(status_code=500, detail="Currency API unavailable")

    rates = resp.json().get("rates", {})
    from_currency = from_currency.upper()
    to_currency = to_currency.upper()

    if from_currency == "EUR":
        eur_amount = amount
    else:
        from_rate = rates.get(from_currency)
        if from_rate is None:
            raise HTTPException(status_code=400, detail=f"Unsupported currency: {from_currency}")
        eur_amount = amount / from_rate

    to_rate = rates.get(to_currency)
    if to_rate is None:
        raise HTTPException(status_code=400, detail=f"Unsupported currency: {to_currency}")

    converted = eur_amount * to_rate

    return {
        "from": from_currency,
        "to": to_currency,
        "original_amount": amount,
        "converted_amount": round(converted, 4)
    }

