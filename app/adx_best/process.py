import pandas as pd
import vectorbtpro as vbt
from indicators import ADX, ema_pair, stoch_rsi
from read_file import read_binance_csv


def generate_signals(df: pd.DataFrame, adx_level: int, adx_diff: float) -> pd.DataFrame:
    is_open_long = (
        (df["plusDI"] > df["minusDI"])
        & (df["plusDI"] > adx_level)
        & (df["plusDI"] - df["minusDI"] > adx_diff)
    )
    is_open_short = (
        (df["minusDI"] > df["plusDI"])
        & (df["minusDI"] > adx_level)
        & (df["minusDI"] - df["plusDI"] > adx_diff)
    )

    is_close_long = (df["plusDI"] < df["minusDI"]) | (df["plusDI"] < adx_level)
    is_close_short = (df["minusDI"] < df["plusDI"]) | (df["minusDI"] < adx_level)

    is_above_long_ema = df["close"] > df["long_ema"]
    is_below_long_ema = df["close"] < df["long_ema"]
    is_above_short_ema = df["close"] > df["short_ema"]
    is_below_short_ema = df["close"] < df["short_ema"]

    is_trend_up = df["stoch_k"] > df["stoch_d"]
    is_trend_down = df["stoch_k"] < df["stoch_d"]

    long_entries = is_open_long & is_above_long_ema & is_above_short_ema & is_trend_up
    short_entries = (
        is_open_short & is_below_long_ema & is_below_short_ema & is_trend_down
    )
    long_exits = is_close_long | is_below_long_ema
    short_exits = is_close_short | is_above_long_ema

    return pd.DataFrame(
        {
            "long_entries": long_entries,
            "short_entries": short_entries,
            "long_exits": long_exits,
            "short_exits": short_exits,
        },
        index=df.index,
    )


def backtest(df: pd.DataFrame) -> pd.DataFrame:
    df = df["2023-12-01 02:00:00":"2023-12-04"]
    # long_entries, long_exits = df["long_entries"].vbt.signals.clean(df["long_exits"])
    # short_entries, short_exits = df["short_entries"].vbt.signals.clean(
    #     df["short_exits"]
    # )
    long_entries, long_exits = df["long_entries"], df["long_exits"]
    short_entries, short_exits = df["short_entries"], df["short_exits"]
    pf = vbt.Portfolio.from_signals(
        close=df["close"],
        long_entries=long_entries,
        long_exits=long_exits,
        short_entries=short_entries,
        short_exits=short_exits,
        init_cash=100,
        fees=0.04 / 100,
        sl_stop=0.03,
        tp_stop=0.06,
        tsl_th=0.02,
        tsl_stop=0.01,
    )
    print(pf.stats())


def main():
    df = read_binance_csv(path="temp/OPUSDT_1H/OPUSDT-1h.csv")
    df_adx = ADX(df=df)
    df_stoch = stoch_rsi(df=df)
    df_ema = ema_pair(df=df, short_period=10, long_period=20)

    df = pd.concat([df, df_adx, df_stoch, df_ema], axis=1)
    df.dropna(inplace=True)

    df_signals = generate_signals(df=df, adx_level=20, adx_diff=1)

    df = pd.concat([df, df_signals], axis=1)
    backtest(df=df)


if __name__ == "__main__":
    main()
