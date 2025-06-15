# strategy/performance.py
def get_total_profit(profit_list):
    return sum(profit_list)


def get_win_rate(profit_list):
    win_trades = [p for p in profit_list if p > 0]
    return len(win_trades) / len(profit_list) if profit_list else 0


def get_max_drawdown(profit_list):
    max_drawdown = 0
    peak = 0
    equity = 0
    for p in profit_list:
        equity += p
        peak = max(peak, equity)
        drawdown = peak - equity
        max_drawdown = max(max_drawdown, drawdown)
    return max_drawdown


def get_max_consecutive_loss(profit_list):
    max_loss = 0
    current_loss = 0
    for p in profit_list:
        if p < 0:
            current_loss += p
            max_loss = min(max_loss, current_loss)
        else:
            current_loss = 0
    return max_loss


def summarize_performance(profit_list):
    return {
        "Total Profit": get_total_profit(profit_list),
        "Win Rate": get_win_rate(profit_list),
        "Max Drawdown": get_max_drawdown(profit_list),
        "Max Consecutive Loss": get_max_consecutive_loss(profit_list)
    }
