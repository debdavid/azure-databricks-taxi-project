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
# 🎨 UI & MODERN DESIGN CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(page_title="NYC Pricing Agent", page_icon="🚖", layout="centered")

st.markdown("""
    <style>
    /* --- 1. CLEAN EXECUTIVE BACKGROUND (The "Green Shade" you liked) --- */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #e4f0e8 100%);
    }
    
    /* --- 2. THE MEDALLION LOGO --- */
    .medallion {
        background-color: #f1c40f; /* Taxi Yellow */
        color: #000000;
        width: 90px;
        height: 90px;
        border-radius: 18px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 800;
        font-size: 26px;
        line-height: 1.1;
        text-align: center;
        box-shadow: 0 6px 0px #c29d0b;
        border: 3px solid #000000;
        margin: auto;
    }
    
    /* --- 3. CARDS & CONTAINERS --- */
    div.css-1r6slb0, div.css-12oz5g7 {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 25px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05); /* Soft shadow */
        border: 1px solid #e1e4e8;
    }
    
    /* Typography */
    h1 { letter-spacing: -1px; color: #1a252f; font-weight: 700;}
    h3 { font-size: 14px; text-transform: uppercase; color: #7f8c8d; letter-spacing: 1.5px; font-weight: 700; border-bottom: 2px solid #eee; padding-bottom: 10px; margin-bottom: 20px; }

    /* Price Card */
    .price-card {
        background: linear-gradient(135deg, #ffffff 0%, #f0fff4 100%);
        border-left: 6px solid #179758;
        padding: 25px;
        border-radius: 10px;
        box-shadow: 0 4px 15px rgba(23, 151, 88, 0.1);
    }
    .price-main {
        font-size: 48px;
        font-weight: 800;
        color: #179758;
        margin: 0;
        line-height: 1.1;
    }
    .price-sub {
        font-size: 13px;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        color: #2c3e50;
        font-weight: 700;
    }
    
    /* Disclaimer */
    .disclaimer {
        font-size: 11px;
        color: #95a5a6;
        margin-top: 50px;
        text-align: center;
        background-color: rgba(255,255,255,0.5);
        padding: 20px;
        border-radius: 8px;
        border: 1px solid #ddd;
    }
    </style>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------
# 🚕 HEADER SECTION
# ---------------------------------------------------------
h_col1, h_col2 = st.columns([1, 4])

with h_col1:
    st.markdown("""
        <div class="medallion">
            NYC<br>TAXI
        </div>
    """, unsafe_allow_html=True)

with h_col2:
    st.title("NYC Price Check")
    st.markdown("**AI-Powered Fair Fare Estimator**")
    st.caption("Compare your potential trip cost against historical market data.")

st.divider()

# ---------------------------------------------------------
# 🎛️ INPUTS
# ---------------------------------------------------------
st.markdown("### 1. Trip Details")
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
# 🏁 ASSESSMENT REPORT
# ---------------------------------------------------------
st.divider()
st.markdown("### 2. Price Check Result")

c1, c2 = st.columns([1.3, 1])

with c1:
    st.markdown(f"""
    <div class="price-card">
        <div class="price-sub">Typical Market Range</div>
        <div class="price-main">${low_range:.2f} - ${high_range:.2f}</div>
        <div style="color: #555; font-size: 14px; margin-top: 8px; font-weight: 500;">
            Estimated Fair Price: <b>${price:.2f}</b>
        </div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    # --- INTELLIGENT ADVICE LOGIC ---
    if distance < 1.5:
        msg = "🚶 **Walkable:** For trips under 1.5 miles, walking/cycling is often faster than NYC traffic."
        icon = "info"
    elif distance > 20:
        msg = "✈️ **Long Haul:** For airports (JFK/EWR), check for flat-rate 'Airport Fares' before accepting the meter."
        icon = "warning"
    elif 16 <= hour <= 19 and not is_weekend:
        msg = "🚦 **Rush Hour:** Heavy congestion (4PM-7PM). Expect the higher end of the typical range."
        icon = "warning"
    elif 0 <= hour <= 4:
        msg = "🌙 **Night Owl:** Low traffic, minimal surcharges. Driver availability may vary."
        icon = "success"
    else:
        msg = "✅ **Standard Rate:** Conditions align with market averages. Proceed with confidence."
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
st.markdown("### 3. Cost Breakdown")

tab1, tab2 = st.tabs(["💵 Cost Structure", "📈 Hourly Trends"])

with tab1:
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
    
    line = alt.Chart(trend_df).mark_area(
        line={'color':'#179758'},
        color=alt.Gradient(
            gradient='linear',
            stops=[alt.GradientStop(color='#179758', offset=0),
                   alt.GradientStop(color='transparent', offset=1)],
            x1=1, x2=1, y1=1, y2=0
        )
    ).encode(
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
