import streamlit as st
import requests

st.set_page_config(page_title="Gold Price Predictor", layout="wide")

st.title("Gold Price Forecasting by VCC Project Team 07")
st.markdown("Provide the latest technical indicators to predict tomorrow's gold price.")

# Create 3 columns
col1, col2, col3 = st.columns(3)

with col1:
    price = st.number_input("Price (Today)", value=3351.5)
    return_1 = st.number_input("Return_1 (1-day % Change)", value=0.0)
    momentum_3 = st.number_input("Momentum_3", value=39.9)

with col2:
    ma_3 = st.number_input("MA_3 (3-day MA)", value=3341.63)
    volatility_7 = st.number_input("Volatility_7 (7-day STD)", value=19.04)
    roc_3 = st.number_input("ROC_3 (3-day % Change)", value=0.01)

with col3:
    ma_7 = st.number_input("MA_7", value=3329.74)
    ma_14 = st.number_input("MA_14", value=3325.23)
    rsi_14 = st.number_input("RSI_14", value=56.92)

# Aggregate features in correct order
features = [
    round(price, 2),
    round(ma_3, 2),
    round(ma_7, 2),
    round(ma_14, 2),
    round(return_1, 4),
    round(volatility_7, 2),
    round(momentum_3, 2),
    round(roc_3, 4),
    round(rsi_14, 2)
]

st.markdown("---")

if st.button("Predict Gold Price"):
    api_url = "https://gold-predictor-449957159975.asia-south1.run.app/predict"
    payload = {"features": features}

    try:
        response = requests.post(api_url, json=payload, timeout=10)
        response.raise_for_status()
        predicted_price = response.json().get("predicted_price")
        st.success(f"Predicted Gold Price: **${predicted_price}**")
    except Exception as e:
        st.error(f"Prediction failed: {e}")
