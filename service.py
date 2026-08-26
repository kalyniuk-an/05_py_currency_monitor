class CurrencyService:
    def __init__(self, api):
        self.api = api

    async def get_exchange_rates(self, session, date: str, currencies = None):
        if currencies is None:
            currencies = ["EUR", "USD"]

        data = await self.api.get_rates(session, date)
        result ={}

        for currency in data.get("exchangeRate",[]):
            currency_name = currency.get("currency")

            if currency_name in currencies:
                result[currency_name]= {
                    "sale": currency.get("saleRate"),
                    "purchase": currency.get("purchaseRate"),
                }

        return{ date: result}
