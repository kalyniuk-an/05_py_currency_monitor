import asyncio
import sys

from datetime import datetime, timedelta
from pprint import pprint
import aiohttp

URL = "https://api.privatbank.ua/p24api/exchange_rates"

async def get_exchange_rates(session: aiohttp.ClientSession, date: str):
    params = {"json": "", "date": date}
    timeout = aiohttp.ClientTimeout(total=10)
    try:
        # async with aiohttp.ClientSession() as sesseion:
        async with session.get(URL, params=params, timeout=timeout) as response:
            if response.status != 200:
                print(
                    f"API повернуло помилку"
                    f"{response.status}"
                )
                return{}
                
            data = await response.json()

            result = {}

            for currency in data["exchangeRate"]:
                currency_name = currency["currency"]
                if currency_name in ["EUR", "USD"]:
                    result[currency_name] = {
                        "sale": currency["saleRate"],
                        "purchase": currency["purchaseRate"],
                    }
            return {date: result}
    except aiohttp.ClientError:
        print(
            f"Помилка мережі під час отримання "
            f"курсу за {date}"
            )
        return{}

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
    async with aiohttp.ClientSession() as session:
        tasks = []
        for day in range(days):
            date = today - timedelta(days=day)
            date_str = date.strftime("%d.%m.%Y")

            rates = get_exchange_rates(session, date_str)
            tasks.append(rates)
        results = await asyncio.gather(*tasks)
    pprint(results)
    # print(f"Потібно отримати курс за {days} днів.")
if __name__ == "__main__":
    asyncio.run(main())