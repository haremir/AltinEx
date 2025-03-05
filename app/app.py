import streamlit as st
from src.db.database import Database
from src.models.investment import calculate_profit

# Veritabanı bağlantısı
db = Database()
db.create_table()  # Tabloları oluştur

# Kullanıcı ekleme ve altın alım işlemleri
st.title("Altın Yatırım Takip Uygulaması")

# Kullanıcı ekleme formu
with st.form(key='user_form'):
    isim = st.text_input("İsim")
    email = st.text_input("Email")
    telefon = st.text_input("Telefon")
    submit_button = st.form_submit_button(label="Kullanıcı Ekle")
    
    if submit_button:
        db.add_user(isim, email, telefon)
        st.success(f"{isim} başarıyla kaydedildi.")

# Kullanıcı altın alım formu
email = st.text_input("Kullanıcı E-postası ile Altın Alım Kaydı Ekle")
if email:
    user = db.get_user(email)
    if user:
        st.write(f"Kullanıcı Bilgileri: {user}")

        tarih = st.date_input("Alım Tarihi")
        miktar = st.number_input("Alınan Miktar (gram)", min_value=0.0, format="%.2f")
        fiyat = st.number_input("Alım Fiyatı (TL/gram)", min_value=0.0, format="%.2f")

        submit_button = st.form_submit_button(label="Altın Alım Yap")
        
        if submit_button:
            db.add_alim(user[0], str(tarih), miktar, fiyat)
            st.success("Altın alımı başarıyla kaydedildi.")

        # Altın kar hesaplama (örnek)
        current_fiyat = 650  # Bu, API'den alınabilir
        profit = calculate_profit(miktar, fiyat, current_fiyat)
        st.write(f"Kar/Zarar: {profit} TL")
