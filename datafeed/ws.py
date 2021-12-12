# s: ticker code
# p: last price
# q: quantity of the trade
# dc: daily change percentage
# dd: daily difference price
# t: timestamp in milliseconds

import os
from websocket import create_connection


apikey = os.getenv('APIKEY')
ws_url="wss://ws.eodhistoricaldata.com/ws/crypto?api_token=" + apikey


# Connect to WebSocket API and subscribe to trade feed for XBT/USD and XRP/USD
ws = create_connection(ws_url)
ws.send('{"action": "subscribe", "symbols": "ETH-USD,BTC-USD,ADA-USD"}')

# Infinite loop waiting for WebSocket data
while True:
    print(ws.recv())

