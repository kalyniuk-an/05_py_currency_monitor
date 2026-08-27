import asyncio
import sys

from datetime import datetime, timedelta
from pprint import pprint
import aiohttp

from api import PrivatBankAPI
from service import CurrencyService
from formatter import format_rates

async def main():
    if len(sys.argv)<2:
        print("Вкажіть кількість днів.")
        return
    try:
        days = int(sys.argv[1])
    except ValueError:
        print("Кількість деів повина бути числом.")
        return

    if days <1 or days > 10:
        print("Кількість днів повинна бути від 1 до 10.")
        return

    currencies =["EUR", "USD"]
    if len(sys.argv) > 2:
        currencies.extend(sys.argv[2:])

    today = datetime.now()
    api = PrivatBankAPI()
    service = CurrencyService(api)
    async with aiohttp.ClientSession() as session:
        tasks = []
        for day in range(days):
            date = today - timedelta(days=day)
            date_str = date.strftime("%d.%m.%Y")

            rates = service.get_exchange_rates(session, date_str, currencies)
            tasks.append(rates)
        results = await asyncio.gather(*tasks)
    formatted_results = format_rates(results)
    pprint(formatted_results)

if __name__ == "__main__":
    asyncio.run(main())