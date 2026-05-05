##5_My_Analysis.py

import streamlit as st
import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm

st.title("My Analysis - GDP Growth and Sentiment Data")

#Import my data set
data = pd.read_csv("merged_gdp_sentiment_data.csv", skiprows=1, index_col='DATE', parse_dates=True)

# Flatten MultiIndex columns
if isinstance(data.columns, pd.MultiIndex):
    data.columns = data.columns.get_level_values(1)

# Ensure 'year' column exists for filtering
data['year'] = data.index.year


#Choose period
period = st.radio(
    "Choose period:",
    ["All data", "Great Recession (2008–2009)", "Great Lockdown (2020)"]
)

# Filter data
if period == "Great Recession (2008–2009)":
    df = data[(data["year"] >= 2008) & (data["year"] <= 2009)]
elif period == "Great Lockdown (2020)":
    df = data[data["year"] == 2020]
else:
    df = data

# Regression
df = df.dropna(subset=["gdp_growth", "sentiment_quarterly"])
X = sm.add_constant(df["sentiment_quarterly"])
y = df["gdp_growth"]
model = sm.OLS(y, X).fit()

# Extract original sentiment coefficient and intercept
original_sentiment_beta = model.params['sentiment_quarterly']
intercept = model.params['const']
mean_sentiment = df['sentiment_quarterly'].mean()

# Add slider for sentiment coefficient adjustment
st.subheader("Adjust Sentiment Coefficient")
adjustment_percentage = st.slider(
    "Adjust sentiment coefficient by percentage:",
    min_value=-100,
    max_value=100,
    value=0,
    step=5,
    format='%d%%'
)

# Calculate adjusted sentiment coefficient
adjusted_sentiment_beta = original_sentiment_beta * (1 + adjustment_percentage / 100)

# Calculate nowcast value based on adjusted coefficient and mean sentiment
nowcast_gdp_growth = intercept + adjusted_sentiment_beta * mean_sentiment

# Display the nowcast using st.metric
st.metric("Nowcast GDP Growth", f"{nowcast_gdp_growth:.2f}%")

# Display results
st.subheader("Estimated Coefficient on Sentiment (Adjusted)")
st.write(f"Original: {original_sentiment_beta:.4f}, Adjusted: {adjusted_sentiment_beta:.4f}")

st.subheader("Regression Summary")
st.text(model.summary())

# Plot
st.subheader("GDP Growth and Sentiment Over Time")
st.line_chart(df[["gdp_growth", "sentiment_quarterly"]])
