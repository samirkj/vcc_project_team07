import streamlit as st
import matplotlib.pyplot as plt
import requests
import pandas as pd

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


# Load historical predictions
daily_df = pd.read_csv("daily_df.csv", parse_dates=["Date"], index_col="Date")

# Load future predictions
future_preds_df = pd.read_csv("future_preds.csv", parse_dates=["Date"], index_col="Date")

st.markdown("---")
import matplotlib.pyplot as plt
import streamlit as st

st.subheader("Actual vs Historical Prediction vs Future Forecast")

# Combine past 30 days actual and predicted, and future forecast
past_actual = daily_df[['Price']].iloc[-30:]
past_predicted = daily_df[['Predicted_Price']].iloc[-30:].rename(columns={'Predicted_Price': 'Price'})
future_forecast = future_preds_df.rename(columns={'Predicted_Price': 'Price'})

# Start plotting
fig, ax = plt.subplots(figsize=(12, 5))

# Plot actual price
ax.plot(past_actual.index, past_actual['Price'], label="Actual", color='blue', linewidth=2)

# Plot historical predicted price (dashed)
ax.plot(past_predicted.index, past_predicted['Price'], label="Predicted (Historical)", color='orange', linestyle='--', linewidth=2)

# Plot forecasted price (dotted)
ax.plot(future_forecast.index, future_forecast['Price'], label="Forecast (Next 10 Days)", color='green', linestyle=':', linewidth=2)

# Add prediction start marker
ax.axvline(daily_df.index[-1], color='red', linestyle='--', label="Prediction Start")

ax.set_title("Gold Price: Actual vs Historical Predictions vs Future Forecast")
ax.set_xlabel("Date")
ax.set_ylabel("Price")
ax.legend()
ax.grid(True)
plt.xticks(rotation=45)

st.pyplot(fig)

st.markdown("---")

st.subheader("Next 10 Days - Gold Price Forecast")

# Round for display
future_preds_display = future_preds_df.copy()
future_preds_display['Predicted_Price'] = future_preds_display['Predicted_Price'].round(2)

st.dataframe(
    future_preds_display.style
    .format("{:.2f}")
    .set_properties(**{'text-align': 'center'}),
    use_container_width=True
)

