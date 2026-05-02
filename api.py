from fastapi import FastAPI
import pickle

app = FastAPI()

# Load model
model = pickle.load(open("model.pkl", "rb"))

@app.get("/")
def home():
    return {"message": "Churn Prediction API is running"}

@app.post("/predict")
def predict(tenure: int, monthly_charges: float, total_charges: float):
    
    input_data = [[tenure, monthly_charges, total_charges]]
    prediction = model.predict(input_data)[0]

    result = "Churn" if prediction == 1 else "No Churn"

    return {"prediction": result}