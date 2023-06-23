import json
import requests

def get(url, headers={"accept": "application/json"}):
    """
    Recieves a response from the server and check if valid or not

    Parameters
    ----------
    url : str
        url to query
    headers : dict, default={"accept": "application/json"}
        request headers

    Returns
    -------
    list[dict]
        json parsed response

    Raises
    ------
    Exception 
        If the response has a status code over 400

    Examples
    --------
    >>> url = 'https://api.upbit.com/v1"
    >>> response = get(url)
    """
    response = requests.get(url, headers=headers)
    if response.ok:
        return json.loads(response.text)
    raise Exception(f"Recieved an invalid response with a status code {response.status_code}\n\tpossible reason might be: {json.loads(response.text)['error']['message']}")

def ticker(*tickers : str) -> list[float]:
    """
    Returns a list of a snapshot of each tickers

    Parameters
    ----------
    *tickers : str
        tickers to check prices.

    Returns
    -------
    list[dict]
        list of a snapshot of each tickers

    Raises
    ------
    ?

    Examples
    --------
    >>> ticker("KRW-BTC", "BTC-ETH")
    [{'market': 'KRW-BTC', 
        'trade_date': '20230619', 
        'trade_time': '034046', 
        'trade_date_kst': '20230619', 
        'trade_time_kst': '124046', 
        'trade_timestamp': 1687146046631, 
        'opening_price': 34466000.0, 
        'high_price': 34689000.0, 
        'low_price': 34455000.0, 
        'trade_price': 34617000.0, 
        'prev_closing_price': 34466000.0, 
        'change': 'RISE', 
        'change_price': 151000.0, 
        'change_rate': 0.0043811292, 
        'signed_change_price': 151000.0, 
        'signed_change_rate': 0.0043811292, 
        'trade_volume': 0.03519107, 
        'acc_trade_price': 12778278102.34667, 
        'acc_trade_price_24h': 58018236211.91778, 
        'acc_trade_volume': 369.72559325, 
        'acc_trade_volume_24h': 1672.7662393, 
        'highest_52_week_price': 40610000.0, 
        'highest_52_week_date': '2023-04-12', 
        'lowest_52_week_price': 20700000.0, 
        'lowest_52_week_date': '2022-12-30', 
        'timestamp': 1687146046660
        }, ...]
    """
    url = f"https://api.upbit.com/v1/ticker?markets={'%2C'.join(tickers)}"
    return get(url)

def market(isDetails=False):
    """
    Return a list of exchangeable markets available in UPbit

    Parameters
    ----------
    isDetails : bool, default=False
        isDetails=True shows market_warning info

    Returns
    -------
    list[{'market', 'korean_name', 'english_name' | 'market_warning'}]
        

    Raises
    ------
    ?

    Examples
    --------
    >>> market(True)
    [{'market_warning': 'NONE', 
        'market': 'KRW-BTC',
        'korean_name': '비트코인',
        'english_name': 'Bitcoin'},
     ...
     {'market_warning': 'CAUTION',
        'market': 'KRW-REP',
        'korean_name': '어거',
        'english_name': 'Augur'}]
    """
    url = f"https://api.upbit.com/v1/market/all?isDetails={isDetails}"
    return get(url)

def orderbook(*tickers):
    """
    Return a list of 15 orderbook units per ticker

    Parameters
    ----------
    *ticker : str
        one or more tickers to check orderbooks

    Returns
    -------
    list[{'market', 'timestamp', 'total_ask_size', 'total_bid_size', 'orderbook_units':list[{'ask_price','bid_price','ask_size','bid_size'}]}]
        

    Raises
    ------
    ?

    Examples
    --------
    >>> orderbook("KRW-BTC", "BTC-ETH")
    [...,
        {
        "market": "KRW-BTC",
        "timestamp": 1529910247984,
        "total_ask_size": 8.83621228,
        "total_bid_size": 2.43976741,
        "orderbook_units": [
            {
            "ask_price": 6956000,
            "bid_price": 6954000,
            "ask_size": 0.24078656,
            "bid_size": 0.00718341
            }]
    """
    url = f"https://api.upbit.com/v1/orderbook?{'&'.join([''.join(['markets=',ticker]) for ticker in tickers])}"
    return get(url)

