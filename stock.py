import urllib.request

def check_stock_quote(stock_code):
    
    url = "https://stooq.com/q/l/?s=<stock_code>&f=sd2t2ohlcv&h&e=csv"
    url = url.replace("<stock_code>", stock_code)
    
    try:
        response = urllib.request.urlopen(url)
    except Exception:
        bot_msg = "I could not get the stock quote now. Please, try again later."
    else:
        lines = [l.decode('utf-8') for l in response.readlines()]
        stock_info = lines[1].split(",")
        if stock_info[1] == "N/D":
            bot_msg = stock_code.upper() + " quote not found."
        else:
            bot_msg = stock_info[0] + " quote is $" + stock_info[3] + " per share"

    return bot_msg