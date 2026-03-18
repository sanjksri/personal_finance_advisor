#!/usr/bin/env python3
import streamlit as st

st.set_page_config(page_title="Personal Finance Advisor", page_icon="💰", layout="centered")

# ---------------- STYLE ---------------- #
st.markdown("""
<style>
.big-title {
    font-size:34px;
    font-weight:700;
    color:#1B5E20;
}
.card {
    background-color:#f1f8e9;
    padding:15px;
    border-radius:12px;
    margin-bottom:12px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ---------------- #
st.markdown('<div class="big-title">💰 Personal Finance Advisor</div>', unsafe_allow_html=True)
st.write("Smart financial planning based on your lifestyle and risk profile.")

# ---------------- INPUTS ---------------- #
age = st.slider("Age", 18, 60, 30)
gender = st.selectbox("Gender", ["Male", "Female", "Other"])
marital = st.selectbox("Marital Status", ["Single", "Married"])
salary = st.number_input("Annual Salary (₹)", min_value=200000, step=50000, value=1000000)

# ----------- NEW SLIDERS (MARKET STANDARD DEFAULTS) ----------- #

monthly_expense = st.slider(
    "Average Monthly Expense (₹)",
    10000, 200000, int(salary * 0.4 / 12)
)

debt_percent = st.slider(
    "Debt Allocation (%)",
    0, 80, 30  # market typical ~20–40%
)

insurance_rate = st.slider(
    "Term Insurance Premium (% of Cover per year)",
    0.5, 2.0, 1.0, step=0.1
)

# ---------------- LOGIC ---------------- #
def get_risk_profile(age):
    if age < 30:
        return "High"
    elif age < 45:
        return "Moderate"
    else:
        return "Low"

def insurance_needed(salary, marital):
    multiplier = 15 if marital == "Married" else 10
    return salary * multiplier

# ---------------- BUTTON ---------------- #
if st.button("Generate Financial Plan"):

    risk = get_risk_profile(age)
    insurance_cover = insurance_needed(salary, marital)

    # Insurance premium
    insurance_premium = insurance_cover * (insurance_rate / 100)

    # Monthly investment capacity
    monthly_income = salary / 12
    monthly_surplus = monthly_income - monthly_expense - (insurance_premium / 12)

    monthly_surplus = max(monthly_surplus, 0)

    # Allocation
    debt_invest = monthly_surplus * (debt_percent / 100)
    equity_invest = monthly_surplus - debt_invest

    # Future value assumptions
    years = 60 - age
    months = years * 12

    # Returns
    equity_r = 0.12 / 12
    debt_r = 0.07 / 12

    # Future value calculation
    def future_value(pmt, r, n):
        if r == 0:
            return pmt * n
        return pmt * (((1 + r) ** n - 1) / r)

    equity_fv = future_value(equity_invest, equity_r, months)
    debt_fv = future_value(debt_invest, debt_r, months)

    total_fv = equity_fv + debt_fv

    # ---------------- OUTPUT ---------------- #
    st.markdown("### 📊 Your Financial Plan")

    st.markdown(f'<div class="card">🔹 <b>Risk Profile:</b> {risk}</div>', unsafe_allow_html=True)

    st.markdown(f'<div class="card">🛡️ <b>Recommended Insurance Cover:</b> ₹{insurance_cover:,.0f}<br>'
                f'Annual Premium ≈ ₹{insurance_premium:,.0f}</div>', unsafe_allow_html=True)

    st.markdown(f'<div class="card">💸 <b>Monthly Surplus Available for Investment:</b> ₹{monthly_surplus:,.0f}</div>',
                unsafe_allow_html=True)

    st.markdown(f'<div class="card">💳 <b>Debt Investment:</b> ₹{debt_invest:,.0f}/month</div>',
                unsafe_allow_html=True)

    st.markdown(f'<div class="card">📈 <b>Equity SIP Investment:</b> ₹{equity_invest:,.0f}/month</div>',
                unsafe_allow_html=True)

    # Instruments
    st.markdown("### 🏦 Suggested Debt Instruments")
    st.markdown("""
- PPF – https://www.nsiindia.gov.in  
- RBI Bonds – https://rbiretaildirect.org.in  
- Debt Mutual Funds – https://www.amfiindia.com  
""")

    st.markdown("### 📊 Suggested SIP Options")
    st.markdown("""
- Index Funds – https://groww.in/mutual-funds/category/index-funds  
- Flexi Cap Funds – https://www.moneycontrol.com/mutual-funds/  
- ELSS – https://cleartax.in/s/elss-funds  
""")

    st.markdown("### 📅 Wealth Projection")

    st.markdown(f'<div class="card">📈 <b>Equity Corpus (12% return):</b> ₹{equity_fv:,.0f}</div>',
                unsafe_allow_html=True)

    st.markdown(f'<div class="card">🏦 <b>Debt Corpus (7% return):</b> ₹{debt_fv:,.0f}</div>',
                unsafe_allow_html=True)

    st.markdown(f'<div class="card" style="background-color:#c8e6c9;">💰 <b>Total Corpus at 60:</b> ₹{total_fv:,.0f}</div>',
                unsafe_allow_html=True)

# ---------------- VISITOR COUNTER ---------------- #
if "visits" not in st.session_state:
    st.session_state.visits = 0

st.session_state.visits += 1

st.markdown("---")
st.markdown(f"👥 Visitors: {st.session_state.visits}")
