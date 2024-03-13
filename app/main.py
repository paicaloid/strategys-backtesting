import glob
from pathlib import Path

import pandas as pd

if __name__ == "__main__":
    file_list = glob.glob("temp/OPUSDT/*.csv")
    file_list = sorted(file_list)

    base_df = pd.read_csv(file_list[0], index_col=0)

    for file in file_list[1:]:
        df = pd.read_csv(file, index_col=0)
        base_df = pd.concat([base_df, df], axis=0)

    base_df.sort_index(inplace=True)
    base_df.to_csv("temp/OPUSDT/OPUSDT-5m.csv")
