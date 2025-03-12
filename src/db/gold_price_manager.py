import requests
from bs4 import BeautifulSoup
from datetime import datetime
from database import Database
import logging

class GoldPriceManager:
    def __init__(self, db_file):
        self.db_file = db_file
        self.db = Database(self.db_file)

    def fetch_gold_price(self):
        """Web scraping ile altın fiyatını çeker ve veritabanına kaydeder."""
        url = "https://www.goldprice.org/"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
        }

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Hata durumunda exception fırlatır
            soup = BeautifulSoup(response.text, 'html.parser')

            # Altın fiyatını sayfadan çekme
            gold_price_tag = soup.find("div", class_="gold-price")
            if gold_price_tag:
                gold_price = gold_price_tag.text.strip().replace(",", "")  # Fiyatı düzelt
                gold_price = float(gold_price)

                date = datetime.now().strftime('%Y-%m-%d')
                self.db.add_gold_price(date, gold_price)  # Veritabanına kaydet
                logging.info(f"Altın fiyatı başarıyla alındı ve kaydedildi: {gold_price} ({date})")
            else:
                logging.warning("Altın fiyatı sayfada bulunamadı.")

        except requests.exceptions.RequestException as e:
            logging.error(f"Web kazıma hatası: {e}")
        except Exception as e:
            logging.error(f"Genel hata: {e}")

    def get_latest_gold_price(self):
        """Veritabanından en son altın fiyatını getirir."""
        result = self.db.get_gold_price()
        if result:
            logging.info(f"En son altın fiyatı: {result[1]} ({result[0]})")
            return result
        else:
            logging.warning("Altın fiyatı veritabanında bulunamadı.")
            return None

    def close(self):
        """Veritabanı bağlantısını kapatır."""
        self.db.close()

# Kullanım:
# GoldPriceManager ile altın fiyatını çekip veritabanına kaydedebilirsiniz.
