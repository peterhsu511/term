# strategy/chart.py
import mplfinance as mpf
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import pandas as pd
import numpy as np


def KBar_to_df(KBar_dic):
    df = pd.DataFrame(KBar_dic)
    df.columns = [i.capitalize() for i in df.columns]
    df.set_index("Time", inplace=True)
    return df


def plot_kbar(title, KBar_dic, addplot=[], volume=True):
    df = KBar_to_df(KBar_dic)
    font_path = "C:/Windows/Fonts/msyh.ttc"
    font_prop = fm.FontProperties(fname=font_path)

    fig, _ = mpf.plot(
        df,
        type='candle',
        style='charles',
        volume=volume,
        addplot=addplot,
        returnfig=True,
        title=title
    )
    fig.suptitle(title, fontproperties=font_prop, fontsize=16)
    plt.show()


def plot_strategy(title, KBar_dic, TradeRecord, MA_long=None, MA_short=None):
    df = KBar_to_df(KBar_dic)
    addplot = []

    if MA_long is not None:
        addplot.append(mpf.make_addplot(df[MA_long], color='red'))
    if MA_short is not None:
        addplot.append(mpf.make_addplot(df[MA_short], color='yellow'))

    # 多單紀錄
    buy_orders = [r for r in TradeRecord if r[0] in ['Buy', 'B']]
    buy_pts = [df['Low'][r[2]] * 0.999 if r[2] in df.index else np.nan for r in buy_orders]
    sell_pts = [df['High'][r[4]] * 1.001 if r[4] in df.index else np.nan for r in buy_orders]

    if any(not np.isnan(p) for p in buy_pts):
        addplot.append(mpf.make_addplot(buy_pts, scatter=True, markersize=50, marker='^', color='red'))
        addplot.append(mpf.make_addplot(sell_pts, scatter=True, markersize=50, marker='v', color='blue'))

    # 空單紀錄
    sell_orders = [r for r in TradeRecord if r[0] in ['Sell', 'S']]
    short_pts = [df['High'][r[2]] * 1.001 if r[2] in df.index else np.nan for r in sell_orders]
    cover_pts = [df['Low'][r[4]] * 0.999 if r[4] in df.index else np.nan for r in sell_orders]

    if any(not np.isnan(p) for p in short_pts):
        addplot.append(mpf.make_addplot(short_pts, scatter=True, markersize=50, marker='v', color='green'))
        addplot.append(mpf.make_addplot(cover_pts, scatter=True, markersize=50, marker='^', color='pink'))

    plot_kbar(title, KBar_dic, addplot)
