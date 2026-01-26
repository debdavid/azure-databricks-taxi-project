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
# 🎨 UI & THEME CONFIGURATION (Dark Mode + BCG Green)
# ---------------------------------------------------------
st.set_page_config(page_title="NYC Pricing Agent", page_icon="🟢", layout="centered")

# Force Dark Theme via CSS Injection
st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background-color: #0E1117;
        color: #FAFAFA;
    }
    /* Card/Container Backgrounds */
    .css-1r6slb0, .css-12oz5g7 {
        background-color: #262730;
        border-radius: 10px;
        padding: 20px;
    }
    /* The "Price Tag" Style */
    .price-tag { 
        font-size: 48px !important; 
        font-family: 'Helvetica Neue', sans-serif;
        color: #179758; /* BCG Green */
        font-weight: 800; 
        margin-bottom: 0px;
    }
    .sub-label {
        color: #B0B0B0;
        font-size: 14px;
        margin-top: -10px;
    }
    /* Agent Alert Box */
    .agent-box {
        background-color: #1E3A2F; 
        border: 1px solid #179758;
        padding: 15px;
        border-radius: 8px;
        color: #E6FFFA;
    }
    </style>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------
# 🚀 HEADER
# ---------------------------------------------------------
st.title("🟢 NYC Pricing Agent")
st.markdown("**Autonomous Fare Optimization Engine**")
st.markdown("This agent automates the workflow of finding the optimal departure time, simulating market conditions to minimize your spend.")
st.divider()

# ---------------------------------------------------------
# 🎛️ WORKFLOW INPUTS
# ---------------------------------------------------------
st.subheader("1. Define Mission")
col1, col2 = st.columns(2)

with col1:
    distance = st.slider("Target Distance (Miles)", 0.5, 50.0, 5.0, step=0.5)
    passengers = st.number_input("Passenger Count", 1, 6, 1)

with col2:
    time_options = ["12 AM", "1 AM", "2 AM", "3 AM", "4 AM", "5 AM", "6 AM", "7 AM", 
                    "8 AM", "9 AM", "10 AM", "11 AM", "12 PM", "1 PM", "2 PM", "3 PM", 
                    "4 PM", "5 PM", "6 PM", "7 PM", "8 PM", "9 PM", "10 PM", "11 PM"]
    time_label = st.select_slider("Target Time", options=time_options, value="2 PM")
    hour = time_options.index(time_label)
    
    day_type = st.radio("Context", ["Weekday", "Weekend"], horizontal=True)
    is_weekend = 1 if day_type == "Weekend" else 0

# ---------------------------------------------------------
# 🧠 AGENT EXECUTION LOOP
# ---------------------------------------------------------
def calculate_fare(dist, hr, weekend, pax):
    day_val = 7 if weekend else 2
    # Components
    c_base = INTERCEPT
    c_dist = dist * COEF_DISTANCE
    c_time = hr * COEF_HOUR
    c_extra = (day_val * COEF_WEEKEND) + (pax * COEF_PASSENGER)
    total = c_base + c_dist + c_time + c_extra
    return max(5.0, total), c_base, c_dist, c_time, c_extra

# 1. Run User Scenario
current_price, c_base, c_dist, c_time, c_extra = calculate_fare(distance, hour, is_weekend, passengers)

# 2. Agent "Thought Process" (Simulate +/- 3 hours)
best_price = current_price
best_hour = hour
savings = 0.0

for h in range(max(0, hour-3), min(23, hour+4)):
    sim_price, _, _, _, _ = calculate_fare(distance, h, is_weekend, passengers)
    if sim_price < best_price:
        best_price = sim_price
        best_hour = h
        savings = current_price - best_price

# ---------------------------------------------------------
# 🏁 AGENT REPORT
# ---------------------------------------------------------
st.divider()
st.subheader("2. Strategic Assessment")

# Layout: Price on Left, Recommendation on Right
c1, c2 = st.columns([1, 1.5])

with c1:
    st.markdown('<p class="sub-label">PREDICTED FARE</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="price-tag">${current_price:.2f}</p>', unsafe_allow_html=True)

with c2:
    if savings > 0.15: # Threshold for recommendation
        better_time = time_options[best_hour]
        st.markdown(f"""
        <div class="agent-box">
            <b>🚀 OPTIMIZATION FOUND</b><br>
            If you shift departure to <b>{better_time}</b>, you save <b>${savings:.2f}</b>.<br>
            <i>The agent recommends rescheduling.</i>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.success("✅ Current selection is optimal. No significant savings found nearby.")

# ---------------------------------------------------------
# 📊 VISUALIsATION (Dark Mode Friendly)
# ---------------------------------------------------------
st.divider()
with st.expander("🔎 View Logic (Cost Drivers & Market Trends)"):
    
    tab1, tab2 = st.tabs(["Cost Structure", "Market Trends"])
    
    with tab1:
        # Renamed Component to "Time of Day Adj."
        breakdown_data = pd.DataFrame({
            "Driver": ["Distance Cost", "Base Rate", "Time of Day Adj.", "Surcharges"],
            "Cost ($)": [c_dist, c_base, c_time, c_extra]
        })
        
        c = alt.Chart(breakdown_data).mark_bar().encode(
            x=alt.X('Driver', sort="-y", axis=alt.Axis(labelColor='white', titleColor='white')),
            y=alt.Y('Cost ($)', axis=alt.Axis(labelColor='white', titleColor='white')),
            color=alt.value("#179758") # BCG Green
        ).properties(background='transparent')
        
        st.altair_chart(c, use_container_width=True)
        
    with tab2:
        trend_data = pd.DataFrame({"Hour": range(24), "Avg Fare": HOURLY_PRICES})
        
        # Line Chart with Gradient
        line = alt.Chart(trend_data).mark_area(
            line={'color':'#179758'},
            color=alt.Gradient(
                gradient='linear',
                stops=[alt.GradientStop(color='#179758', offset=0),
                       alt.GradientStop(color='transparent', offset=1)],
                x1=1, x2=1, y1=1, y2=0
            )
        ).encode(
            x=alt.X('Hour', axis=alt.Axis(labelColor='white')),
            y=alt.Y('Avg Fare', axis=alt.Axis(labelColor='white'))
        ).properties(background='transparent')
        
        # Current selection dot
        point = alt.Chart(pd.DataFrame({'Hour': [hour], 'Avg Fare': [HOURLY_PRICES[hour]]}))\
            .mark_point(color='white', size=100, filled=True)\
            .encode(x='Hour', y='Avg Fare')

        st.altair_chart(line + point, use_container_width=True)
