#!/usr/bin/env python3
import streamlit as st

st.set_page_config(page_title="Personal Finance Advisor", page_icon="💰")
st.markdown("Created by S K Srivastava, IFS")
st.markdown("Legal Disclaimer: This is a simple tool created for helping a person manage his finances. There is absolutely no guarantee on the projected returns as they are governed by the market conditions")

st.title("💰 Personal Finance Advisor")

# ---------------- INPUTS ---------------- #
age = st.slider("Age", 18, 60, 30)

marital = st.selectbox("Marital Status", ["Single", "Married"])
smoker = st.selectbox("Smoking Status", ["Non-Smoker", "Smoker"])

salary = st.number_input("Monthly Take Home Salary (₹)", value=80000)

monthly_expense = st.slider(
    "Monthly Expenses (₹)",
    10000, 200000, int(salary * 0.4)
)

# ---------------- CALCULATIONS ---------------- #
disposable_income = salary - monthly_expense
disposable_income = max(disposable_income, 0)

# Insurance suggestion
def insurance_needed(monthly_income):
    annual_income = monthly_income * 12
    cover = annual_income * 15
    return max(cover, 10000000)  # Minimum ₹1 Cr

insurance_cover = insurance_needed(salary)

insurance_slider = st.slider(
    "Select Insurance Cover (₹)",
    5000000, 50000000, insurance_cover, step=500000
)

# Premium adjustment
def premium_estimate(age, smoker, cover):
    base_rate = 0.00015
    if age > 40:
        base_rate += 0.0001
    if smoker == "Smoker":
        base_rate += 0.0001
    return cover * base_rate

premium = premium_estimate(age, smoker, insurance_slider)

# ---------------- ALLOCATION ---------------- #
debt_percent = st.slider("Debt Allocation (%)", 0, 80, 30)

debt_invest = disposable_income * debt_percent / 100
equity_invest = disposable_income - debt_invest

# ---------------- OUTPUT ---------------- #
st.subheader("📊 Financial Summary")

st.write(f"Disposable Income: ₹{disposable_income:,.0f}")

st.markdown("### 🛡️ Insurance Recommendation")
st.write(f"Suggested Cover: ₹{insurance_slider:,.0f}")
st.write(f"Estimated Monthly Premium: ₹{premium/12:,.0f}")
st.write(f"Estimated Annual Premium: ₹{premium:,.0f}")

# ---------------- INSURANCE OPTIONS ---------------- #
st.subheader("🏆 Top Term Insurance Plans (India)")

st.markdown("""
1. **LIC e-Term Plan**  
   https://licindia.in  

2. **ICICI Prudential iProtect Smart**  
   https://www.iciciprulife.com  

3. **SBI Life Smart Shield**  
   https://www.sbilife.co.in  
""")

# ---------------- DEBT ---------------- #
st.subheader("🏦 Debt Allocation")

st.write(f"Debt Investment: ₹{debt_invest:,.0f} per month")

st.markdown("""
Suggested Instruments:
- PPF – https://www.nsiindia.gov.in  
- RBI Bonds – https://rbiretaildirect.org.in  
- Debt Mutual Funds – https://www.amfiindia.com  
""")

# ---------------- SIP ---------------- #
st.subheader("📈 SIP Investment")

st.write(f"SIP Investment: ₹{equity_invest:,.0f} per month")

st.markdown("""
Suggested High Performing Categories (last 1 year):
- Index Funds (Nifty 50)
- Flexi Cap Funds
- Large & Midcap Funds

Explore:
- https://groww.in/mutual-funds  
- https://www.etmoney.com/mutual-funds/featured/best-sip-funds/18 
""")

# ---------------- PROJECTION ---------------- #
years = 60 - age
months = years * 12

r = 0.12 / 12

def future_value(pmt, r, n):
    return pmt * (((1+r)**n - 1)/r)

corpus = future_value(equity_invest, r, months)

st.subheader("💰 Retirement Projection")

st.write(f"Estimated Corpus at 60: ₹{corpus:,.0f}")
st.write(f"General advice: Take only term insurance, avoid hybrid funds like ULIP or Money back kind of products, Avoid trading in equities directly unless you understand markets properly. Prefer SIP route ")

# ---------------- COUNTER ---------------- #
if "visits" not in st.session_state:
    st.session_state.visits = 0

st.session_state.visits += 1

st.markdown("---")
st.write(f"👥 Visitors: {st.session_state.visits}")
