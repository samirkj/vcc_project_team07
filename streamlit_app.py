import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
from datetime import timedelta

st.set_page_config(page_title="Gold Forecast - VCC Project", layout="wide")

# Load historical data
daily_df = pd.read_csv("daily_df.csv", parse_dates=["Date"], index_col="Date")

# If 'Predicted_Price' not in daily_df, fill with NaNs
if 'Predicted_Price' not in daily_df.columns:
    daily_df['Predicted_Price'] = np.nan

API_URL = "https://vcc-project-team07-449957159975.asia-south1.run.app/predict"

st.title("Gold Price Forecast")

today_price = st.number_input("Enter Today’s Gold Price (₹)", min_value=0.0, value=3500.0, format="%.2f")

if st.button("Predict Gold Price"):
    future_df = daily_df.copy()
    last_known_date = future_df.index[-1]
    current_date = last_known_date + timedelta(days=1)

    # Add today's price
    while current_date.weekday() >= 5:
        current_date += timedelta(days=1)

    future_df.loc[current_date] = np.nan
    future_df.at[current_date, 'Price'] = today_price

    future_preds = []

    for _ in range(10):
        temp_df = future_df.copy()

        ma_3 = temp_df['Price'].iloc[-3:].mean()
        ma_7 = temp_df['Price'].iloc[-7:].mean()
        ma_14 = temp_df['Price'].iloc[-14:].mean()
        return_1 = temp_df['Price'].pct_change().iloc[-1]
        volatility_7 = temp_df['Price'].iloc[-7:].std()
        momentum_3 = temp_df['Price'].iloc[-1] - temp_df['Price'].iloc[-4]
        roc_3 = (temp_df['Price'].iloc[-1] - temp_df['Price'].iloc[-4]) / temp_df['Price'].iloc[-4]

        delta = temp_df['Price'].diff()
        gain = delta.clip(lower=0).rolling(14).mean().iloc[-1]
        loss = -delta.clip(upper=0).rolling(14).mean().iloc[-1]
        rs = gain / loss if loss != 0 else 0
        rsi_14 = 100 - (100 / (1 + rs))

        feature_row = [round(today_price, 2), round(ma_3, 2), round(ma_7, 2), round(ma_14, 2),
                       round(return_1, 4), round(volatility_7, 2), round(momentum_3, 2),
                       round(roc_3, 4), round(rsi_14, 2)]

        response = requests.post(API_URL, json={"features": feature_row})
        predicted_price = response.json()['predicted_price']

        next_date = temp_df.index[-1] + timedelta(days=1)
        while next_date.weekday() >= 5:
            next_date += timedelta(days=1)

        new_row = pd.DataFrame([{
            'Price': predicted_price
        }], index=[next_date])

        future_df = pd.concat([future_df, new_row])
        future_preds.append((next_date, predicted_price))
        today_price = predicted_price

    # Show tomorrow's prediction
    st.success(f"Predicted Gold Price for Tomorrow: ₹{future_preds[0][1]:.2f}")

    st.markdown("---")
    st.subheader("Actual + Historical + 10-Day Forecast")

    past_actual = daily_df[['Price']].iloc[-60:]
    past_predicted = daily_df[['Predicted_Price']].iloc[-60:].rename(columns={'Predicted_Price': 'Price'})
    future_forecast = pd.DataFrame(future_preds, columns=["Date", "Price"]).set_index("Date")

    fig, ax = plt.subplots(figsize=(14, 6))
    ax.plot(past_actual.index, past_actual['Price'], label="Actual", color='blue')
    ax.plot(past_predicted.index, past_predicted['Price'], label="Predicted (Historical)", color='orange', linestyle='--')
    ax.plot(future_forecast.index, future_forecast['Price'], label="Forecast (Next 10D)", color='green', linestyle=':')
    ax.axvline(daily_df.index[-1], color='red', linestyle='--', label="Prediction Start")
    ax.set_title("Gold Price: Last 60 Days + 10-Day Forecast")
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    ax.grid(True)
    ax.legend()
    st.pyplot(fig)

    st.markdown("---")
    st.subheader("Forecast Table - Next 10 Business Days")
    future_forecast['Price'] = future_forecast['Price'].round(2)
    st.table(future_forecast)
