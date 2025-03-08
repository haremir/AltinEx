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

# Logo ve yazıyı hizalama
col1, col2, col3 = st.columns([2, 4, 2])  # Logoyu ve yazıyı hizalamak için sütunlar
with col2:
    st.image("ALTINEX.PNG", width=1600)  # Logoyu ortala ve boyutunu 2 katına çıkar (400 -> 800)

# Ana başlık ve logo
st.markdown("<h1 style='text-align: center; font-size: 36px;'>ALTINEX</h1>", unsafe_allow_html=True)  # ALTINEX yazısı
st.markdown("<h2 style='text-align: center; font-size: 24px;'>             ALTIN YATIRIM TAKIP UYGULAMASI</h2>", unsafe_allow_html=True)  # Büyük harflerle yazı

# Veritabanını başlat
conn = initialize_db()
if conn is None:
    st.error("Veritabanı bağlantısı kurulamadı! Lütfen veritabanını kontrol edin.")
    st.stop()

# Soldaki panelin en tepesine büyük logo ekle
with st.sidebar:
    st.image("ALTINEX.PNG", width=600)  # Soldaki panele büyük logo ekle ve boyutunu 2 katına çıkar (300 -> 600)

# Giriş ve kayıt butonları
col1, col2 = st.sidebar.columns(2)
with col1:
    if st.button("Giriş Yap", key="login_button", use_container_width=True):
        st.session_state["show_login"] = True
        st.session_state["show_register"] = False
with col2:
    if st.button("Kayıt Ol", key="register_button", use_container_width=True):
        st.session_state["show_login"] = False
        st.session_state["show_register"] = True

# Giriş formu
if st.session_state.get("show_login"):
    st.sidebar.subheader("Hesabınıza Giriş Yapın")
    with st.sidebar.form(key="login_form"):
        username = st.text_input("Kullanıcı Adı", key="login_username")
        password = st.text_input("Şifre", type="password", key="login_password")
        if st.form_submit_button("Giriş Yap", use_container_width=True):
            conn = initialize_db()  # Yeni bağlantı oluştur
            user = login_user(conn, username, password)
            if user:
                st.sidebar.success(f"Hoş geldiniz, {user[1]}!")
                st.session_state["logged_in"] = True
                st.session_state["user_id"] = user[0]
            else:
                st.sidebar.error("Geçersiz kullanıcı adı veya şifre!")

# Kayıt formu
if st.session_state.get("show_register"):
    st.sidebar.subheader("Yeni Hesap Oluştur")
    with st.sidebar.form(key="register_form"):
        first_name = st.text_input("Ad", key="register_first_name")
        last_name = st.text_input("Soyad", key="register_last_name")
        email = st.text_input("E-posta", key="register_email")
        phone = st.text_input("Telefon Numarası", key="register_phone")
        username = st.text_input("Kullanıcı Adı", key="register_username")
        password = st.text_input("Şifre", type="password", key="register_password")
        confirm_password = st.text_input("Şifreyi Tekrar Girin", type="password", key="register_confirm_password")
        if st.form_submit_button("Kayıt Ol", use_container_width=True):
            if password == confirm_password:
                if first_name and last_name and email and phone and username and password:
                    conn = initialize_db()  # Yeni bağlantı oluştur
                    register_user(conn, first_name, last_name, email, phone, username, password)
                    st.sidebar.success("Hesabınız başarıyla oluşturuldu!")
                else:
                    st.sidebar.warning("Lütfen tüm alanları doldurun!")
            else:
                st.sidebar.error("Şifreler eşleşmiyor!")

# Çıkış butonu
if st.session_state.get("logged_in"):
    if st.sidebar.button("Çıkış Yap", key="logout_button", use_container_width=True):
        st.session_state["logged_in"] = False
        st.session_state["user_id"] = None
        st.session_state["show_login"] = False
        st.session_state["show_register"] = False
        st.sidebar.success("Başarıyla çıkış yapıldı!")

# Kullanıcı giriş yapmadan erişimi engelle
if not st.session_state.get("logged_in"):
    st.warning("Lütfen giriş yapın veya kayıt olun.")
    st.stop()

# Ana uygulama
st.title("ALTINEX - ALTIN YATIRIM TAKIP UYGULAMASI")

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
amount = st.number_input("Yatırım Miktarı (TL)", min_value=0.0, key="investment_amount")
date = st.date_input("Yatırım Tarihi", datetime.date.today(), key="investment_date")

if st.button("Yatırım Ekle", key="add_investment_button", use_container_width=True):
    if amount > 0:
        gold_price = get_gold_price()  # Güncel altın fiyatını al
        quantity = amount / gold_price  # Alınan altın miktarını hesapla
        conn = initialize_db()  # Yeni bağlantı oluştur
        add_investment(conn, st.session_state["user_id"], amount, format_date(date), gold_price, quantity)
        st.success("Yatırım başarıyla eklendi!")
    else:
        st.error("Yatırım miktarı 0 TL'den fazla olmalıdır!")

# Filtreleme seçenekleri
st.sidebar.subheader("Filtreleme Seçenekleri")
start_date = st.sidebar.date_input("Başlangıç Tarihi", datetime.date.today(), key="filter_start_date")
end_date = st.sidebar.date_input("Bitiş Tarihi", datetime.date.today(), key="filter_end_date")
profit_filter = st.sidebar.selectbox("Kar/Zarar Durumu", ["Tümü", "Kar", "Zarar"], key="filter_profit")

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