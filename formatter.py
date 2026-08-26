from dataclasses import asdict

def fotmat_rates(results):
    formatted_results = []
    for result in results:
        formatted_result = {}
        for date, currencies in result.items():
            formatted_result[date] = {}
            for currency, rate in currencies.items():
                formatted_result[date][currency] = asdict(rate)
        formatted_results.append(formatted_result)

    return formatted_result