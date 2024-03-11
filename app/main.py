from pathlib import Path

import pandas as pd
from lightweight_charts import Chart


def read_csv(path: str) -> pd.DataFrame:
    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError(f"File {file_path} does not exist")
    df = pd.read_csv(file_path, index_col=0)
    df.drop(columns=["close_time", "ignore"], inplace=True)
    df.index = pd.to_datetime(df.index, unit="ms")

    return df


if __name__ == "__main__":
    chart = Chart()

    df = read_csv("temp/OPUSDT/OPUSDT-5m-2023-02.csv")
    # print(df)
    chart.set(df)

    chart.show(block=True)
