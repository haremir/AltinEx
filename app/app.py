import sys
import os
import streamlit as st
from datetime import datetime

# Proje kök dizinini sys.path'e ekle
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.db.database import Database
from src.models.investment import Investment
from src.db.gold_price_manager import GoldPriceManager
from components.auth import show_login_form, show_register_form
from components.investment_ui import (
    show_individual_investment_analysis,
    show_investment_form,
    show_financial_summary
)

# Veritabanı ve Investment sınıfını başlat
db = Database("data/investment_app.db")
investment = Investment(db)

# GoldPriceManager'ı başlat
gold_price_manager = GoldPriceManager("data/investment_app.db")

# Ana uygulama
def main():
    # Logo
    st.image("ALTINEX.PNG", width=1600)

    # Giriş ve kayıt butonları
    with st.sidebar:
        st.image("ALTINEX.PNG", width=600)

        if not st.session_state.get("logged_in"):
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Giriş Yap", use_container_width=True):
                    st.session_state["show_login"] = True
                    st.session_state["show_register"] = False
            with col2:
                if st.button("Kayıt Ol", use_container_width=True):
                    st.session_state["show_login"] = False
                    st.session_state["show_register"] = True

            if st.session_state.get("show_login"):
                show_login_form(db)
            if st.session_state.get("show_register"):
                show_register_form(db)
        else:
            # Kullanıcı giriş yaptığında sidebar içeriği
            st.subheader("Hesap İşlemleri")
            if st.button("Profilimi Görüntüle"):
                st.session_state["show_profile"] = True
                st.rerun()  # Sayfayı yenile

            st.markdown("---")  # Çizgi ekle

            # Güncel altın fiyatını güncelleme alanı
            st.subheader("Güncel Altın Fiyatını Güncelle")
            current_gold_price = st.number_input("Güncel Altın Fiyatı (TL/gram)", min_value=0.0, key="current_gold_price")
            if st.button("Fiyatı Güncelle"):
                if current_gold_price > 0:
                    date = datetime.now().strftime('%Y-%m-%d')
                    db.add_gold_price(date, current_gold_price)
                    st.success("Altın fiyatı başarıyla güncellendi!")
                else:
                    st.error("Geçerli bir fiyat giriniz.")

            # Gerçek zamanlı altın fiyatını güncelle
            if st.button("Altın Fiyatını Otomatik Güncelle"):
                fetched_price = gold_price_manager.fetch_gold_price()
                if fetched_price:
                    st.success(f"Altın fiyatı güncellendi: {fetched_price} TL/gram")
                else:
                    st.error("Altın fiyatı güncellenemedi. Lütfen internet bağlantınızı kontrol edin.")

            # Güncel altın fiyatını göster
            latest_gold_price = db.get_gold_price()
            if latest_gold_price:
                st.write(f"**Güncel Altın Fiyatı:** {latest_gold_price[1]:.2f} TL/gram (Son Güncelleme: {latest_gold_price[0]})")
            else:
                st.warning("Altın fiyatı bulunamadı. Lütfen altın fiyatını güncelleyin.")

            st.markdown("---")  # Çizgi ekle

            # Çıkış yap butonunu en alta ekle
            if st.button("Çıkış Yap", use_container_width=True):
                st.session_state["logged_in"] = False
                st.session_state["user_id"] = None
                st.session_state["show_profile"] = False
                st.success("Başarıyla çıkış yapıldı!")
                st.rerun()

    # Kullanıcı giriş yapmadan erişimi engelle
    if not st.session_state.get("logged_in"):
        st.warning("Lütfen giriş yapın veya kayıt olun.")
        st.stop()

    # Ana uygulama içeriği
    if st.session_state.get("show_profile"):
        # Profil görüntüleme ekranını göster
        show_profile(db, st.session_state["user_id"])
    else:
        # Normal yatırım ekranını göster
        try:
            show_investment_form(db, investment, st.session_state["user_id"])
            show_financial_summary(investment, st.session_state["user_id"])
            show_individual_investment_analysis(investment, st.session_state["user_id"])
        except ValueError as e:
            st.error(str(e))  # Hata mesajını kullanıcıya göster
            st.warning("Lütfen altın fiyatını güncelleyin.")

def show_profile(db, user_id):
    st.subheader("Hesap Bilgilerim")
    user = db.get_user(user_id)
    if user:
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Ad:** {user[1]}")
            st.write(f"**Soyad:** {user[2]}")
        with col2:
            st.write(f"**E-posta:** {user[3]}")
            st.write(f"**Telefon Numarası:** {user[4]}")
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Hesap Bilgilerimi Güncelle"):
                st.session_state["show_update_profile"] = True
        with col2:
            if st.button("Ana Sayfaya Dön"):
                st.session_state["show_profile"] = False
                st.session_state["show_update_profile"] = False
                st.rerun()

    if st.session_state.get("show_update_profile"):
        show_update_profile_form(db, user_id)

def show_update_profile_form(db, user_id):
    st.subheader("Hesap Bilgilerini Güncelle")
    user = db.get_user(user_id)
    if user:
        with st.form(key="update_profile_form"):
            first_name = st.text_input("Ad", value=user[1], key="update_first_name")
            last_name = st.text_input("Soyad", value=user[2], key="update_last_name")
            email = st.text_input("E-posta", value=user[3], key="update_email")
            phone = st.text_input("Telefon Numarası", value=user[4], key="update_phone")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.form_submit_button("Güncelle"):
                    db.update_user(user_id, first_name, last_name, email, phone)
                    st.success("Hesap bilgileriniz başarıyla güncellendi!")
                    st.session_state["show_update_profile"] = False
                    st.rerun()

if __name__ == "__main__":
    main()