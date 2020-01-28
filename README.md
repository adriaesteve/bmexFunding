# fundonebot

bitmex market bot
based on funding rate, with option for hedges in between positions

uses (heavily modified) https://github.com/BitMEX/sample-market-maker framework

### notes:
- cannot build sample-market-maker directly; there are changes to market_maker/market_maker.py, market_maker/bitmex.py, and market_maker/ws/ws_thread.py
- has stops implemented to prevent drastic losses in positions
- not particularly fast latency-wise, wouldn't be wise to adapt to quick trading strategies

### usage:
- setup settings.py from settings_example.py with your api key and secret
	- modify variables in settings.py to desired values
- `pip3 install -r requirements.txt`
- `python3 strat.py`
