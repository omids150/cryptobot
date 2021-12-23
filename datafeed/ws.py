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
ws.send('{"action": "subscribe", "symbols": "BTC-USD,ETH-USD,BNB-USD,USDT-USD,SOL-USD,ADA-USD,XRP-USD,DOT-USD,LUNA-USD,DOGE-USD,AVAX-USD,SHIB-USD,CRO-USD,MATIC-USD,WBTC-USD,LTC-USD,UNI-USD,ALGO-USD,TRX-USD,LINK-USD,BCH-USD,XLM-USD,DAI-USD,MANA-USD,AXS-USD,NEAR-USD,FTT-USD,ATOM-USD,VET-USD,FIL-USD,BTCB-USD,EGLD-USD,ICP-USD,ETC-USD,SAND-USD,HBAR-USD,THETA-USD,GALA-USD,XTZ-USD,FTM-USD,LEO-USD,XMR-USD,KLAY-USD,LRC-USD,EOS-USD,GRT-USD,MIONA-USD,BTT-USD,HNT-USD,CAKE-USD"}')

# open a file for write and append
f=open('out-0.json', 'w+')

# Infinite loop waiting for WebSocket data
i = 0
j = 0
while True:
	if(i%100000==0):
		f.close()
		j = j + 1
		f=open('out-'+str(j)+".json", 'w+')
	s=ws.recv()
	print(str(i) +" : " +  s)
	f.write(s)
	f.write('\n')
	f.flush()
	i = i + 1
