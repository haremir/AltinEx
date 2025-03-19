import streamlit as st
import pandas as pd

def show_investment_form(db, investment, user_id):
    st.subheader("Yeni Yatırım Ekle")
    amount = st.number_input("Yatırım Miktarı (TL)", min_value=0.0, key="investment_amount", value=None)
    date = st.date_input("Yatırım Tarihi", key="investment_date")
    if st.button("Yatırım Ekle"):
        if amount and amount > 0:
            gold_price = investment.get_gold_price()
            quantity = amount / gold_price
            db.add_investment(user_id, amount, date, gold_price, quantity)
            st.success("Yatırım başarıyla eklendi!")
        else:
            st.error("Yatırım miktarı 0 TL'den fazla olmalıdır!")

def show_individual_investment_analysis(investment, user_id):
    st.subheader("Yatırım Bazlı Kar/Zarar Analizi")
    analysis = investment.get_individual_investment_analysis(user_id)
    
    if analysis:
        df = pd.DataFrame(analysis)
        df["date"] = pd.to_datetime(df["date"])
        df = df[["date", "amount", "quantity", "current_value", "profit", "profit_ratio"]]
        df.columns = ["Tarih", "Yatırım Miktarı (TL)", "Alınan Altın Miktarı (gram)", "Güncel Değer (TL)", "Kar/Zarar (TL)", "Kar/Zarar Oranı (%)"]

        # Filtreleme ve sıralama
        col1, col2, col3 = st.columns(3)
        with col1:
            sort_by = st.selectbox("Sırala", ["Tarih", "Kar/Zarar Miktarı", "Kar/Zarar Oranı"])
        with col2:
            filter_by = st.selectbox("Filtrele", ["Tümü", "Karda Olanlar", "Zararda Olanlar"])
        with col3:
            ascending = st.checkbox("Artan Sırala", True)

        # Filtreleme
        if filter_by == "Karda Olanlar":
            df = df[df["Kar/Zarar (TL)"] > 0]
        elif filter_by == "Zararda Olanlar":
            df = df[df["Kar/Zarar (TL)"] < 0]

        # Sıralama
        if sort_by == "Tarih":
            df = df.sort_values(by="Tarih", ascending=ascending)
        elif sort_by == "Kar/Zarar Miktarı":
            df = df.sort_values(by="Kar/Zarar (TL)", ascending=ascending)
        elif sort_by == "Kar/Zarar Oranı":
            df = df.sort_values(by="Kar/Zarar Oranı (%)", ascending=ascending)

        # Detaylı bilgiler
        st.subheader("Detaylı Bilgiler")
        for index, row in df.iterrows():
            color = "green" if row["Kar/Zarar (TL)"] > 0 else "red"
            with st.expander(f"{row['Tarih'].strftime('%d %B %Y').upper()} - YATIRIM DETAYI", expanded=False):
                st.write(f"""
                **Yatırım Miktarı:** {row['Yatırım Miktarı (TL)']:.2f} TL  
                **Alınan Altın Miktarı:** {row['Alınan Altın Miktarı (gram)']:.2f} gram  
                **Güncel Değer:** {row['Güncel Değer (TL)']:.2f} TL  
                **Kar/Zarar:** <span style="color: {color}">{row['Kar/Zarar (TL)']:.2f} TL</span>  
                **Kar/Zarar Oranı:** <span style="color: {color}">{row['Kar/Zarar Oranı (%)']:.2f}%</span>
                """, unsafe_allow_html=True)

        # Grafik
        st.subheader("Yatırım Bazlı Kar/Zarar Grafiği")
        st.line_chart(df.set_index("Tarih")["Kar/Zarar (TL)"])
        st.write("X Ekseni: Tarih")
        st.write("Y Ekseni: Kar/Zarar Miktarı (TL)")
    else:
        st.warning("Henüz yatırım bulunmamaktadır.")

def show_financial_summary(investment, user_id):
    st.subheader("Genel Finansal Özet")
    summary = investment.get_total_investment_analysis(user_id)
    color = "green" if summary["total_profit"] > 0 else "red"
    st.write(f"""
    **Toplam Yatırım:** {summary["total_investment"]:.2f} TL  
    **Toplam Altın Miktarı:** {summary["total_quantity"]:.2f} gram  
    **Güncel Değer:** <span style="color: {color}">{summary["current_value"]:.2f} TL</span>  
    **Toplam Kar/Zarar:** <span style="color: {color}">{summary["total_profit"]:.2f} TL</span>  
    **Toplam Kar/Zarar Oranı:** <span style="color: {color}">{summary["total_profit_ratio"]:.2f}%</span>
    """, unsafe_allow_html=True)