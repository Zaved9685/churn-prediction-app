import streamlit as st
if "logged_in" not in st.session_state:
    st.stop()
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Please login first")
    st.stop()
import matplotlib.pyplot as plt

st.metric("Total Customers", len(df))
st.metric("Churn Rate", f"{df['Churn'].mean()*100:.2f}%")

# Chart 1
fig, ax = plt.subplots()
df["Churn"].value_counts().plot(kind="bar", ax=ax)
st.pyplot(fig)

# Chart 2
fig2, ax2 = plt.subplots()
df.groupby("Churn")["tenure"].mean().plot(kind="bar", ax=ax2)
st.pyplot(fig2)
st.set_page_config(layout="wide")
st.subheader("📊 Key Metrics Overview")
import pandas as pd

st.title("📊 Customer Churn Dashboard")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("churn.csv")
    return df

df = load_data()

# Clean data
df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
df = df.dropna()

st.write("---")

# 🔹 FILTERS
st.sidebar.header("🔍 Filters")

contract_filter = st.sidebar.selectbox(
    "Select Contract Type",
    ["All"] + list(df["Contract"].unique())
)

internet_filter = st.sidebar.selectbox(
    "Select Internet Service",
    ["All"] + list(df["InternetService"].unique())
)

# Apply filters
filtered_df = df.copy()

if contract_filter != "All":
    filtered_df = filtered_df[filtered_df["Contract"] == contract_filter]

if internet_filter != "All":
    filtered_df = filtered_df[filtered_df["InternetService"] == internet_filter]

# 🔹 METRICS
total_customers = len(filtered_df)

churn_count = filtered_df["Churn"].value_counts().get("Yes", 0)
churn_percent = (churn_count / total_customers) * 100 if total_customers > 0 else 0

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Customers", total_customers)

with col2:
    st.metric("Churn Count", churn_count)

with col3:
    st.metric("Churn %", f"{churn_percent:.2f}%")

st.write("---")

# 🔹 CHURN BY CONTRACT
st.subheader("📌 Churn by Contract")

contract_churn = pd.crosstab(filtered_df["Contract"], filtered_df["Churn"])
st.bar_chart(contract_churn)

st.write("---")

# 🔹 CHURN BY INTERNET
st.subheader("🌐 Churn by Internet Service")

internet_churn = pd.crosstab(filtered_df["InternetService"], filtered_df["Churn"])
st.bar_chart(internet_churn)

st.write("---")

# 🔹 EXTRA INSIGHT
st.subheader("💰 Monthly Charges Distribution")

st.bar_chart(filtered_df["MonthlyCharges"].value_counts().sort_index())