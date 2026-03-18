#!/usr/bin/env python3
import streamlit as st
import pandas as pd
import numpy as np
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import tempfile

st.set_page_config(page_title="Advanced Finance Advisor", page_icon="💰")

st.title("💰 Advanced Personal Finance Advisor")

# ---------------- INPUTS ---------------- #
age = st.slider("Age", 18, 60, 30)
salary = st.number_input("Annual Salary (₹)", value=1000000)
monthly_expense = st.slider("Monthly Expense (₹)", 10000, 200000, int(salary*0.4/12))
debt_percent = st.slider("Debt Allocation (%)", 0, 80, 30)

# Goals
st.subheader("🎯 Goals")
education_goal = st.number_input("Child Education Goal (₹)", value=2000000)
house_goal = st.number_input("House Goal (₹)", value=5000000)

# ---------------- LOGIC ---------------- #
def insurance_needed(salary):
    return salary * 15

def premium_by_company(age, cover):
    return {
        "ICICI": cover * (0.00012 if age < 30 else 0.00018),
        "SBI": cover * (0.00013 if age < 30 else 0.00020),
        "LIC": cover * (0.00016 if age < 30 else 0.00025),
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

# returns
equity_r = 0.12 / 12
debt_r = 0.07 / 12
inflation = 0.06

def future_value(pmt, r, n):
    return pmt * (((1+r)**n - 1)/r)

equity_fv = future_value(equity, equity_r, months)
debt_fv = future_value(debt, debt_r, months)
total_fv = equity_fv + debt_fv

# Inflation adjusted
real_value = total_fv / ((1 + inflation) ** years)

# ---------------- OUTPUT ---------------- #
st.subheader("📊 Summary")

st.write(f"**Insurance Cover:** ₹{cover:,.0f}")

st.write("### 🛡️ Insurance Comparison")
df_ins = pd.DataFrame(premiums.items(), columns=["Company", "Annual Premium"])
st.dataframe(df_ins)

st.write(f"**Monthly Surplus:** ₹{monthly_surplus:,.0f}")
st.write(f"**Equity Investment:** ₹{equity:,.0f}")
st.write(f"**Debt Investment:** ₹{debt:,.0f}")

st.write("### 💰 Corpus")
st.write(f"Nominal Corpus: ₹{total_fv:,.0f}")
st.write(f"Inflation Adjusted Corpus: ₹{real_value:,.0f}")

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

st.write(f"Education Goal: ₹{education_goal:,.0f}")
st.write(f"House Goal: ₹{house_goal:,.0f}")

if total_fv > (education_goal + house_goal):
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

    Corpus: {total_fv:,.0f}
    Inflation Adjusted: {real_value:,.0f}

    Equity: {equity:,.0f}
    Debt: {debt:,.0f}
    """

    pdf_file = generate_pdf(text)

    with open(pdf_file, "rb") as f:
        st.download_button("Download PDF", f, file_name="report.pdf")

# ---------------- COUNTER ---------------- #
if "visits" not in st.session_state:
    st.session_state.visits = 0

st.session_state.visits += 1
st.markdown("---")
st.write(f"👥 Visitors: {st.session_state.visits}")
