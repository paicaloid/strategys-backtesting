import pandas as pd
import streamlit as st
from lightweight_charts.widgets import StreamlitChart


def df_line(signal: pd.DataFrame, name: str):
    return pd.DataFrame(
        {
            "time": signal["time"],
            name: signal[name],
        }
    )


st.set_page_config(layout="wide")

chart = StreamlitChart(height=500, width=1200)


chart.grid(vert_enabled=True, horz_enabled=True)

chart.layout(
    background_color="#131722",
    font_family="Trebuchet MS",
    font_size=16,
)

chart.legend(
    visible=True,
    font_family="Trebuchet MS",
    ohlc=True,
    percent=True,
)

df = pd.read_csv("signal.csv")
df.rename(columns={"open_time": "time"}, inplace=True)
chart.set(df)


line30 = chart.create_line(name="ema_30", color="red")
line30.set(df_line(signal=df, name="ema_30"))

line50 = chart.create_line(name="ema_50", color="blue")
line50.set(df_line(signal=df, name="ema_50"))

line_upper = chart.create_line(name="upper", color="gray")
line_upper.set(df_line(signal=df, name="upper"))

line_lower = chart.create_line(name="lower", color="gray")
line_lower.set(df_line(signal=df, name="lower"))


df_entries = df.loc[df["clean_entries"] == True]

for i in range(len(df_entries)):
    chart.marker(
        time=df_entries.iloc[i]["time"],
        text="Entry",
        color="green",
    )

df_exits = df.loc[df["clean_exits"] == True]
for i in range(len(df_exits)):
    chart.marker(
        time=df_exits.iloc[i]["time"],
        text="Exit",
        color="red",
        position="above",
    )


chart.load()
