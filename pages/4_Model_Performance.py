import streamlit as st
if st.session_state.role == "user":
    st.error("Access denied")
    st.stop()
import pandas as pd
import pickle
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

st.set_page_config(layout="wide")

st.title("📈 Model Performance")

# Load model + encoders
@st.cache_resource
def load_files():
    model = pickle.load(open("model.pkl", "rb"))
    encoders = pickle.load(open("encoders.pkl", "rb"))
    return model, encoders

model, encoders = load_files()

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("churn.csv")

    # Clean data
    df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
    df = df.dropna()

    # Target
    df["Churn"] = df["Churn"].map({"Yes": 1, "No": 0})

    # Encode categorical columns (same as training)
    cat_cols = ["gender", "Partner", "Contract", "InternetService"]

    for col in cat_cols:
        df[col] = encoders[col].transform(df[col])

    return df

df = load_data()

# Features (must match training exactly)
X = df[
    [
        "gender",
        "Partner",
        "Contract",
        "InternetService",
        "tenure",
        "MonthlyCharges",
        "TotalCharges",
    ]
]

y = df["Churn"]

# Predictions
y_pred = model.predict(X)

# Metrics
acc = accuracy_score(y, y_pred)
cm = confusion_matrix(y, y_pred)

# UI
st.metric("Accuracy", f"{acc*100:.2f}%")

st.write("### Confusion Matrix")
st.write(cm)

st.write("### Classification Report")
st.text(classification_report(y, y_pred))