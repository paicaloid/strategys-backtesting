from pathlib import Path

import pandas as pd


def read_binance_csv(path: str) -> pd.DataFrame:
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
