import streamlit as st
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Please login first")
    st.stop()
import pickle
# Page config
st.set_page_config(layout="wide")

# Load model and encoders
@st.cache_resource
def load_files():
    model = pickle.load(open("model.pkl", "rb"))
    encoders = pickle.load(open("encoders.pkl", "rb"))
    return model, encoders

model, encoders = load_files()

# Title
st.title("🔮 Customer Churn Prediction")

st.write("Enter customer details below:")

st.write("---")

# INPUTS
gender = st.selectbox("Gender", ["Male", "Female"])
partner = st.selectbox("Partner", ["Yes", "No"])
contract = st.selectbox("Contract", ["Month-to-month", "One year", "Two year"])
internet = st.selectbox("Internet Service", ["DSL", "Fiber optic", "No"])

tenure = st.slider("Tenure (months)", 0, 72, 12)
monthly = st.number_input("Monthly Charges", 0.0, 200.0, 50.0)
total = st.number_input("Total Charges", 0.0, 10000.0, 500.0)

st.write("---")

# PREDICT BUTTON
if st.button("Predict"):

    # Encode inputs
    input_data = [
        encoders["gender"].transform([gender])[0],
        encoders["Partner"].transform([partner])[0],
        encoders["Contract"].transform([contract])[0],
        encoders["InternetService"].transform([internet])[0],
        tenure,
        monthly,
        total
    ]

    # Prediction with loader
    with st.spinner("Analyzing customer data..."):
        prediction = model.predict([input_data])[0]

    # RESULT
    if prediction == 1:
        st.markdown("### ⚠️ High Risk Customer")
        st.error("This customer is likely to churn.")
    else:
        st.markdown("### ✅ Low Risk Customer")
        st.success("This customer is likely to stay.")