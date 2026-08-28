import asyncio
import aiohttp
from interfaces import ExchangeAPI

class PrivatBankAPI(ExchangeAPI):
    URL = "https://api.privatbank.ua/p24api/exchange_rates"

    async def get_rates(self, session: aiohttp.ClientSession, date: str):
        params = {"json": "", "date": date,}
        timeout = aiohttp.ClientTimeout(total=10)

        try:
            async with session.get(self.URL, params=params, timeout=timeout) as response:
                if response.status !=200:
                    print(f"Помилка API: статус {response.status}, дата {date}")
                    return {}
                
                return await response.json()
        except asyncio.TimeoutError:
            print(f"Перевищено час очікування під чіс отримання курсу валют {date}")
            return {}
        except aiohttp.ClientError:
            print(f"Помилка мережі під час оримання курсу за {date}")
            return {}
