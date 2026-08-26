import asyncio
import sys

from datetime import datetime, timedelta
from pprint import pprint
import aiohttp

from api import PrivetBankAPI
from service import CurrencyService

async def main():
    if len(sys.argv)<2:
        print("Вкажіть кількість днів.")
        return
    try:
        days = int(sys.argv[1])
    except ValueError:
        print("Кількість деів повина бути чслом.")

    if days <1 or days > 10:
        print("Кількість днів повинна бути від 1 до 10.")
        return

    today = datetime.now()
    api = PrivetBankAPI()
    service = CurrencyService(api)
    async with aiohttp.ClientSession() as session:
        tasks = []
        for day in range(days):
            date = today - timedelta(days=day)
            date_str = date.strftime("%d.%m.%Y")

            rates = service.get_exchange_rates(session, date_str)
            tasks.append(rates)
        results = await asyncio.gather(*tasks)
    pprint(results)
    # print(f"Потібно отримати курс за {days} днів.")
if __name__ == "__main__":
    asyncio.run(main())