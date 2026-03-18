#!/usr/bin/env python3
import streamlit as st
import pandas as pd
import numpy as np
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import tempfile

st.set_page_config(page_title="Advanced Finance Advisor", page_icon="💰")

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
st.markdown('<div class="big-title">💰 Advanced Personal Finance Advisor</div>', unsafe_allow_html=True)

# ---------------- INPUTS ---------------- #
age = st.slider("Age", 18, 60, 30)
salary = st.number_input("Annual Salary (₹)", value=1000000)

monthly_expense = st.slider(
    "Monthly Expense (₹)",
    10000, 200000, int(salary * 0.4 / 12)
)

debt_percent = st.slider("Debt Allocation (%)", 0, 80, 30)

# ---------------- GOALS ---------------- #
st.subheader("🎯 Goals")
education_goal = st.number_input("Child Education Goal (₹)", value=2000000)
house_goal = st.number_input("House Goal (₹)", value=5000000)

# ---------------- LOGIC ---------------- #
def insurance_needed(salary):
    return salary * 15

def premium_by_company(age, cover):
    if age < 30:
        return {
            "ICICI": cover * 0.00012,
            "SBI": cover * 0.00013,
            "LIC": cover * 0.00016,
        }
    elif age < 40:
        return {
            "ICICI": cover * 0.00018,
            "SBI": cover * 0.00020,
            "LIC": cover * 0.00025,
        }
    else:
        return {
            "ICICI": cover * 0.00030,
            "SBI": cover * 0.00035,
            "LIC": cover * 0.00040,
        }

cover = insurance_needed(salary)
premiums = premium_by_company(age, cover)

monthly_income = salary / 12
monthly_surplus = monthly_income - monthly_expense
monthly_surplus = max(monthly_surplus, 0)

debt = monthly_surplus * debt_percent / 100
equity = monthly_surplus - debt

years = 60 - age
months = years * 12

# Returns
equity_r = 0.12 / 12
debt_r = 0.07 / 12
inflation = 0.06

def future_value(pmt, r, n):
    if r == 0:
        return pmt * n
    return pmt * (((1+r)**n - 1)/r)

equity_fv = future_value(equity, equity_r, months)
debt_fv = future_value(debt, debt_r, months)
total_fv = equity_fv + debt_fv

# Inflation-adjusted
real_value = total_fv / ((1 + inflation) ** years)

# ---------------- OUTPUT ---------------- #
st.subheader("📊 Financial Summary")

st.markdown(f'<div class="card">💰 <b>Monthly Surplus:</b> ₹{monthly_surplus:,.0f}</div>', unsafe_allow_html=True)

# ---------------- INSURANCE ---------------- #
st.write(f"### 🛡️ Insurance Cover: ₹{cover:,.0f}")

df_ins = pd.DataFrame([
    {
        "Company": k,
        "Annual Premium (₹)": round(v, 0),
        "Monthly Premium (₹)": round(v / 12, 0)
    }
    for k, v in premiums.items()
])

st.subheader("🛡️ Insurance Comparison")
st.dataframe(df_ins)

# ---------------- INVESTMENT ---------------- #
st.markdown(f'<div class="card">📈 Equity SIP: ₹{equity:,.0f}/month</div>', unsafe_allow_html=True)
st.markdown(f'<div class="card">🏦 Debt Investment: ₹{debt:,.0f}/month</div>', unsafe_allow_html=True)

# ---------------- CORPUS ---------------- #
st.subheader("💰 Wealth Projection")

st.markdown(f'<div class="card">Nominal Corpus: ₹{total_fv:,.0f}</div>', unsafe_allow_html=True)
st.markdown(f'<div class="card">Inflation Adjusted Corpus: ₹{real_value:,.0f}</div>', unsafe_allow_html=True)

# ---------------- GRAPH ---------------- #
st.subheader("📈 Wealth Growth Curve")

years_list = list(range(years))
values = []

for y in years_list:
    m = y * 12
    val = future_value(equity, equity_r, m) + future_value(debt, debt_r, m)
    values.append(val)

df = pd.DataFrame({"Year": years_list, "Wealth": values})
st.line_chart(df.set_index("Year"))

# ---------------- GOAL CHECK ---------------- #
st.subheader("🎯 Goal Analysis")

total_goal = education_goal + house_goal

st.write(f"Total Goals: ₹{total_goal:,.0f}")

if total_fv > total_goal:
    st.success("✅ You are on track for your goals")
else:
    st.warning("⚠️ You may fall short. Increase SIP or reduce expenses.")

# ---------------- PDF EXPORT ---------------- #
def generate_pdf(text):
    file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    doc = SimpleDocTemplate(file.name)
    styles = getSampleStyleSheet()
    story = [Paragraph(text, styles["Normal"])]
    doc.build(story)
    return file.name

if st.button("📄 Export PDF Report"):
    text = f"""
    Financial Report

    Age: {age}
    Salary: {salary}

    Monthly Investment: {monthly_surplus:,.0f}

    Corpus: {total_fv:,.0f}
    Inflation Adjusted: {real_value:,.0f}
    """

    pdf_file = generate_pdf(text)

    with open(pdf_file, "rb") as f:
        st.download_button("Download PDF", f, file_name="financial_report.pdf")

# ---------------- COUNTER ---------------- #
if "visits" not in st.session_state:
    st.session_state.visits = 0

st.session_state.visits += 1

st.markdown("---")
st.write(f"👥 Visitors: {st.session_state.visits}")
