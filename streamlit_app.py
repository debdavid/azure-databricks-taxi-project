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
st.set_page_config(page_title="NYC Pricing Agent", page_icon="🚖", layout="centered")

st.markdown("""
    <style>
    /* Background */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #e4f0e8 100%);
    }
    
    /* Medallion Logo */
    .medallion {
        background-color: #f1c40f; 
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
    
    /* Cards */
    div.css-1r6slb0, div.css-12oz5g7 {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 25px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05);
        border: 1px solid #e1e4e8;
    }
    
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

    /* --- CHAT INTERFACE STYLING --- */
    .chat-header {
        background-color: #1a252f;
        color: white;
        padding: 15px;
        border-top-left-radius: 12px;
        border-top-right-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-top: 30px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .chat-status {
        font-size: 12px;
        color: #2ecc71; /* Green */
        text-transform: uppercase;
        font-weight: bold;
        letter-spacing: 1px;
    }
    .pulsing-dot {
        height: 10px;
        width: 10px;
        background-color: #2ecc71;
        border-radius: 50%;
        display: inline-block;
        margin-right: 5px;
        box-shadow: 0 0 0 rgba(46, 204, 113, 0.4);
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(46, 204, 113, 0.4); }
        70% { box-shadow: 0 0 0 10px rgba(46, 204, 113, 0); }
        100% { box-shadow: 0 0 0 0 rgba(46, 204, 113, 0); }
    }
    </style>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------
# 🚕 HEADER
# ---------------------------------------------------------
h_col1, h_col2 = st.columns([1, 4])
with h_col1:
    st.markdown('<div class="medallion">NYC<br>TAXI</div>', unsafe_allow_html=True)
with h_col2:
    st.title("NYC Price Check")
    st.markdown("**AI-Powered Fair Fare Estimator**")

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
# 🧠 CALCULATION ENGINE
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
# 🏁 REPORT
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
    if distance < 1.5:
        st.info("🚶 **Walkable:** Short trip detected. Walking may be faster.")
    elif 16 <= hour <= 19 and not is_weekend:
        st.warning("🚦 **Rush Hour:** Expect heavy traffic (4-7 PM).")
    else:
        st.success("✅ **Standard Rate:** Conditions are normal.")

# ---------------------------------------------------------
# 💬 AGENT CHAT (The "Wizard of Oz" Logic)
# ---------------------------------------------------------
# Custom Header for Chat
st.markdown("""
<div class="chat-header">
    <div style="font-weight: bold; font-size: 18px;">🤖 Live Agent Consultant</div>
    <div class="chat-status"><span class="pulsing-dot"></span>ONLINE</div>
</div>
""", unsafe_allow_html=True)

# Initialize Chat & Add Welcome Message if empty
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Auto-Greeting (Triggers engagement)
    welcome_msg = "Hello! I am analyzing the market data for your trip. Ask me about **traffic**, **airport rates**, or how to **save money**."
    st.session_state.messages.append({"role": "assistant", "content": welcome_msg})

# Display History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle Input
if prompt := st.chat_input("Ask about your trip (e.g. 'Is this expensive?')..."):
    
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.spinner("Consulting knowledge base..."):
        time.sleep(1.2) # Fake "Thinking" Latency

    # FAKE AI LOGIC ROUTER
    prompt_lower = prompt.lower()
    
    if "save" in prompt_lower or "cheaper" in prompt_lower:
        response = f"To save on this **{distance} mile** trip, consider travelling outside of rush hour (4PM-7PM) or using the subway for part of the journey. The current fair price is around **${price:.2f}**."
    elif "traffic" in prompt_lower or "rush" in prompt_lower:
        if 16 <= hour <= 19:
            response = "⚠️ **Heavy Traffic Alert:** You are selecting a pickup during **Rush Hour (4PM - 7PM)**. My model includes a time-penalty, but real-world delays could increase the meter further."
        else:
            response = "Traffic is currently moderate. You are outside the peak congestion window."
    elif "airport" in prompt_lower or "jfk" in prompt_lower or "lga" in prompt_lower:
        response = "✈️ **Airport Advice:** For JFK trips, NYC taxis often use a **Flat Fare** (approx $70 + tolls). Verify this with the driver before starting the meter!"
    elif "hello" in prompt_lower or "hi" in prompt_lower:
        response = "Hello! I'm here to help you audit your taxi fare. What details can I clarify for you?"
    else:
        response = f"Based on **2.7 million historical records**, a trip of **{distance} miles** at **{time_label}** typically costs between **${low_range:.2f}** and **${high_range:.2f}**. If your quote is higher, check for surge pricing."

    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
