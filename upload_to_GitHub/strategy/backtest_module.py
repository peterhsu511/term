# strategy/backtest.py
import numpy as np
from talib.abstract import SMA
from .utils import GetOpenInterest, GetCumulativeCapitalRate_finalReturn


def back_test(OrderRecord, KBar_dic, LongMAPeriod=10, ShortMAPeriod=2, MoveStopLoss=10, Order_Quantity=1):
    # 計算技術指標
    KBar_dic['MA_long'] = SMA(KBar_dic, timeperiod=int(LongMAPeriod))
    KBar_dic['MA_short'] = SMA(KBar_dic, timeperiod=int(ShortMAPeriod))

    for n in range(1, len(KBar_dic['time']) - 1):
        if not np.isnan(KBar_dic['MA_long'][n - 1]):
            if GetOpenInterest(OrderRecord.OpenInterestQty) == 0:
                if KBar_dic['MA_short'][n - 1] <= KBar_dic['MA_long'][n - 1] and KBar_dic['MA_short'][n] > KBar_dic['MA_long'][n]:
                    OrderRecord.Order('Buy', KBar_dic['product'][n + 1], KBar_dic['time'][n + 1], KBar_dic['open'][n + 1], Order_Quantity)
                    OrderPrice = KBar_dic['open'][n + 1]
                    StopLossPoint = OrderPrice - MoveStopLoss
                elif KBar_dic['MA_short'][n - 1] >= KBar_dic['MA_long'][n - 1] and KBar_dic['MA_short'][n] < KBar_dic['MA_long'][n]:
                    OrderRecord.Order('Sell', KBar_dic['product'][n + 1], KBar_dic['time'][n + 1], KBar_dic['open'][n + 1], Order_Quantity)
                    OrderPrice = KBar_dic['open'][n + 1]
                    StopLossPoint = OrderPrice + MoveStopLoss

            elif GetOpenInterest(OrderRecord.OpenInterestQty) > 0:
                if KBar_dic['product'][n + 1] != KBar_dic['product'][n]:
                    OrderRecord.Cover('Sell', KBar_dic['product'][n], KBar_dic['time'][n], KBar_dic['close'][n], GetOpenInterest(OrderRecord.OpenInterestQty))
                elif KBar_dic['close'][n] - MoveStopLoss > StopLossPoint:
                    StopLossPoint = KBar_dic['close'][n] - MoveStopLoss
                elif KBar_dic['close'][n] < StopLossPoint:
                    OrderRecord.Cover('Sell', KBar_dic['product'][n + 1], KBar_dic['time'][n + 1], KBar_dic['open'][n + 1], GetOpenInterest(OrderRecord.OpenInterestQty))

            elif GetOpenInterest(OrderRecord.OpenInterestQty) < 0:
                if KBar_dic['product'][n + 1] != KBar_dic['product'][n]:
                    OrderRecord.Cover('Buy', KBar_dic['product'][n], KBar_dic['time'][n], KBar_dic['close'][n], -GetOpenInterest(OrderRecord.OpenInterestQty))
                elif KBar_dic['close'][n] + MoveStopLoss < StopLossPoint:
                    StopLossPoint = KBar_dic['close'][n] + MoveStopLoss
                elif KBar_dic['close'][n] > StopLossPoint:
                    OrderRecord.Cover('Buy', KBar_dic['product'][n + 1], KBar_dic['time'][n + 1], KBar_dic['open'][n + 1], -GetOpenInterest(OrderRecord.OpenInterestQty))

    return GetCumulativeCapitalRate_finalReturn(OrderRecord.Capital_rate)
