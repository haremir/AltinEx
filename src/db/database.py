import sqlite3
from sqlite3 import Error
import logging

class Database:
    def __init__(self, db_file):
        self.db_file = db_file
        self.conn = self.create_connection()
        self.create_tables()
        self.setup_logging()

    def setup_logging(self):
        """Loglama için temel yapılandırma."""
        logging.basicConfig(
            filename="data/database.log",
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )
        logging.info("Veritabanı bağlantısı başlatıldı.")

    def create_connection(self):
        """Veritabanı bağlantısını oluşturur."""
        conn = None
        try:
            conn = sqlite3.connect(self.db_file)
            logging.info(f"SQLite bağlantısı başarılı: {self.db_file}")
        except Error as e:
            logging.error(f"Veritabanı bağlantı hatası: {e}")
        return conn

    def create_tables(self):
        """Tabloları oluşturur."""
        create_investments_table = """
        CREATE TABLE IF NOT EXISTS investments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            date TEXT NOT NULL,
            gold_price REAL NOT NULL,
            quantity REAL NOT NULL
        );
        """
        create_users_table = """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        );
        """
        create_gold_prices_table = """
        CREATE TABLE IF NOT EXISTS gold_prices (
            date TEXT PRIMARY KEY,
            price REAL NOT NULL
        );
        """
        try:
            c = self.conn.cursor()
            c.execute(create_investments_table)
            c.execute(create_users_table)
            c.execute(create_gold_prices_table)
            logging.info("Tablolar başarıyla oluşturuldu.")
        except Error as e:
            logging.error(f"Tablo oluşturma hatası: {e}")

    def add_investment(self, user_id, amount, date, gold_price, quantity):
        """Yatırım bilgilerini veritabanına ekler."""
        sql = """INSERT INTO investments(user_id, amount, date, gold_price, quantity)
                 VALUES(?,?,?,?,?)"""
        try:
            cur = self.conn.cursor()
            cur.execute(sql, (user_id, amount, date, gold_price, quantity))
            self.conn.commit()
            logging.info(f"Yatırım kaydedildi: {amount} ({date})")
        except Error as e:
            logging.error(f"Yatırım kaydetme hatası: {e}")

    def get_investments(self, user_id):
        """Kullanıcıya ait yatırımları getirir."""
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM investments WHERE user_id = ?", (user_id,))
        return cur.fetchall()

    def register_user(self, first_name, last_name, email, phone, username, password):
        """Yeni kullanıcı kaydeder."""
        sql = """INSERT INTO users(first_name, last_name, email, phone, username, password)
                 VALUES(?,?,?,?,?,?)"""
        try:
            cur = self.conn.cursor()
            cur.execute(sql, (first_name, last_name, email, phone, username, password))
            self.conn.commit()
            logging.info(f"Kullanıcı kaydedildi: {username}")
        except Error as e:
            logging.error(f"Kullanıcı kaydetme hatası: {e}")

    def login_user(self, username, password):
        """Kullanıcı girişi kontrolü yapar."""
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        return cur.fetchone()

    def get_user(self, user_id):
        """Kullanıcı bilgilerini getirir."""
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        return cur.fetchone()

    def add_gold_price(self, date, price):
        """Altın fiyatını veritabanına ekler."""
        sql = """INSERT OR REPLACE INTO gold_prices (date, price)
                 VALUES (?, ?)"""
        try:
            cur = self.conn.cursor()
            cur.execute(sql, (date, price))
            self.conn.commit()
            logging.info(f"Altın fiyatı kaydedildi: {price} ({date})")
        except Error as e:
            logging.error(f"Altın fiyatı kaydetme hatası: {e}")

    def get_gold_price(self):
        """Son altın fiyatını getirir."""
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM gold_prices ORDER BY date DESC LIMIT 1")
        return cur.fetchone()

    def close(self):
        """Veritabanı bağlantısını kapatır."""
        if self.conn:
            self.conn.close()
            logging.info("Veritabanı bağlantısı kapatıldı.")

    def update_user(self, user_id, first_name, last_name, email, phone):
        """Kullanıcı bilgilerini günceller."""
        sql = """
        UPDATE users
        SET first_name = ?, last_name = ?, email = ?, phone = ?
        WHERE id = ?
        """
        try:
            cur = self.conn.cursor()
            cur.execute(sql, (first_name, last_name, email, phone, user_id))
            self.conn.commit()
            logging.info(f"Kullanıcı bilgileri güncellendi: {user_id}")
        except Error as e:
            logging.error(f"Kullanıcı güncelleme hatası: {e}")
