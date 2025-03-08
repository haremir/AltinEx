import sys
import os

# Proje kök dizinini sys.path'e ekle
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from src.db.database import initialize_db, register_user, login_user, add_investment, get_investments
from src.models.investment import calculate_profit, get_gold_price, get_financial_summary, filter_investments
from src.utils.helper import format_date
import datetime
import pandas as pd


# Veritabanını başlat
conn = initialize_db()
if conn is None:
    st.error("Veritabanı bağlantısı kurulamadı! Lütfen veritabanını kontrol edin.")
    st.stop()

# Kullanıcı giriş/kayıt formu
st.sidebar.title("Giriş / Kayıt")
choice = st.sidebar.selectbox("Seçim Yapın", ["Giriş Yap", "Kayıt Ol"])

if choice == "Kayıt Ol":
    st.sidebar.subheader("Yeni Hesap Oluştur")
    new_username = st.sidebar.text_input("Kullanıcı Adı")
    new_password = st.sidebar.text_input("Şifre", type="password")
    if st.sidebar.button("Kayıt Ol"):
        if new_username and new_password:
            register_user(conn, new_username, new_password)
            st.sidebar.success("Hesabınız başarıyla oluşturuldu!")
        else:
            st.sidebar.warning("Kullanıcı adı ve şifre giriniz.")

elif choice == "Giriş Yap":
    st.sidebar.subheader("Hesabınıza Giriş Yapın")
    username = st.sidebar.text_input("Kullanıcı Adı")
    password = st.sidebar.text_input("Şifre", type="password")
    if st.sidebar.button("Giriş Yap"):
        user = login_user(conn, username, password)
        if user:
            st.sidebar.success(f"Hoş geldiniz, {user[1]}!")
            st.session_state["logged_in"] = True
            st.session_state["user_id"] = user[0]
        else:
            st.sidebar.error("Geçersiz kullanıcı adı veya şifre!")

# Kullanıcı giriş yapmadan erişimi engelle
if not st.session_state.get("logged_in"):
    st.warning("Lütfen giriş yapın veya kayıt olun.")
    st.stop()

# Ana uygulama
st.title("ALTINEX - Altın Yatırım Takip Uygulaması")

# Genel finansal özet
st.subheader("Genel Finansal Özet")
summary = get_financial_summary(conn, st.session_state["user_id"])
st.write(f"""
**Toplam Yatırım:** {summary["total_investment"]:.2f} TL  
**Toplam Altın Miktarı:** {summary["total_quantity"]:.2f} gram  
**Güncel Değer:** {summary["current_value"]:.2f} TL  
**Toplam Kar/Zarar:** {summary["total_profit"]:.2f} TL
""")

# Görsel öğeler
profit_ratio = summary["total_profit"] / summary["total_investment"] if summary["total_investment"] > 0 else 0
st.progress(profit_ratio)

# Yeni yatırım ekleme
st.subheader("Yeni Yatırım Ekle")
amount = st.number_input("Yatırım Miktarı (TL)", min_value=0.0)
date = st.date_input("Yatırım Tarihi", datetime.date.today())

if st.button("Yatırım Ekle"):
    if amount > 0:
        gold_price = get_gold_price()  # Güncel altın fiyatını al
        quantity = amount / gold_price  # Alınan altın miktarını hesapla
        add_investment(conn, st.session_state["user_id"], amount, format_date(date), gold_price, quantity)
        st.success("Yatırım başarıyla eklendi!")
    else:
        st.error("Yatırım miktarı 0 TL'den fazla olmalıdır!")

# Filtreleme seçenekleri
st.sidebar.subheader("Filtreleme Seçenekleri")
start_date = st.sidebar.date_input("Başlangıç Tarihi", datetime.date.today())
end_date = st.sidebar.date_input("Bitiş Tarihi", datetime.date.today())
profit_filter = st.sidebar.selectbox("Kar/Zarar Durumu", ["Tümü", "Kar", "Zarar"])

# Yatırımları filtrele
filtered_investments = filter_investments(
    get_investments(conn, st.session_state["user_id"]),
    start_date=format_date(start_date),
    end_date=format_date(end_date),
    profit_filter=profit_filter if profit_filter != "Tümü" else None
)

# Detaylı analiz
st.subheader("Detaylı Analiz")
for inv in filtered_investments:
    current_value = inv[4] * get_gold_price()
    profit = current_value - inv[1]
    st.write(f"""
    **Tarih:** {inv[2]}  
    **Yatırım Miktarı:** {inv[1]:.2f} TL  
    **Altın Miktarı:** {inv[4]:.2f} gram  
    **Güncel Değer:** {current_value:.2f} TL  
    **Kar/Zarar:** {profit:.2f} TL
    """)

# Aylık kar/zarar grafiği
st.subheader("Aylık Kar/Zarar Grafiği")
df = pd.DataFrame(filtered_investments, columns=["ID", "Amount", "Date", "Gold Price", "Quantity"])
df["Date"] = pd.to_datetime(df["Date"])
df["Current Value"] = df["Quantity"] * get_gold_price()
df["Profit"] = df["Current Value"] - df["Amount"]
df["Month"] = df["Date"].dt.to_period("M")
monthly_profit = df.groupby("Month")["Profit"].sum()
st.line_chart(monthly_profit)