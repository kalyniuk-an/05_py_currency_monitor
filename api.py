import aiohttp

class PrivetBankAPI:
    URL = "https://api.privatbank.ua/p24api/exchange_rates"

    async def get_rates(self, session: aiohttp.ClientSession, date: str):
        params = {"json": "", "date": date,}
        timeout = aiohttp.ClientTimeout(total=10)

        try:
            async with session.get(self.URL, params=params, timeout=timeout) as response:
                if response.status !=200:
                    print()
                    return {}
                
                return await response.json()
        except aiohttp.ClientError:
            print(f"Помилка мережі під час оримання курсу за {date}")
            return {}
