import streamlit as st
import sqlite3
import bcrypt

# ✅ MUST BE FIRST
st.set_page_config(page_title="Customer Churn Prediction", layout="wide")

# ---------------- SESSION ---------------- #
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.role = None

# ---------------- DATABASE ---------------- #
def create_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password BLOB,
        role TEXT
    )
    """)
    conn.commit()
    conn.close()

create_db()

def add_user(username, password, role):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    try:
        c.execute("INSERT INTO users VALUES (?, ?, ?)", (username, hashed, role))
        conn.commit()
    except:
        return False

    conn.close()
    return True

def login_user(username, password):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    c.execute("SELECT password, role FROM users WHERE username=?", (username,))
    data = c.fetchone()

    conn.close()

    if data:
        stored_password, role = data
        if bcrypt.checkpw(password.encode(), stored_password):
            return role

    return None

# ---------------- LOGIN / SIGNUP ---------------- #
menu = st.sidebar.selectbox("Menu", ["Login", "Signup"])

if menu == "Login":
    st.title("🔐 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        role = login_user(username, password)

        if role:
            st.session_state.logged_in = True
            st.session_state.role = role
            st.success(f"Logged in as {role}")
            st.rerun()
        else:
            st.error("Invalid credentials")

elif menu == "Signup":
    st.title("📝 Signup")

    new_user = st.text_input("Username")
    new_pass = st.text_input("Password", type="password")
    role = st.selectbox("Role", ["user", "developer"])

    if st.button("Signup"):
        if add_user(new_user, new_pass, role):
            st.success("Account created!")
        else:
            st.warning("User already exists")

# ---------------- PROTECTION ---------------- #
if not st.session_state.logged_in:
    st.warning("Please login to continue")
    st.stop()

# ---------------- SIDEBAR ---------------- #
st.sidebar.success(f"Role: {st.session_state.role}")

if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.rerun()

st.sidebar.title("📊 Churn Prediction System")
st.sidebar.markdown("""
Welcome to the ML-powered churn analysis tool.

Use the menu below to navigate:
- 🔮 Predict
- 📊 Dashboard
- 📁 Bulk Upload
- 📈 Model Performance
""")

# ---------------- UI DESIGN ---------------- #
st.markdown("""
<style>
body {
    background-color: #f5f7fa;
}
h1, h2, h3 {
    color: #2c3e50;
}
.stButton>button {
    background-color: #4CAF50;
    color: white;
    border-radius: 8px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HOME PAGE ---------------- #
st.title("📊 Customer Churn Prediction System")

st.markdown("""
### Predict. Analyze. Retain Customers.

This application helps businesses identify customers likely to churn using Machine Learning.
""")

st.write("---")

st.markdown("""
<div style="padding:20px; border-radius:12px; background-color:#eef4ff; box-shadow:0 2px 8px rgba(0,0,0,0.1);">
<h3 style="color:#1f4e79;">💡 Why this tool?</h3>
<p style="color:#333333;">Reduce customer loss by identifying high-risk users early.</p>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.subheader("🔮 Prediction")
    st.write("Predict churn for individual customers.")

with col2:
    st.subheader("📊 Insights")
    st.write("Analyze churn trends with interactive dashboard.")

st.write("---")

st.markdown("## 🔍 About the Project")
st.write("""
This system uses Machine Learning to predict whether a customer will churn or not.  
It helps businesses take proactive actions to retain customers and reduce losses.
""")

st.markdown("## 🚀 Key Features")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("🔮 Prediction")
    st.write("Predict customer churn based on input features.")

with col2:
    st.subheader("📊 Dashboard")
    st.write("Visualize churn trends and customer behavior.")

with col3:
    st.subheader("📁 Bulk Upload")
    st.write("Upload CSV file and predict churn for multiple customers.")

st.markdown("## ⚙️ How It Works")

st.write("""
1. Enter customer details  
2. Model analyzes the data  
3. Get instant churn prediction  
4. Take action based on insights  
""")

st.markdown("## 👉 Get Started")
st.info("Use the sidebar to navigate to Prediction, Dashboard, and other features.")

st.write("---")
st.markdown("Made by Zaved Khan 🚀")