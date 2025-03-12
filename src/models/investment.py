class Investment:
    def __init__(self, db):
        self.db = db

    def get_gold_price(self):
        # API çağrısı veya sabit bir değer
        return 3500  # Örnek: 3500 TL/gram

    def calculate_investment_profit(self, investment):
        """
        Tek bir yatırımın kar/zarar durumunu hesaplar.
        :param investment: Yatırım bilgileri (amount, date, gold_price, quantity)
        :return: Yatırımın bugünkü değeri, kar/zarar miktarı ve oranı
        """
        amount = investment[2]  # Yatırım miktarı
        quantity = investment[5]  # Alınan altın miktarı
        current_value = quantity * self.get_gold_price()  # Bugünkü değer
        profit = current_value - amount  # Kar/zarar miktarı
        profit_ratio = (profit / amount) * 100 if amount != 0 else 0  # Kar/zarar oranı
        return current_value, profit, profit_ratio

    def get_individual_investment_analysis(self, user_id):
        """
        Kullanıcının her bir yatırımını ayrı ayrı analiz eder.
        :param user_id: Kullanıcı ID'si
        :return: Her bir yatırımın analiz sonuçları
        """
        investments = self.db.get_investments(user_id)
        analysis = []
        for inv in investments:
            current_value, profit, profit_ratio = self.calculate_investment_profit(inv)
            analysis.append({
                "id": inv[0],  # Yatırım ID'si
                "date": inv[3],  # Yatırım tarihi
                "amount": inv[2],  # Yatırım miktarı
                "gold_price": inv[4],  # Alınma kuru (TL/gram)
                "quantity": inv[5],  # Alınan altın miktarı (gram)
                "current_value": current_value,  # Bugünkü değer
                "profit": profit,  # Kar/zarar miktarı
                "profit_ratio": profit_ratio  # Kar/zarar oranı
            })
        return analysis

    def get_total_investment_analysis(self, user_id):
        """
        Kullanıcının tüm yatırımlarını birleştirerek genel analiz yapar.
        :param user_id: Kullanıcı ID'si
        :return: Toplam yatırım analizi
        """
        investments = self.db.get_investments(user_id)
        total_investment = sum(inv[2] for inv in investments)  # Toplam yatırım miktarı
        total_quantity = sum(inv[5] for inv in investments)  # Toplam altın miktarı
        current_value = total_quantity * self.get_gold_price()  # Bugünkü toplam değer
        total_profit = current_value - total_investment  # Toplam kar/zarar
        total_profit_ratio = (total_profit / total_investment) * 100 if total_investment != 0 else 0  # Toplam kar/zarar oranı
        return {
            "total_investment": total_investment,
            "total_quantity": total_quantity,
            "current_value": current_value,
            "total_profit": total_profit,
            "total_profit_ratio": total_profit_ratio
        }