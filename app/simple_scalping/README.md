# Simple Scalping
ref: https://medium.com/coinmonks/i-made-codetradings-scalping-strategy-profitable-for-crypto-5916c9b81e6a


## Concept
- 5-minute timeframe on EUR/USD
- Uptrend: EMA(30) > EMA(50) for the latest 7 candles
- Downtrend: EMA(30) < EMA(50) for the latest 7 candles
- Buy: Uptrend & Close < lower Bollinger Band(15, std=1.5)
- Sell: Downtrend & Close > upper Bollinger Band(15, std=1.5)
- Close position using stop loss and take profit (using 1.1*ATR(7) and RRR=1.5)