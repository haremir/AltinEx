import streamlit as st
import pandas as pd

def show_investment_form(db, investment, user_id):
    st.subheader("Yeni Yatırım Ekle")
    amount = st.number_input("Yatırım Miktarı (TL)", min_value=0.0, key="investment_amount")
    date = st.date_input("Yatırım Tarihi", key="investment_date")
    if st.button("Yatırım Ekle"):
        if amount > 0:
            gold_price = investment.get_gold_price()
            quantity = amount / gold_price
            db.add_investment(user_id, amount, date, gold_price, quantity)
            st.success("Yatırım başarıyla eklendi!")
        else:
            st.error("Yatırım miktarı 0 TL'den fazla olmalıdır!")

def show_individual_investment_analysis(investment, user_id):
    st.subheader("Bireysel Yatırım Analizi")
    analysis = investment.get_individual_investment_analysis(user_id)
    if analysis:
        df = pd.DataFrame(analysis)
        st.dataframe(df)  # Tablo olarak göster
    else:
        st.warning("Henüz yatırım bulunmamaktadır.")

def show_financial_summary(investment, user_id):
    st.subheader("Genel Finansal Özet")
    summary = investment.get_total_investment_analysis(user_id)
    st.write(f"""
    **Toplam Yatırım:** {summary["total_investment"]:.2f} TL  
    **Toplam Altın Miktarı:** {summary["total_quantity"]:.2f} gram  
    **Güncel Değer:** {summary["current_value"]:.2f} TL  
    **Toplam Kar/Zarar:** {summary["total_profit"]:.2f} TL  
    **Toplam Kar/Zarar Oranı:** {summary["total_profit_ratio"]:.2f}%
    """)

def show_total_investment_analysis(investment, user_id):
    st.subheader("Toplam Yatırım Analizi")
    summary = investment.get_total_investment_analysis(user_id)
    st.write(f"""
    **Toplam Yatırım:** {summary["total_investment"]:.2f} TL  
    **Toplam Altın Miktarı:** {summary["total_quantity"]:.2f} gram  
    **Güncel Değer:** {summary["current_value"]:.2f} TL  
    **Toplam Kar/Zarar:** {summary["total_profit"]:.2f} TL  
    **Toplam Kar/Zarar Oranı:** {summary["total_profit_ratio"]:.2f}%
    """)

def show_monthly_profit_chart(investment, user_id):
    st.subheader("Aylık Kar/Zarar Grafiği")
    analysis = investment.get_individual_investment_analysis(user_id)
    if analysis:
        df = pd.DataFrame(analysis)
        df["date"] = pd.to_datetime(df["date"])
        df["Month"] = df["date"].dt.to_period("M")
        monthly_profit = df.groupby("Month")["profit"].sum()
        st.line_chart(monthly_profit)
    else:
        st.warning("Henüz yatırım bulunmamaktadır.")