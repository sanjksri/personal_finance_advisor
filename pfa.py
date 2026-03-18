#!/usr/bin/env python3
import streamlit as st
import math

st.set_page_config(page_title="Personal Finance Advisor", page_icon="💰", layout="centered")

# ---------------- STYLE ---------------- #
st.markdown("""
<style>
.big-title {
    font-size:32px;
    font-weight:700;
    color:#2E7D32;
}
.card {
    background-color:#f5f5f5;
    padding:15px;
    border-radius:12px;
    margin-bottom:10px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ---------------- #
st.markdown('<div class="big-title">💰 Personal Finance Advisor</div>', unsafe_allow_html=True)
st.write("Get personalized financial guidance based on your profile.")

# ---------------- INPUTS ---------------- #
age = st.slider("Age", 18, 70, 30)
gender = st.selectbox("Gender", ["Male", "Female", "Other"])
marital = st.selectbox("Marital Status", ["Single", "Married"])
salary = st.number_input("Annual Salary (₹)", min_value=100000, step=50000)

# ---------------- LOGIC ---------------- #
def get_risk_profile(age, marital):
    if age < 30:
        return "High"
    elif age < 45:
        return "Moderate"
    else:
        return "Low"

def insurance_needed(salary, marital):
    multiplier = 15 if marital == "Married" else 10
    return salary * multiplier

def allocation(age):
    equity = max(100 - age, 20)  # thumb rule
    debt = 100 - equity
    return equity, debt

# ---------------- BUTTON ---------------- #
if st.button("Generate Plan"):

    risk = get_risk_profile(age, marital)
    insurance = insurance_needed(salary, marital)
    equity, debt = allocation(age)

    monthly_sip = round((salary * equity/100) / 12 * 0.3, 0)  # 30% investable assumption

    # ---------------- OUTPUT ---------------- #
    st.markdown("### 📊 Your Financial Plan")

    st.markdown(f'<div class="card">🔹 <b>Risk Profile:</b> {risk}</div>', unsafe_allow_html=True)

    st.markdown(f'<div class="card">🛡️ <b>Recommended Life Insurance:</b> ₹{insurance:,.0f}</div>', unsafe_allow_html=True)

    st.markdown(f'<div class="card">💳 <b>Debt Allocation:</b> {debt}% of investments</div>', unsafe_allow_html=True)

    st.markdown("### 🏦 Suggested Debt Instruments")
    st.markdown("""
- **PPF** (Safe, tax-free): https://www.nsiindia.gov.in  
- **EPF/VPF**: https://www.epfindia.gov.in  
- **Debt Mutual Funds**: https://www.amfiindia.com  
- **RBI Bonds**: https://rbiretaildirect.org.in  
""")

    st.markdown(f'<div class="card">📈 <b>Equity (SIP Allocation):</b> {equity}%</div>', unsafe_allow_html=True)

    st.markdown(f'<div class="card">💰 <b>Suggested Monthly SIP:</b> ₹{monthly_sip:,.0f}</div>', unsafe_allow_html=True)

    st.markdown("### 📊 Suggested SIP Types")
    st.markdown("""
- **Index Funds (Nifty 50 / Sensex)** – Low cost, stable  
  https://groww.in/mutual-funds/category/index-funds  

- **Large Cap Funds** – Lower volatility  
  https://www.valueresearchonline.com  

- **Flexi Cap Funds** – Balanced growth  
  https://www.moneycontrol.com/mutual-funds/  

- **ELSS (Tax Saving)** – Section 80C benefit  
  https://cleartax.in/s/elss-funds  
""")

    # Future value calculation (12% return assumed)
    years = max(60 - age, 10)
    r = 0.12 / 12
    n = years * 12
    fv = monthly_sip * (((1 + r)**n - 1) / r)

    st.markdown(f'<div class="card">📅 <b>Estimated Corpus by Age 60:</b> ₹{fv:,.0f}</div>', unsafe_allow_html=True)

# ---------------- VISITOR COUNTER ---------------- #
if "visits" not in st.session_state:
    st.session_state.visits = 0

st.session_state.visits += 1

st.markdown("---")
st.markdown(f"👥 Visitors: {st.session_state.visits}")
