# strategy/optimization.py
import numpy as np
from .utils import GetCumulativeCapitalRate_finalReturn
from .backtest import back_test
from order_Lo13 import Record


def optimize_MA(OrderRecord, KBar_dic, 
                period_range_long, period_range_short, 
                MoveStopLoss=10, Order_Quantity=1, 
                isFuture=False, G_commission=0.001425):

    best_capital = float('-inf')
    best_series = []
    best_params = (0, 0)

    for long_p in period_range_long:
        for short_p in period_range_short:
            if long_p <= short_p:
                continue

            # 重建紀錄器，保證回測不受前次影響
            if isFuture:
                OrderRecord = Record(G_spread=3.628e-4, G_tax=0.00002, G_commission=G_commission, isFuture=True)
            else:
                OrderRecord = Record(G_spread=3.628e-4, G_tax=0.003, G_commission=G_commission, isFuture=False)

            cum_series, final_return = back_test(OrderRecord, KBar_dic, long_p, short_p, MoveStopLoss, Order_Quantity)

            if final_return + 1 > best_capital:
                best_capital = final_return + 1
                best_series = cum_series
                best_params = (long_p, short_p)

    return best_capital, best_series, best_params
