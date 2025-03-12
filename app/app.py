import sys
import os
import streamlit as st

# Proje kök dizinini sys.path'e ekle
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.db.database import Database
from src.models.investment import Investment
from components.auth import show_login_form, show_register_form
from components.investment_ui import show_individual_investment_analysis, show_investment_form, show_financial_summary, show_monthly_profit_chart, show_total_investment_analysis

# Veritabanı ve Investment sınıfını başlat
db = Database("data/investment_app.db")
investment = Investment(db)

# Ana uygulama
def main():
    # Logo ve başlık
    st.image("ALTINEX.PNG", width=1600)
    st.markdown("<h1 style='text-align: center; font-size: 36px;'>ALTINEX</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; font-size: 24px;'>ALTIN YATIRIM TAKIP UYGULAMASI</h2>", unsafe_allow_html=True)

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
            if st.button("Çıkış Yap"):
                st.session_state["logged_in"] = False
                st.session_state["user_id"] = None
                st.session_state["show_profile"] = False
                st.sidebar.success("Başarıyla çıkış yapıldı!")
                # Sayfayı yenile
                st.rerun()

            if st.session_state.get("show_profile"):
                show_profile(db, st.session_state["user_id"])

    # Kullanıcı giriş yapmadan erişimi engelle
    if not st.session_state.get("logged_in"):
        st.warning("Lütfen giriş yapın veya kayıt olun.")
        st.stop()

    # Ana uygulama içeriği
    st.title("ALTINEX - ALTIN YATIRIM TAKIP UYGULAMASI")
    show_investment_form(db, investment, st.session_state["user_id"])
    show_individual_investment_analysis(investment, st.session_state["user_id"])
    show_financial_summary(investment, st.session_state["user_id"])
    show_total_investment_analysis(investment, st.session_state["user_id"])
    show_monthly_profit_chart(investment, st.session_state["user_id"])

def show_profile(db, user_id):
    st.sidebar.subheader("Hesap Bilgileri")
    user = db.get_user(user_id)
    if user:
        st.sidebar.write(f"**Ad:** {user[1]}")
        st.sidebar.write(f"**Soyad:** {user[2]}")
        st.sidebar.write(f"**E-posta:** {user[3]}")
        st.sidebar.write(f"**Telefon Numarası:** {user[4]}")
        if st.sidebar.button("Hesabımı Güncelle", key="update_profile"):
            st.session_state["show_update_profile"] = True

    if st.session_state.get("show_update_profile"):
        show_update_profile_form(db, user_id)

def show_update_profile_form(db, user_id):
    st.sidebar.subheader("Hesap Bilgilerini Güncelle")
    with st.sidebar.form(key="update_profile_form"):
        first_name = st.text_input("Ad", key="update_first_name")
        last_name = st.text_input("Soyad", key="update_last_name")
        email = st.text_input("E-posta", key="update_email")
        phone = st.text_input("Telefon Numarası", key="update_phone")
        if st.form_submit_button("Güncelle"):
            db.update_user(user_id, first_name, last_name, email, phone)
            st.sidebar.success("Hesap bilgileriniz başarıyla güncellendi!")
            st.session_state["show_update_profile"] = False
            st.rerun()

if __name__ == "__main__":
    main()