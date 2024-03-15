from typing import List

import numpy as np
import pandas as pd
import pandas_ta as ta


def ta_change(series: pd.Series, period: int = 1) -> pd.Series:
    return series - series.shift(period)


def calculate_plus_dm(upMove: pd.Series, downMove: pd.Series) -> pd.Series:
    plusDM = pd.Series(np.nan, index=upMove.index)
    positive_move = (upMove > downMove) & (upMove > 0)
    plusDM[positive_move] = upMove[positive_move]
    plusDM = plusDM.fillna(0)
    return plusDM


def calculate_minus_dm(upMove: pd.Series, downMove: pd.Series) -> pd.Series:
    minusDM = pd.Series(np.nan, index=upMove.index)
    negative_move = (downMove > upMove) & (downMove > 0)
    minusDM[negative_move] = downMove[negative_move]
    minusDM = minusDM.fillna(0)
    return minusDM


def true_range_rma(
    high: pd.Series, low: pd.Series, close: pd.Series, period: int = 14
) -> pd.Series:
    tr = ta.true_range(high=high, low=low, close=close)
    trur = ta.rma(close=tr, length=period)
    return trur


def DX(
    plusDM: pd.Series, minusDM: pd.Series, trur: pd.Series, period: int = 14
) -> List[pd.Series]:
    rma_plusDM = ta.rma(close=plusDM, length=period)
    rma_minusDM = ta.rma(close=minusDM, length=period)

    plusDI = 100 * rma_plusDM / trur
    minusDI = 100 * rma_minusDM / trur

    dx_rma = ta.rma(close=abs(plusDI - minusDI) / (plusDI + minusDI), length=period)
    dx = 100 * dx_rma
    return dx, plusDI, minusDI


def ADX(df: pd.DataFrame, period: int = 14) -> pd.DataFrame:
    high = df["high"]
    low = df["low"]
    close = df["close"]
    upMove = ta_change(high)
    downMove = -ta_change(low)
    plusDM = calculate_plus_dm(upMove, downMove)
    minusDM = calculate_minus_dm(upMove, downMove)
    trur = true_range_rma(high, low, close, period)
    dx, plusDI, minusDI = DX(plusDM, minusDM, trur, period)
    adx = ta.rma(close=dx, length=period)
    return pd.DataFrame(
        {"adx": adx, "plusDI": plusDI, "minusDI": minusDI}, index=df.index
    )


def stoch_rsi(
    df: pd.DataFrame,
    stoch_period: int = 14,
    rsi_period: int = 14,
    k_period: int = 3,
    d_period: int = 3,
) -> pd.DataFrame:
    stoch_data = ta.stochrsi(
        close=df["close"],
        length=stoch_period,
        rsi_length=rsi_period,
        k=k_period,
        d=d_period,
    )

    return pd.DataFrame(
        {
            "stoch_k": stoch_data.iloc[:, 0],
            "stoch_d": stoch_data.iloc[:, 1],
        },
        index=df.index,
    )


def ema_pair(
    df: pd.DataFrame, short_period: int = 10, long_period: int = 20
) -> pd.DataFrame:
    short_ema = ta.ema(close=df["close"], length=short_period)
    long_ema = ta.ema(close=df["close"], length=long_period)
    return pd.DataFrame(
        {
            "short_ema": short_ema,
            "long_ema": long_ema,
        },
        index=df.index,
    )
