import streamlit as st
import pandas as pd
import altair as alt

# ---------------------------------------------------------
# 🧠 AGENT BRAIN (Model & Data)
# ---------------------------------------------------------
INTERCEPT = 10.3838
COEF_DISTANCE = 4.6309
COEF_HOUR = 0.0935
COEF_WEEKEND = 0.0693
COEF_PASSENGER = 0.1288
HOURLY_PRICES = [28.91, 25.88, 24.61, 26.37, 32.53, 37.89, 30.28, 26.44, 25.39, 25.86, 
                 26.06, 25.47, 25.74, 26.5, 27.67, 27.41, 29.81, 28.23, 26.94, 27.83, 
                 27.42, 27.66, 28.65, 30.02]

# ---------------------------------------------------------
# 🎨 UI CONFIGURATION (Clean Professional Light Theme)
# ---------------------------------------------------------
st.set_page_config(page_title="NYC Pricing Agent", page_icon="🚖", layout="centered")

# Custom CSS for "BCG Style" Professionalism
st.markdown("""
    <style>
    .main {
        background-color: #FFFFFF;
    }
    h1 {
        color: #000000;
        font-family: 'Helvetica Neue', sans-serif;
    }
    .price-box { 
        padding: 20px; 
        background-color: #f8f9fa; 
        border-left: 5px solid #179758; /* Green Accent */
        border-radius: 5px;
    }
    .price-large {
        font-size: 42px;
        font-weight: bold;
        color: #179758;
        margin: 0;
    }
    .price-label {
        font-size: 14px;
        color: #666;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .agent-insight {
        background-color: #e8f5e9;
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #c8e6c9;
        color: #2e7d32;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("NYC Fair Price Auditor")
st.markdown("#### AI-Powered Fare Protection Engine")
st.markdown("This agent analyses millions of historical trips to calculate a **fair price range**, helping you identify overpriced quotes or surge pricing.")
st.divider()

# ---------------------------------------------------------
# 🎛️ INPUTS
# ---------------------------------------------------------
st.subheader("1. Trip Context")
col1, col2 = st.columns(2)

with col1:
    distance = st.slider("Distance (Miles)", 0.5, 50.0, 5.0, step=0.5)
    passengers = st.number_input("Passengers", 1, 6, 1)

with col2:
    time_options = ["12 AM", "1 AM", "2 AM", "3 AM", "4 AM", "5 AM", "6 AM", "7 AM", 
                    "8 AM", "9 AM", "10 AM", "11 AM", "12 PM", "1 PM", "2 PM", "3 PM", 
                    "4 PM", "5 PM", "6 PM", "7 PM", "8 PM", "9 PM", "10 PM", "11 PM"]
    time_label = st.select_slider("Time of Day", options=time_options, value="2 PM")
    hour = time_options.index(time_label)
    
    day_type = st.radio("Day Type", ["Weekday", "Weekend"], horizontal=True)
    is_weekend = 1 if day_type == "Weekend" else 0

# ---------------------------------------------------------
# 🧠 CALCULATION LOGIC
# ---------------------------------------------------------
def calculate_fare(dist, hr, weekend, pax):
    day_val = 7 if weekend else 2
    c_base = INTERCEPT
    c_dist = dist * COEF_DISTANCE
    c_time = hr * COEF_HOUR
    c_extra = (day_val * COEF_WEEKEND) + (pax * COEF_PASSENGER)
    total = c_base + c_dist + c_time + c_extra
    return max(5.0, total), c_base, c_dist, c_time, c_extra

price, c_base, c_dist, c_time, c_extra = calculate_fare(distance, hour, is_weekend, passengers)

# AGENT LOGIC: Calculate "Range" (Standard vs. Heavy Traffic/Surge Risk)
low_range = price * 0.95  # Best case
high_range = price * 1.15 # Traffic variance

# ---------------------------------------------------------
# 🏁 OUTPUT SECTION
# ---------------------------------------------------------
st.divider()
st.subheader("2. Agent Assessment")

c1, c2 = st.columns([1.2, 1])

with c1:
    st.markdown(f"""
    <div class="price-box">
        <div class="price-label">Fair Price Range</div>
        <div class="price-large">${low_range:.2f} - ${high_range:.2f}</div>
        <div style="margin-top: 10px; font-size: 14px; color: #555;">
            Target Estimate: <b>${price:.2f}</b>
        </div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    # Contextual Advice based on Price
    if price > 50:
        advice = "⚠️ **High Fare Alert:** This is a long-distance trip. Negotiate a flat rate if possible."
    elif c_time > 2.0:
        advice = "🕒 **Traffic Warning:** High time-based charges detected. Expect variability."
    else:
        advice = "✅ **Standard Fare:** This quote is consistent with historical averages."
        
    st.markdown(f"""
    <div class="agent-insight">
        <b>🤖 Agent Insight:</b><br>
        {advice}
    </div>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------
# 📊 VISUALISATION (Fixed Error)
# ---------------------------------------------------------
st.divider()
st.subheader("3. Cost Transparency")

tab1, tab2 = st.tabs(["Cost Breakdown", "Market Trends"])

with tab1:
    breakdown_data = pd.DataFrame({
        "Driver": ["Distance Cost", "Base Rate", "Time/Traffic Adj.", "Surcharges"],
        "Cost ($)": [c_dist, c_base, c_time, c_extra]
    })
    
    chart = alt.Chart(breakdown_data).mark_bar(color='#179758').encode(
        x=alt.X('Driver', sort="-y", title="Cost Component"),
        y=alt.Y('Cost ($)', title="Amount ($)"),
        tooltip=['Driver', 'Cost ($)']
    )
    st.altair_chart(chart, use_container_width=True)

with tab2:
    # SEPARATE CHARTS to avoid Layer Error
    st.write("Average Price Curve (24h):")
    
    trend_data = pd.DataFrame({"Hour": range(24), "Avg Fare": HOURLY_PRICES})
    
    # 1. The Line Chart
    line = alt.Chart(trend_data).mark_line(color='#179758', strokeWidth=3).encode(
        x=alt.X('Hour', title="Hour of Day"),
        y=alt.Y('Avg Fare', title="Average Market Rate ($)")
    )
    
    # 2. The Point (Current Selection)
    current_point = pd.DataFrame({'Hour': [hour], 'Avg Fare': [HOURLY_PRICES[hour]]})
    point = alt.Chart(current_point).mark_point(
        color='#d32f2f', 
        size=200, 
        filled=True
    ).encode(
        x='Hour',
        y='Avg Fare',
        tooltip=alt.value("Your Selection")
    )
    
    # Combine safely
    st.altair_chart(line + point, use_container_width=True)
    st.caption(f"The red dot indicates the average market rate for {time_label}.")
