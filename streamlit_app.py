import streamlit as st
import pandas as pd
import altair as alt

# ---------------------------------------------------------
# 🧠 MODEL & DATA ASSETS
# ---------------------------------------------------------
# 1. Model Weights (From Phase 6)
INTERCEPT = 10.3838
COEF_DISTANCE = 4.6309
COEF_HOUR = 0.0935
COEF_WEEKEND = 0.0693
COEF_PASSENGER = 0.1288

# 2. Gold Layer Insights (Actual Data)
HOURLY_PRICES = [28.91, 25.88, 24.61, 26.37, 32.53, 37.89, 30.28, 26.44, 25.39, 25.86, 
                 26.06, 25.47, 25.74, 26.5, 27.67, 27.41, 29.81, 28.23, 26.94, 27.83, 
                 27.42, 27.66, 28.65, 30.02]

# ---------------------------------------------------------
# 🎨 APP LAYOUT
# ---------------------------------------------------------
st.set_page_config(page_title="NYC Taxi AI Agent", page_icon="🚖", layout="centered")

st.title("🚖 NYC Taxi Fare Predictor")
st.markdown("""**Plan your trip budget instantly.** This AI Agent analyzes millions of historical NYC rides to estimate your fare in real-time.""")
st.divider()

# 📝 INPUT SECTION
col1, col2 = st.columns(2)
with col1:
    distance = st.slider("Trip Distance (miles)", 0.5, 50.0, 5.0, step=0.5)
    hour = st.slider("Pickup Hour (24h format)", 0, 23, 14)
with col2:
    is_weekend = st.checkbox("Is it a Weekend?", value=False)
    passengers = st.number_input("Passengers", 1, 6, 1)

# 🧮 INFERENCE ENGINE
def predict_fare(dist, hr, weekend, pax):
    day_val = 7 if weekend else 2
    
    # Calculate components for the breakdown chart
    cost_base = INTERCEPT
    cost_dist = dist * COEF_DISTANCE
    cost_time = hr * COEF_HOUR
    cost_extra = (day_val * COEF_WEEKEND) + (pax * COEF_PASSENGER)
    
    total = cost_base + cost_dist + cost_time + cost_extra
    return max(5.0, total), cost_base, cost_dist, cost_time, cost_extra

price, c_base, c_dist, c_time, c_extra = predict_fare(distance, hour, is_weekend, passengers)

# 🏁 RESULT SECTION
st.divider()
st.subheader(f"🤖 Agent Estimate: ${price:.2f}")

# ---------------------------------------------------------
# 📊 NEW: DATA INSIGHTS SECTION
# ---------------------------------------------------------
with st.expander("🔎 See Data Insights (Why this price?)", expanded=True):
    
    # Insight 1: Cost Breakdown (Stacked Bar)
    st.markdown("### 1. Cost Breakdown")
    st.write("Where does your money go?")
    
    breakdown_data = pd.DataFrame({
        "Component": ["Base Fare", "Distance", "Time/Traffic", "Surcharges"],
        "Cost": [c_base, c_dist, c_time, c_extra]
    })
    st.bar_chart(breakdown_data.set_index("Component"))

    # Insight 2: Hourly Trends (Line Chart)
    st.markdown("### 2. Market Trends")
    st.write("Average NYC taxi fares by hour of day (Historical Data):")
    
    trend_data = pd.DataFrame({
        "Hour": range(24),
        "Average Fare": HOURLY_PRICES
    })
    
    # Highlight the user's selected hour
    c = alt.Chart(trend_data).mark_line(color='#FF4B4B').encode(
        x='Hour', 
        y='Average Fare',
        tooltip=['Hour', 'Average Fare']
    )
    
    point = alt.Chart(pd.DataFrame({'Hour': [hour], 'Average Fare': [HOURLY_PRICES[hour]]})).mark_point(color='red', size=100, filled=True).encode(x='Hour', y='Average Fare')
    
    st.altair_chart(c + point, use_container_width=True)
    st.caption("🔴 Red dot indicates your selected pickup time.")
