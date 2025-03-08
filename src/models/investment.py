from src.db.database import get_investments

# Güncel altın fiyatını al (API veya sabit bir değer)
def get_gold_price():
    # Burada API çağrısı yapılabilir. Şimdilik sabit bir değer döndürelim.
    return 3500  # Örnek: 1200 TL/gram

# Kar/zarar hesapla
def calculate_profit(conn):
    investments = get_investments(conn)
    total_profit = 0
    current_gold_price = get_gold_price()  # Güncel altın fiyatı
    for investment in investments:
        amount = investment[1]
        quantity = investment[4]
        current_value = quantity * current_gold_price
        profit = current_value - amount
        total_profit += profit
    return total_profit

def get_financial_summary(conn, user_id):
    investments = get_investments(conn, user_id)
    total_investment = sum(inv[2] for inv in investments)
    total_quantity = sum(inv[5] for inv in investments)
    current_value = total_quantity * get_gold_price()
    total_profit = current_value - total_investment
    return {
        "total_investment": total_investment,
        "total_quantity": total_quantity,
        "current_value": current_value,
        "total_profit": total_profit
    }

def filter_investments(investments, start_date=None, end_date=None, profit_filter=None):
    filtered = investments
    if start_date:
        filtered = [inv for inv in filtered if inv[2] >= start_date]
    if end_date:
        filtered = [inv for inv in filtered if inv[2] <= end_date]
    if profit_filter == "Kar":
        filtered = [inv for inv in filtered if (inv[4] * get_gold_price()) > inv[1]]
    elif profit_filter == "Zarar":
        filtered = [inv for inv in filtered if (inv[4] * get_gold_price()) < inv[1]]
    return filtered