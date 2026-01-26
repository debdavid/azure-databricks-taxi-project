import streamlit as st
import pandas as pd
import altair as alt
import time 

# ---------------------------------------------------------
# 🧠 AGENT BRAIN
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
# 🎨 UI CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(page_title="NYC Pricing Agent", page_icon="🚖", layout="wide")

st.markdown("""
    <style>
    /* 1. BACKGROUND */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #e4f0e8 100%);
    }
    
    /* 2. LOGO */
    .medallion {
        background-color: #f1c40f; 
        color: #000000;
        width: 70px;
        height: 70px;
        border-radius: 14px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 800;
        font-size: 20px;
        line-height: 1.1;
        text-align: center;
        box-shadow: 0 4px 0px #c29d0b;
        border: 2px solid #000000;
        margin-right: 15px;
    }
    
    /* 3. MAIN CARDS */
    div.css-1r6slb0, div.css-12oz5g7 {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 25px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        border: 1px solid #e1e4e8;
    }
    
    /* 4. PRICE CARD (Full Width Banner Style) */
    .price-card {
        background: white;
        border-left: 8px solid #179758;
        padding: 25px;
        border-radius: 8px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        margin-bottom: 15px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .price-main {
        font-size: 48px;
        font-weight: 800;
        color: #179758;
        margin: 0;
        line-height: 1;
    }
    .price-sub {
        font-size: 14px;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        color: #555;
        font-weight: 700;
    }
    .price-small {
        font-size: 16px;
        color: #888;
        font-weight: 500;
        text-align: right;
    }

    /* 5. RIGHT PANEL (Chat Box) */
    .chat-container {
        background-color: white;
        border-radius: 12px;
        border: 1px solid #e1e4e8;
        padding: 10px;
        height: 100%;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }
    .chat-header {
        background-color: #1a252f;
        color: white;
        padding: 12px;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 15px;
    }
    .pulsing-dot {
        height: 8px;
        width: 8px;
        background-color: #2ecc71;
        border-radius: 50%;
        display: inline-block;
        margin-right: 6px;
        box-shadow: 0 0 0 rgba(46, 204, 113, 0.4);
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(46, 204, 113, 0.4); }
        70% { box-shadow: 0 0 0 6px rgba(46, 204, 113, 0); }
        100% { box-shadow: 0 0 0 0 rgba(46, 204, 113, 0); }
    }
    
    /* Disclaimer */
    .disclaimer {
        font-size: 11px;
        color: #95a5a6;
        margin-top: 40px;
        border-top: 1px solid #eee;
        padding-top: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------
# 🏗️ LAYOUT STRUCTURE
# ---------------------------------------------------------
# [2.5, 1] Ratio -> Gives the main app much more breathing room
left_col, right_col = st.columns([2.5, 1], gap="large")

# =========================================================
# 👈 LEFT COLUMN: THE WORKBENCH
# =========================================================
with left_col:
    
    # Header
    h_c1, h_c2 = st.columns([0.8, 5])
    with h_c1:
        st.markdown('<div class="medallion">NYC<br>TAXI</div>', unsafe_allow_html=True)
    with h_c2:
        st.title("NYC Price Check")
        st.markdown("**AI-Powered Fair Fare Estimator**")
    
    st.divider()

    # 1. Inputs
    st.markdown("### 1. Journey Context")
    
    i_c1, i_c2 = st.columns(2)
    with i_c1:
        distance = st.slider("📏 Distance (Miles)", 0.5, 50.0, 5.0, step=0.5)
        passengers = st.number_input("👥 Passengers", 1, 6, 1)
    with i_c2:
        time_options = ["12 AM", "1 AM", "2 AM", "3 AM", "4 AM", "5 AM", "6 AM", "7 AM", 
                        "8 AM", "9 AM", "10 AM", "11 AM", "12 PM", "1 PM", "2 PM", "3 PM", 
                        "4 PM", "5 PM", "6 PM", "7 PM", "8 PM", "9 PM", "10 PM", "11 PM"]
        time_label = st.select_slider("⏰ Time of Day", options=time_options, value="2 PM")
        hour = time_options.index(time_label)
        day_type = st.radio("📅 Day Type", ["Weekday", "Weekend"], horizontal=True)
        is_weekend = 1 if day_type == "Weekend" else 0

    # Logic
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

    # 2. Results (Stacked for better alignment)
    st.divider()
    st.markdown("### 2. Price Check Result")
    
    # Custom HTML Card
    st.markdown(f"""
    <div class="price-card">
        <div>
            <div class="price-sub">Typical Market Range</div>
            <div class="price-main">${low_range:.2f} - ${high_range:.2f}</div>
        </div>
        <div class="price-small">
            Target Estimate<br>
            <span style="font-size: 24px; color: #333; font-weight: bold;">${price:.2f}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Advice Banner (Full Width)
    if distance < 1.5:
        st.info("🚶 **Walkable:** Short trip detected. Walking or cycling may be faster than sitting in NYC traffic.")
    elif 16 <= hour <= 19 and not is_weekend:
        st.warning("🚦 **Rush Hour:** Expect heavy traffic (4-7 PM). Prices reflect the higher end of the range.")
    else:
        st.success("✅ **Standard Rate:** Conditions align with market averages. Proceed with confidence.")

    # 3. Visualisation
    st.markdown("### 3. Cost Visualisation")
    
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
        ).properties(height=250)
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
            y=alt.Y('Avg Fare', title="Avg Market Rate ($)")
        ).properties(height=250)
        
        point_df = pd.DataFrame({'Hour': [hour], 'Avg Fare': [HOURLY_PRICES[hour]]})
        point = alt.Chart(point_df).mark_point(fill='red', color='red', size=80).encode(x='Hour', y='Avg Fare')
        st.altair_chart(line + point, use_container_width=True)

    # Disclaimer
    st.markdown("""
    <div class="disclaimer">
        <b>Data Transparency:</b> Model trained on NYC TLC trip records (Jan 2024). 
        Estimates based on historical patterns. Actual fares vary by live traffic/weather.
    </div>
    """, unsafe_allow_html=True)


