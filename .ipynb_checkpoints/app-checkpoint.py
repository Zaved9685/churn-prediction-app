import streamlit as st

# Page config
st.set_page_config(
    page_title="Customer Churn Prediction",
    page_icon="📊",
    layout="wide"
)

# Custom CSS for styling
st.markdown("""
    <style>
    .main {
        background-color: #f5f7fa;
    }
    .title {
        font-size: 40px;
        font-weight: bold;
        color: #2c3e50;
    }
    .subtitle {
        font-size: 20px;
        color: #7f8c8d;
    }
    .section {
        margin-top: 40px;
    }
    </style>
""", unsafe_allow_html=True)

# HEADER
st.markdown('<div class="title">📊 Customer Churn Prediction System</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Predict which customers are likely to leave your business</div>', unsafe_allow_html=True)

st.write("---")

# ABOUT SECTION
st.markdown("## 🔍 About the Project")
st.write("""
This system uses Machine Learning to predict whether a customer will churn or not.  
It helps businesses take proactive actions to retain customers and reduce losses.
""")

# FEATURES SECTION
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

# HOW IT WORKS
st.markdown("## ⚙️ How It Works")

st.write("""
1. Enter customer details  
2. Model analyzes the data  
3. Get instant churn prediction  
4. Take action based on insights  
""")

# CALL TO ACTION
st.markdown("## 👉 Get Started")
st.info("Use the sidebar to navigate to Prediction, Dashboard, and other features.")