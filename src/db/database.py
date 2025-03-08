import os
import sqlite3
from sqlite3 import Error

# Veritabanı bağlantısı oluşturma
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f"SQLite bağlantısı başarılı: {db_file}")
        return conn
    except Error as e:
        print(f"Hata: {e}")
    return conn

# Tablo oluşturma
def create_table(conn):
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
    try:
        c = conn.cursor()
        c.execute(create_investments_table)
        c.execute(create_users_table)
        print("Tablolar başarıyla oluşturuldu.")
    except Error as e:
        print(f"Hata: {e}")

# Veritabanı bağlantısını ve tabloyu başlat
def initialize_db():
    database = "data/investment_app.db"
    # data klasörü yoksa oluştur
    os.makedirs(os.path.dirname(database), exist_ok=True)
    conn = create_connection(database)
    if conn is not None:
        create_table(conn)
        print("Veritabanı başarıyla başlatıldı.")
    else:
        print("Hata: Veritabanı bağlantısı kurulamadı!")
    return conn

# Yatırım ekleme
def add_investment(conn, user_id, amount, date, gold_price, quantity):
    sql = """INSERT INTO investments(user_id, amount, date, gold_price, quantity)
             VALUES(?,?,?,?,?)"""
    cur = conn.cursor()
    cur.execute(sql, (user_id, amount, date, gold_price, quantity))
    conn.commit()
    return cur.lastrowid

# Tüm yatırımları getirme
def get_investments(conn, user_id):
    cur = conn.cursor()
    cur.execute("SELECT * FROM investments WHERE user_id = ?", (user_id,))
    rows = cur.fetchall()
    return rows

# Kullanıcı kayıt
def register_user(conn, first_name, last_name, email, phone, username, password):
    sql = """INSERT INTO users(first_name, last_name, email, phone, username, password)
             VALUES(?,?,?,?,?,?)"""
    cur = conn.cursor()
    cur.execute(sql, (first_name, last_name, email, phone, username, password))
    conn.commit()
    return cur.lastrowid

# Kullanıcı giriş
def login_user(conn, username, password):
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cur.fetchone()
    return user