# =========================================================
# 👉 RIGHT COLUMN: THE AI AGENT (Sidebar Style)
# =========================================================
with right_col:
    # Use a container to create the "White Panel" look
    with st.container():
        st.markdown('<div class="chat-header"><div style="font-weight: bold; font-size: 14px;">🤖 Live Consultant</div><div style="font-size: 10px; color: #2ecc71; font-weight: bold;"><span class="pulsing-dot"></span>ONLINE</div></div>', unsafe_allow_html=True)
        
        # Initialize Chat
        if "messages" not in st.session_state:
            st.session_state.messages = []
            welcome_msg = "Hello! I am analysing the market data. Ask me about **traffic**, **airport rates**, or how to **save money**."
            st.session_state.messages.append({"role": "assistant", "content": welcome_msg})

        # History
        # Fixed height to ensure it doesn't stretch the page too much
        with st.container(height=550):
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

            # Input
            if prompt := st.chat_input("Ask about your fare..."):
                st.chat_message("user").markdown(prompt)
                st.session_state.messages.append({"role": "user", "content": prompt})

                with st.spinner("Processing..."):
                    time.sleep(1.0) 

                # LOGIC
                prompt_lower = prompt.lower()
                if "save" in prompt_lower or "cheaper" in prompt_lower:
                    response = f"To save on this **{distance} mile** trip, consider travelling outside of rush hour (4PM-7PM). The current fair price is **${price:.2f}**."
                elif "traffic" in prompt_lower or "rush" in prompt_lower:
                    if 16 <= hour <= 19:
                        response = "⚠️ **Heavy Traffic Alert:** You are selecting a pickup during **Rush Hour (4PM - 7PM)**. My model includes a time-penalty."
                    else:
                        response = "Traffic is currently moderate. You are outside the peak congestion window."
                elif "airport" in prompt_lower or "jfk" in prompt_lower:
                    response = "✈️ **Airport Advice:** For JFK trips, NYC taxis often use a **Flat Fare** (approx $70 + tolls). Verify this with the driver!"
                else:
                    response = f"Based on **2.7 million historical records**, a trip of **{distance} miles** at **{time_label}** typically costs between **${low_range:.2f}** and **${high_range:.2f}**. Always verify the metre starts correctly."

                with st.chat_message("assistant"):
                    st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
