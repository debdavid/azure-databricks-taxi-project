import streamlit as st
import pandas as pd
import altair as alt

# ---------------------------------------------------------
# 🧠 MODEL CONFIGURATION (The "Brain")
# ---------------------------------------------------------
INTERCEPT = 10.3838
COEF_DISTANCE = 4.6309
COEF_HOUR = 0.0935
COEF_WEEKEND = 0.0693
COEF_PASSENGER = 0.1288

# HOURLY TRENDS (Data from Databricks Gold Layer)
HOURLY_PRICES = [28.91, 25.88, 24.61, 26.37, 32.53, 37.89, 30.28, 26.44, 25.39, 25.86, 
                 26.06, 25.47, 25.74, 26.5, 27.67, 27.41, 29.81, 28.23, 26.94, 27.83, 
                 27.42, 27.66, 28.65, 30.02]

# ---------------------------------------------------------
# 🎨 UI CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(page_title="NYC Taxi Fare Predictor", page_icon="🚖", layout="centered")

# Custom CSS to make it look "Enterprise" (Bigger fonts, cleaner spacing)
st.markdown("""
    <style>
    .big-font { font-size:24px !important; font-weight: bold; }
    .price-tag { font-size: 45px !important; color: #00CC96; font-weight: bold; }
    .sub-text { font-size: 14px; color: #888; }
    </style>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------
# 🚀 HEADER SECTION
# ---------------------------------------------------------
st.title("🚖 NYC Taxi Fare Predictor")
st.markdown("#### AI-Powered Trip Estimation Engine")
st.markdown("Use the controls below to simulate a trip. The model utilizes historical data from **2.7 million rides** to predict your fare.")
st.divider()

# ---------------------------------------------------------
# 🎛️ CONTROLS SECTION
# ---------------------------------------------------------
st.subheader("1️⃣ Trip Details")

col1, col2 = st.columns(2)

with col1:
    # DISTANCE: Clearer labels with "Miles"
    distance = st.slider("📏 Trip Distance (Miles)", 0.5, 50.0, 5.0, step=0.5)
    
    # PASSENGERS: Clean number input
    passengers = st.number_input("Passengers", 1, 6, 1)

with col2:
    # TIME: Converted to AM/PM for "Adult" readability
    time_options = ["12 AM", "1 AM", "2 AM", "3 AM", "4 AM", "5 AM", "6 AM", "7 AM", 
                    "8 AM", "9 AM", "10 AM", "11 AM", "12 PM", "1 PM", "2 PM", "3 PM", 
                    "4 PM", "5 PM", "6 PM", "7 PM", "8 PM", "9 PM", "10 PM", "11 PM"]
    
    time_label = st.select_slider("⏰ Pickup Time", options=time_options, value="2 PM")
    
    # Map label back to 0-23 integer for the math
    hour = time_options.index(time_label)

    # DAY TYPE: Professional Segmented Control
    day_type = st.radio("📅 Day Type", ["Weekday (Mon-Fri)", "Weekend (Sat-Sun)"], horizontal=True)
    is_weekend = 1 if "Weekend" in day_type else 0

# ---------------------------------------------------------
# 🧮 CALCULATION ENGINE
# ---------------------------------------------------------
def predict_fare(dist, hr, weekend, pax):
    day_val = 7 if weekend else 2
    
    # The Math
    cost_base = INTERCEPT
    cost_dist = dist * COEF_DISTANCE
    cost_time = hr * COEF_HOUR
    cost_extra = (day_val * COEF_WEEKEND) + (pax * COEF_PASSENGER)
    
    total = cost_base + cost_dist + cost_time + cost_extra
    return max(5.0, total), cost_base, cost_dist, cost_time, cost_extra

# Run Inference
price, c_base, c_dist, c_time, c_extra = predict_fare(distance, hour, is_weekend, passengers)

# ---------------------------------------------------------
# 💵 RESULTS SECTION
# ---------------------------------------------------------
st.divider()
st.subheader("2️⃣ Fare Estimate")

# Use columns to center the price
c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    st.markdown(f'<p class="price-tag">${price:.2f}</p>', unsafe_allow_html=True)
    st.markdown(f"**Estimated for {distance} miles at {time_label}**")

st.divider()

# ---------------------------------------------------------
# 📊 INSIGHTS SECTION (The "Glass Box")
# ---------------------------------------------------------
st.subheader("3️⃣ Why this Price?")
st.markdown("Breakdown of the cost drivers based on our analytics engine.")

tab1, tab2 = st.tabs(["💰 Cost Breakdown", "📈 Hourly Trends"])

with tab1:
    # Clean Bar Chart
    breakdown_data = pd.DataFrame({
        "Component": ["Base Rate", "Distance Cost", "Time/Traffic", "Surcharges"],
        "Amount ($)": [c_base, c_dist, c_time, c_extra]
    })
    
    chart = alt.Chart(breakdown_data).mark_bar().encode(
        x=alt.X('Component', sort="-y"),
        y='Amount ($)',
        tooltip=['Component', 'Amount ($)'],
        color=alt.value("#00CC96")  # BCG Green
    ).properties(height=300)
    
    st.altair_chart(chart, use_container_width=True)

with tab2:
    # Hourly Trend Line
    trend_data = pd.DataFrame({
        "Hour": range(24),
        "Avg Fare ($)": HOURLY_PRICES
    })
    
    # Base Line
    line = alt.Chart(trend_data).mark_line(color='#808080').encode(
        x='Hour', 
        y='Avg Fare ($)'
    )
    
    # Red Dot for Current Selection
    point = alt.Chart(pd.DataFrame({'Hour': [hour], 'Avg Fare ($)': [HOURLY_PRICES[hour]]}))\
        .mark_point(color='#FF4B4B', size=150, filled=True)\
        .encode(x='Hour', y='Avg Fare ($)')
        
    st.altair_chart(line + point, use_container_width=True)
    st.caption(f"The red dot shows the average market rate for {time_label}.")
