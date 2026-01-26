import streamlit as st
import pandas as pd
import altair as alt

# ---------------------------------------------------------
# 🧠 AGENT BRAIN (Model Weights)
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
# 🎨 UI & MODERN DESIGN
# ---------------------------------------------------------
st.set_page_config(page_title="NYC Pricing Agent", page_icon="🚖", layout="centered")

st.markdown("""
    <style>
    /* Modern Background */
    .stApp { background: linear-gradient(135deg, #f5f7fa 0%, #e4f0e8 100%); }
    
    /* Cards */
    div.css-1r6slb0, div.css-12oz5g7 {
        background-color: white;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        border: 1px solid #e0e0e0;
    }
    
    /* Typography */
    h1, h2, h3 { font-family: 'Helvetica Neue', sans-serif; color: #2c3e50; }
    
    /* Price Card */
    .price-card {
        background-color: #ffffff;
        border-left: 6px solid #179758;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    .price-main {
        font-size: 42px;
        font-weight: 800;
        color: #179758;
        margin: 0;
        line-height: 1.2;
    }
    .price-sub {
        font-size: 14px;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: #888;
        font-weight: 600;
    }
    
    /* Disclaimer */
    .disclaimer {
        font-size: 12px;
        color: #888;
        margin-top: 50px;
        text-align: center;
        border-top: 1px solid #ddd;
        padding-top: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("NYC Fair Price Auditor")
st.markdown("#### 🛡️ AI-Powered Price Protection")
st.markdown("Don't overpay. This agent analyses **2.7 million historical trips** to calculate a fair price range for your journey.")
st.divider()

# ---------------------------------------------------------
# 🎛️ INPUTS
# ---------------------------------------------------------
st.subheader("1. Journey Details")
col1, col2 = st.columns(2)

with col1:
    distance = st.slider("📏 Distance (Miles)", 0.5, 50.0, 5.0, step=0.5)
    passengers = st.number_input("👥 Passengers", 1, 6, 1)

with col2:
    time_options = ["12 AM", "1 AM", "2 AM", "3 AM", "4 AM", "5 AM", "6 AM", "7 AM", 
                    "8 AM", "9 AM", "10 AM", "11 AM", "12 PM", "1 PM", "2 PM", "3 PM", 
                    "4 PM", "5 PM", "6 PM", "7 PM", "8 PM", "9 PM", "10 PM", "11 PM"]
    time_label = st.select_slider("⏰ Time of Day", options=time_options, value="2 PM")
    hour = time_options.index(time_label)
    
    day_type = st.radio("📅 Day Type", ["Weekday", "Weekend"], horizontal=True)
    is_weekend = 1 if day_type == "Weekend" else 0

# ---------------------------------------------------------
# 🧠 LOGIC ENGINE
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

low_range = price * 0.95 
high_range = price * 1.15 

# ---------------------------------------------------------
# 🏁 AUDIT REPORT (The "Smart" Part)
# ---------------------------------------------------------
st.divider()
st.subheader("2. Audit Result")

c1, c2 = st.columns([1.2, 1])

with c1:
    st.markdown(f"""
    <div class="price-card">
        <div class="price-sub">Fair Price Range</div>
        <div class="price-main">${low_range:.2f} - ${high_range:.2f}</div>
        <div style="color: #666; font-size: 14px; margin-top: 5px;">
            Target Estimate: <b>${price:.2f}</b>
        </div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    # --- INTELLIGENT ADVICE LOGIC ---
    if distance < 1.5:
        msg = "🚶 **Walkable Distance:** For trips under 1.5 miles, walking or cycling is often faster than sitting in NYC traffic."
        icon = "info"
    elif distance > 20:
        msg = "✈️ **Long Haul:** For airport trips (JFK/EWR), check if a flat-rate 'Airport Fare' applies before accepting the meter."
        icon = "warning"
    elif 16 <= hour <= 19 and not is_weekend:
        msg = "🚦 **Rush Hour:** Heavy congestion detected (4PM-7PM). Expect the higher end of the price range."
        icon = "warning"
    elif 0 <= hour <= 4:
        msg = "🌙 **Night Owl:** Low traffic expected, but driver availability may be lower. Price surcharges are minimal."
        icon = "success"
    else:
        msg = "✅ **Standard Rate:** Current conditions align with standard market averages. Proceed with confidence."
        icon = "success"

    if icon == "warning":
        st.warning(msg)
    elif icon == "info":
        st.info(msg)
    else:
        st.success(msg)

# ---------------------------------------------------------
# 📊 TRANSPARENCY
# ---------------------------------------------------------
st.divider()
st.subheader("3. Cost Transparency")

tab1, tab2 = st.tabs(["💵 Cost Breakdown", "📈 Market Trends"])

with tab1:
    # RENAMED "Time/Traffic Adj." to "Time Fee"
    breakdown_data = pd.DataFrame({
        "Component": ["Distance Rate", "Base Fare", "Time Fee", "Surcharges"],
        "Cost ($)": [c_dist, c_base, c_time, c_extra]
    })
    
    chart = alt.Chart(breakdown_data).mark_bar(cornerRadiusTopLeft=5, cornerRadiusTopRight=5).encode(
        x=alt.X('Component', sort="-y", title=None),
        y=alt.Y('Cost ($)', title=None),
        color=alt.value("#179758"),
        tooltip=['Component', 'Cost ($)']
    ).properties(height=200)
    
    st.altair_chart(chart, use_container_width=True)

with tab2:
    trend_df = pd.DataFrame({"Hour": range(24), "Avg Fare": HOURLY_PRICES})
    
    line = alt.Chart(trend_df).mark_line(color='#179758', strokeWidth=3).encode(
        x=alt.X('Hour', title="Hour of Day"),
        y=alt.Y('Avg Fare', title="Average Market Rate ($)")
    )
    
    point_df = pd.DataFrame({'Hour': [hour], 'Avg Fare': [HOURLY_PRICES[hour]]})
    point = alt.Chart(point_df).mark_point(fill='red', color='red', size=100).encode(
        x='Hour',
        y='Avg Fare'
    )
    
    st.altair_chart(line + point, use_container_width=True)
    st.caption(f"🔴 Red dot shows the average market rate for {time_label}.")

# ---------------------------------------------------------
# ⚖️ DISCLAIMER
# ---------------------------------------------------------
st.markdown("""
    <div class="disclaimer">
        <b>Data Transparency Statement:</b><br>
        This AI model was trained on NYC Taxi & Limousine Commission (TLC) trip record data from <b>January 2024</b>. 
        Estimates are based on historical patterns and linear regression weights. 
        Actual real-world fares may vary due to live traffic, weather conditions, or new regulatory surcharges.
    </div>
    """, unsafe_allow_html=True)
