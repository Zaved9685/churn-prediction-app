import streamlit as st
if st.session_state.role == "user":
    st.error("Access denied")
    st.stop()
import pandas as pd
import pickle

st.title("📁 Bulk Customer Churn Prediction")
st.info("Upload a CSV with columns: tenure, MonthlyCharges, TotalCharges")

# Load model
@st.cache_resource
def load_model():
    return pickle.load(open("model.pkl", "rb"))

try:
    model = load_model()
except:
    st.error("Model not found. Please train model first.")
    st.stop()

st.write("Upload a CSV file to predict churn for multiple customers.")

st.write("---")

# Upload file
uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)

    st.subheader("📄 Uploaded Data")
    st.write(df.head())

    st.write("---")

    # Check required columns
    required_columns = ["tenure", "MonthlyCharges", "TotalCharges"]

    if all(col in df.columns for col in required_columns):

        # Clean data
        df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
        df = df.dropna()

        # Prediction
        input_data = df[required_columns]

        predictions = model.predict(input_data)

        df["Prediction"] = predictions

        # Convert 0/1 to readable
        df["Prediction"] = df["Prediction"].map({0: "No Churn", 1: "Churn"})

        st.subheader("✅ Prediction Results")
        st.write(df)

        # Download button
        csv = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="📥 Download Results",
            data=csv,
            file_name="churn_predictions.csv",
            mime="text/csv"
        )

    else:
        st.error("CSV must contain columns: tenure, MonthlyCharges, TotalCharges")