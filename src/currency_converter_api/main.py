from datetime import datetime
from decimal import Decimal, InvalidOperation
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from httpx import AsyncClient, HTTPError

from currency_converter_api.config import Settings, get_settings

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/convert")
async def convert(from_currency: str, to_currency: str, amount: Decimal, settings: Annotated[Settings, Depends(get_settings)]):
    params: dict = {
        "access_key": settings.exchange_rates.api_key,
        "symbols": ','.join([from_currency, to_currency])
    }

    async with AsyncClient() as client:
        res = await client.get(str(settings.exchange_rates.latest_rates), params=params)
        print(res.url)
        try:
            res.raise_for_status()
            data = res.json()
            rates = data.get("rates")

            from_rate = Decimal(rates.get(from_currency))
            to_rate = Decimal(rates.get(to_currency))

            result_rate = to_rate / from_rate
            return {
                "from": from_currency,
                "to": to_currency,
                "rate": result_rate,
                "result": amount * result_rate,
                "timestamp": datetime.now()
            }

        except (HTTPError, TypeError, InvalidOperation) as err:
            raise HTTPException(status_code=503, detail="Service Unavailable") from err
