import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import pickle

# Load data
df = pd.read_csv("churn.csv")

# Clean TotalCharges
df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
df = df.dropna()

# Convert target
df["Churn"] = df["Churn"].map({"Yes": 1, "No": 0})

# Encode categorical columns
cat_cols = ["gender", "Partner", "Contract", "InternetService"]

encoders = {}
for col in cat_cols:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    encoders[col] = le

# Features (more inputs now)
X = df[[
    "gender",
    "Partner",
    "Contract",
    "InternetService",
    "tenure",
    "MonthlyCharges",
    "TotalCharges"
]]

y = df["Churn"]

# Train model
model = RandomForestClassifier()
model.fit(X, y)

# Save model + encoders
pickle.dump(model, open("model.pkl", "wb"))
pickle.dump(encoders, open("encoders.pkl", "wb"))

print("✅ Model retrained with more features!")