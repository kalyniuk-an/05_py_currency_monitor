import asyncio
import logging
from datetime import datetime, timedelta
from aiofile import async_open
from aiopath import AsyncPath

import aiohttp
import names
import websockets

import websockets
from websockets.exceptions import ConnectionClosedOK, ConnectionClosedError

from api import PrivatBankAPI
from service import CurrencyService


logging.basicConfig(level=logging.INFO)

class Server:
    clients = set()

    def __init__(self):
        self.api = PrivatBankAPI()
        self.currency_service = CurrencyService(self.api)

    async def register(self, ws: ConnectionClosedError):
        ws.name = names.get_full_name()
        self.clients.add(ws)

        logging.info(f"{ws.remote_address} connects")

    async def unregister(self, ws: ConnectionClosedError):
        self.clients.remove(ws)
        logging.info(f"{ws.remote_address} disconnects")

    async def send_to_clients(self, message: str):
        if self.clients:
            await asyncio.gather(
                *[
                    client.send(message)
                    for client in self.clients
                ]
            )

    async def ws_handler(self, ws: ConnectionClosedError):
        await self.register(ws)
        try:
            await self.distribute(ws)
        except ConnectionClosedOK:
            pass
        finally:
            await self.unregister(ws)

    async def get_exchange_message(self, days =1):
        today = datetime.now()

        if days < 1 or days > 10:
            return "Кількість днів повинна бути від 1 до 10."

        tasks = []

        async with aiohttp.ClientSession() as session:
            for day in range(days):
                date = today - timedelta(days=day)
                date_str = date.strftime("%d.%m.%Y")
                task = self.currency_service.get_exchange_rates(session, date_str, ["EUR", "USD"])
                tasks.append(task)
            results = await asyncio.gather(*tasks)

        message = ""

        for result in results:
            for date_str, rates in result.items():
                message += f"\n{date_str}\n"
                for currency, rate in rates.items():
                    message += (
                        f"{currency}: "
                        f"купівля {rate.purchase},"
                        f"продаж {rate.sale}\n"
                    )
        return message

    async def distribute(self, ws: ConnectionClosedError):
        async for message in ws:
            command = message.strip().lower()
            if command == "exchange" or command.startswith("exchange "):
                await self.log_exchange(command)
                parts = command.split()
                if len(parts) == 1:
                    days = 1
                else:
                    try:
                        days = int(parts[1])
                    except ValueError:
                        await ws.send("Формат команди: exchange або exchange N")
                        continue
                exchange_message = await self.get_exchange_message(days)
                await self.send_to_clients(exchange_message)
            else:
                await self.send_to_clients(f"{ws.name}: {message}")

    async def log_exchange(self, command):
        log_path = AsyncPath("chat/exchange.log")
        async with async_open(log_path, "a") as file:
            await file.write(
                f"{datetime.now().strftime('%d.%m.%Y %H:%M:%S')} "
                f" - command: {command}\n"
            )


async def main():
    server = Server()
    async with websockets.serve(server.ws_handler, "localhost", 8080):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
