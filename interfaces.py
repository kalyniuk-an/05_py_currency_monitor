from abc import ABC, abstractmethod

class ExchangeAPI(ABC):
    @abstractmethod
    async def get_rates(self, session, date: str):
        pass