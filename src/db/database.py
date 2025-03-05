import sqlite3
from sqlite3 import Error

class Database:
    def __init__(self, db_file="data/investment_app.db"):
        """Veritabanı bağlantısını başlatır."""
        self.db_file = db_file
        self.conn = self.create_connection()

    def create_connection(self):
        """Veritabanı bağlantısını oluşturur."""
        conn = None
        try:
            conn = sqlite3.connect(self.db_file)
            print(f"Veritabanı bağlantısı başarılı: {self.db_file}")
        except Error as e:
            print(f"Veritabanı bağlantısı hatası: {e}")
        return conn

    def create_table(self):
        """Kullanıcılar ve altın alımları için tablolar oluşturur."""
        create_users_table = """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            isim TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            telefon TEXT
        );
        """

        create_alim_table = """
        CREATE TABLE IF NOT EXISTS alımlar (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            tarih TEXT NOT NULL,
            miktar REAL NOT NULL,
            fiyat REAL NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        );
        """

        try:
            cursor = self.conn.cursor()
            cursor.execute(create_users_table)
            cursor.execute(create_alim_table)
            self.conn.commit()
            print("Tablolar başarıyla oluşturuldu.")
        except Error as e:
            print(f"Tablo oluşturma hatası: {e}")

    def add_user(self, isim, email, telefon):
        """Yeni kullanıcı ekler."""
        query = "INSERT INTO users (isim, email, telefon) VALUES (?, ?, ?)"
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, (isim, email, telefon))
            self.conn.commit()
            print(f"Kullanıcı {isim} başarıyla eklendi.")
        except Error as e:
            print(f"Kullanıcı eklerken hata oluştu: {e}")

    def get_user(self, email):
        """Email ile kullanıcıyı getirir."""
        query = "SELECT * FROM users WHERE email = ?"
        cursor = self.conn.cursor()
        cursor.execute(query, (email,))
        user = cursor.fetchone()
        return user

    def add_alim(self, user_id, tarih, miktar, fiyat):
        """Altın alımı kaydeder."""
        query = "INSERT INTO alımlar (user_id, tarih, miktar, fiyat) VALUES (?, ?, ?, ?)"
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, (user_id, tarih, miktar, fiyat))
            self.conn.commit()
            print("Altın alımı başarıyla kaydedildi.")
        except Error as e:
            print(f"Altın alımı eklerken hata oluştu: {e}")

    def get_alim_by_user(self, user_id):
        """Belirli bir kullanıcı için yapılan alımları getirir."""
        query = "SELECT * FROM alımlar WHERE user_id = ?"
        cursor = self.conn.cursor()
        cursor.execute(query, (user_id,))
        alımlar = cursor.fetchall()
        return alımlar
