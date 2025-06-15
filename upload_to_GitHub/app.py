# app.py
import streamlit as st
import pandas as pd
from order_Lo13 import *
from strategy.backtest import back_test
from strategy.indicators import add_MA, add_RSI, add_Bollinger_Bands, add_MACD
from strategy.optimization import optimize_MA
from strategy.performance import summarize_performance
from strategy.chart import plot_strategy
from strategy.utils import toDictionary
import os
st.set_page_config(layout="wide")
st.title("程式交易策略回測平台")

# --- 資料代號對應表 ---
stock_list = {
    "1522": "kbars_1522_2020-01-01-2024-04-12.xlsx",
    "2330": "kbars_2330_2022-01-01-2024-04-09.xlsx",
    "2356": "kbars_2356_2020-01-01-2024-04-12.xlsx",
    "MXF(小台指)": "kbars_MXF202412_2023-12-21-2024-04-11.xlsx",
    "TXF(台指期)": "kbars_TXF202412_2023-12-21-2024-04-11.xlsx"
}

# --- 選擇預設資料 ---
st.sidebar.header("選擇資料代號")
selected_symbol = st.sidebar.selectbox("請選擇代號：", list(stock_list.keys()))
selected_file = stock_list[selected_symbol]

# 顯示資料代號
st.markdown(f"### 📌 資料代號：`{selected_symbol}`")

# --- 讀取資料 ---
data_folder = "data"
file_path = os.path.join(data_folder, selected_file)
if selected_file.endswith(".xlsx"):
    df = pd.read_excel(file_path)
else:
    df = pd.read_csv(file_path)
#清理資料格式
df = df.drop(columns=[col for col in df.columns if "Unnamed" in col], errors='ignore')
df['time'] = pd.to_datetime(df['time'])
df.set_index("time", inplace=True)

# --- 選擇使用日期範圍 ---
date_min, date_max = df.index.min(), df.index.max()
selected_range = st.sidebar.slider("📆 選擇使用資料區間：", min_value=date_min, max_value=date_max, value=(date_min, date_max))
df = df.loc[selected_range[0]:selected_range[1]]
# 加入技術指標
df = add_MA(df)
df = add_RSI(df)
df = add_Bollinger_Bands(df)
df = add_MACD(df)
df.reset_index(inplace=True)

KBar_dic = toDictionary(df)

# --- 策略設定 ---
st.sidebar.header("策略參數")
long_period = st.sidebar.slider("MA 長期週期", 5, 100, 20)
short_period = st.sidebar.slider("MA 短期週期", 2, long_period - 1, 5)
move_stop = st.sidebar.number_input("移動停損 (點數)", value=10)
order_qty = st.sidebar.number_input("下單口數/股數", value=1)

if st.sidebar.button("執行回測"):
    order = Record(G_spread=0.0001, G_tax=0.003, G_commission=0.001425, isFuture=False)
    capital_curve, final_return = back_test(order, KBar_dic, long_period, short_period, move_stop, order_qty)

    st.success(f"回測完成！總報酬率: {round(final_return*100,2)}%")
    perf = summarize_performance(order.Profit)
    st.write("### 策略績效指標：")
    st.json(perf)

    trade_record = GetTradeRecord(order.TradeRecord)
    st.write("### 策略視覺化：")
    plot_strategy("策略圖", KBar_dic, trade_record, MA_long="MA_long", MA_short="MA_short")

if st.sidebar.button(" 參數最佳化"):
    st.info("請稍候，正在進行最佳化...")
    order = Record(G_spread=0.0001, G_tax=0.003, G_commission=0.001425, isFuture=False)
    best_cap, best_curve, best_param = optimize_MA(order, KBar_dic, range(5, 30), range(2, 20))
    st.success(f"最佳參數：長期 = {best_param[0]}, 短期 = {best_param[1]}，報酬率 = {round((best_cap - 1)*100,2)}%")