def trades(ticker, to=None, count=None, cursor=None, daysAgo=None):
    """
    return the most recent trade history for the ticker

    Parameters
    ----------
    ticker : str
        ticker name

    to : str:format=('12:59:59' or '125959'), default=None
        time endpoint of inquiring trade history

    count : int, default=None
        number of history to recieve
        1 when None

    cursor : str, default=None
        not exactly sure what it does, but it does something with pagenation
        basically recieves the data after the match
    
    daysAgo : int(1~7), default=None
        number of days past of the inquiring trade history
        basically exists because of the 'to'
        today when default

    Returns
    -------
    list[{'market', 'trade_date_utc', 'trade_time_utc', 'timestamp', 'trade_price', 'trade_volume', 'prev_closing_price', 'chance_price', 'ask_bid'}]
        

    Raises
    ------
    ?

    Examples
    --------
    >>> trades("BTC-ETC")
    [{'market': 'BTC-ETC',
        'trade_date_utc': '2023-06-18',
        'trade_time_utc': '13:06:03',
        'timestamp': 1687093563549,
        'trade_price': 0.00057922,
        'trade_volume': 30.23278356,
        'prev_closing_price': 0.00057548,
        'change_price': 3.74e-06,
        'ask_bid': 'ASK',
        'sequential_id': 16870935635490000}]
    """
    url = f"https://api.upbit.com/v1/trades/ticks?market={ticker}"
    if to:
        url = '&to='.join([url, to])
    if count:
        url = '&count='.join([url, str(count)])
    if cursor:
        url = '&cursor='.join([url, cursor])
    if daysAgo:
        url = '&daysAgo='.join([url, str(daysAgo)])
    return get(url)

def candles(ticker, timescale=None, to=None, count=None, unit=1):
    """
    return the candlestick data

    Parameters
    ----------
    ticker : str
        ticker name

    timescale : str["days" or "months"], default=None
        minutes when default

    to : str:format=(yyyy-MM-dd'T'HH:mm:ss'Z' or yyyy-MM-dd HH:mm:ss), default=None
        time endpoint of inquiring ohlc

    count : int(~200), default=None
        number of candlesticks
        1 when None

    unit : int[ 1, 3, 5, 15, 10, 30, 60, 240 ], default=1
        unit for minutes

    Returns
    -------
    list[{'market', 'candle_date_time_utc', 'candle_date_time_kst', 'opening_price', 'high_price', 'low_price', 'trade_price', 'timestamp', 'candle_acc_trade_price', 'candle_acc_trade_volume', 'unit'}]
        

    Raises
    ------
    ?

    Examples
    --------
    >>> candles("KRW-BTC")
    [{'market': 'KRW-BTC',
        'candle_date_time_utc': '2023-06-18T18:26:00',
        'candle_date_time_kst': '2023-06-19T03:26:00',
        'opening_price': 34800000.0,
        'high_price': 34836000.0,
        'low_price': 34800000.0,
        'trade_price': 34836000.0,
        'timestamp': 1687112792891,
        'candle_acc_trade_price': 3192649.7346,
        'candle_acc_trade_volume': 0.09169878,
        'unit': 1}]
    """
    url = "https://api.upbit.com/v1/candles"
    if not timescale:
        url = "/".join([url, 'minutes', str(unit)])
    else:
        url = "/".join([url, timescale])
    url = ''.join([url, "?market=", ticker])
    if to:
        url = '&to='.join([url, to])
    if count:
        url = '&count='.join([url, str(count)])
    return get(url)

def current_prices(*tickers : str) -> list[float]:
    """
    Return a list of a current price of each tickers

    Parameters
    ----------
    *tickers : str
        tickers to check prices.

    Returns
    -------
    list[float]
        list of price for each ticker

    Raises
    ------
    ?

    Examples
    --------
    >>> ticker("KRW-BTC", "BTC-ETH")
    [34856000.0, 0.0655679]
    """
    return [tk["trade_price"] for tk in ticker(*tickers)]
    