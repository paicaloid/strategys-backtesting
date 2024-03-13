import pandas as pd
import talib as ta


def ema_pair(df: pd.DataFrame, fast: int, slow: int) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "fast_ema": ta.EMA(df["close"], timeperiod=fast),
            "slow_ema": ta.EMA(df["close"], timeperiod=slow),
        },
        index=df.index,
    )


def bbands(df: pd.DataFrame, period: int, stdev: float) -> pd.DataFrame:
    upper, _, lower = ta.BBANDS(
        df["close"], timeperiod=period, nbdevup=stdev, nbdevdn=stdev
    )
    return pd.DataFrame(
        {
            "upper": upper,
            "lower": lower,
        },
        index=df.index,
    )


def rsi(df: pd.DataFrame, period: int) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "rsi": ta.RSI(df["close"], timeperiod=period),
        },
        index=df.index,
    )


def trend_ema(df: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "uptrend": df["fast_ema"] > df["slow_ema"],
            "downtrend": df["fast_ema"] < df["slow_ema"],
        },
        index=df.index,
    )


def cross_bbands(df: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "above_bb": df["close"] > df["upper"],
            "below_bb": df["close"] < df["lower"],
        },
        index=df.index,
    )
