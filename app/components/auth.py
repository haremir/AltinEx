import streamlit as st

def show_login_form(db):
    st.sidebar.subheader("Hesabınıza Giriş Yapın")
    with st.sidebar.form(key="login_form"):
        username = st.text_input("Kullanıcı Adı", key="login_username")
        password = st.text_input("Şifre", type="password", key="login_password")
        
        if st.form_submit_button("Giriş Yap"):
            user = db.login_user(username, password)
            if user:
                st.sidebar.success(f"Hoş geldiniz, {user[1]}!")
                st.session_state["logged_in"] = True
                st.session_state["user_id"] = user[0]
                # Sayfayı yeniden yükle
                st.rerun()
            else:
                st.sidebar.error("Geçersiz kullanıcı adı veya şifre!")
                # Hata durumunda da yeniden yükleyebilirsiniz
                st.rerun()

def show_register_form(db):
    st.sidebar.subheader("Yeni Hesap Oluştur")
    with st.sidebar.form(key="register_form"):
        first_name = st.text_input("Ad", key="register_first_name")
        last_name = st.text_input("Soyad", key="register_last_name")
        email = st.text_input("E-posta", key="register_email")
        phone = st.text_input("Telefon Numarası", key="register_phone")
        username = st.text_input("Kullanıcı Adı", key="register_username")
        password = st.text_input("Şifre", type="password", key="register_password")
        confirm_password = st.text_input("Şifreyi Tekrar Girin", type="password", key="register_confirm_password")
        if st.form_submit_button("Kayıt Ol"):
            if password == confirm_password:
                db.register_user(first_name, last_name, email, phone, username, password)
                st.sidebar.success("Hesabınız başarıyla oluşturuldu!")
                # Formu temizle
                st.session_state["register_form_submitted"] = True
            else:
                st.sidebar.error("Şifreler eşleşmiyor!")
                # Hatalı kayıtta formu temizle
                st.session_state["register_form_submitted"] = True

    # Form gönderildikten sonra metin alanlarını temizle
    if st.session_state.get("register_form_submitted"):
        st.session_state["register_first_name"] = ""
        st.session_state["register_last_name"] = ""
        st.session_state["register_email"] = ""
        st.session_state["register_phone"] = ""
        st.session_state["register_username"] = ""
        st.session_state["register_password"] = ""
        st.session_state["register_confirm_password"] = ""
        st.session_state["register_form_submitted"] = False