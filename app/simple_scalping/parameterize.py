from pathlib import Path

import numpy as np
import pandas as pd
import vectorbtpro as vbt
from indicators import bbands, cross_bbands, ema_pair, rsi, trend_ema


def read_csv(path: str) -> pd.DataFrame:
    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError(f"File {file_path} does not exist")
    df = pd.read_csv(file_path, index_col=0)
    df.drop(
        columns=[
            "close_time",
            "ignore",
            "quote_volume",
            "count",
            "taker_buy_volume",
            "taker_buy_quote_volume",
        ],
        inplace=True,
    )
    df.index = pd.to_datetime(df.index, unit="ms")

    return df


def generate_signals(df: pd.DataFrame) -> pd.DataFrame:
    long_entries = df["below_bb"] & df["uptrend"] & (df["rsi"] <= 50)
    short_entries = df["above_bb"] & df["downtrend"] & (df["rsi"] >= 50)

    return pd.DataFrame(
        {
            "long_entries": long_entries,
            "short_entries": short_entries,
        },
        index=df.index,
    )


@vbt.parameterized(merge_func="concat")
def tuning(
    data: pd.DataFrame,
    fast_ema: int,
    slow_ema: int,
    bb_period: int,
    bb_stdev: float,
    rsi_period: int,
) -> pd.DataFrame:
    df_ema = ema_pair(df=data, fast=fast_ema, slow=slow_ema)
    df_bb = bbands(df=data, period=bb_period, stdev=bb_stdev)
    df_rsi = rsi(df=data, period=rsi_period)
    df = pd.concat([data, df_ema, df_bb, df_rsi], axis=1)

    df_trend = trend_ema(df=df)
    df_cross = cross_bbands(df=df)
    df = pd.concat([df, df_trend, df_cross], axis=1)

    df_signal = generate_signals(df=df)
    df = pd.concat([df, df_signal], axis=1)
    df.dropna(inplace=True)

    long_entries = df["long_entries"].vbt.signals.clean()
    short_entries = df["short_entries"].vbt.signals.clean()

    pf = vbt.Portfolio.from_signals(
        close=df["close"],
        long_entries=long_entries,
        short_entries=short_entries,
        init_cash=1000,
        fees=0.001,
        sl_stop=0.1,
        tp_stop=0.2,
    )

    return pf.sharpe_ratio


def main():
    df = read_csv(path="temp/OPUSDT/OPUSDT-5m.csv")
    print(df)
    perf = tuning(
        data=df,
        fast_ema=vbt.Param(np.arange(5, 50), condition="x < slow_ema"),
        slow_ema=vbt.Param(np.arange(5, 50)),
        bb_period=50,
        bb_stdev=3,
        rsi_period=14,
    )
    print(perf.sort_values(ascending=False))


if __name__ == "__main__":
    main()
