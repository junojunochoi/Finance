import json
import requests

def get_prices(*tickers : str) -> list[float]:
    """
    Return a list of a current price of each tickers
    
    Parameters
    ----------
    *tickers : tickers to check prices.

    Examples
    --------
    >>> get_prices("KRW-BTC", "KRW-ETH")
    [34711000.0, 2272000.0]

    """
    url = f"https://api.upbit.com/v1/ticker?markets={'%2C'.join(tickers)}"

    headers = {"accept": "application/json"}

    response = requests.get(url, headers=headers)

    if response.ok:
        return [ticker['trade_price'] for ticker in json.loads(response.text)]
    else:
        print(f"status code: {response.status_code}\nreason: {response.reason}")
        return response.ok
