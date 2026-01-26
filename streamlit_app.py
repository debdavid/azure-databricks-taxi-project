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
# 🎨 UI CONFIGURATION (Accenture Style)
# ---------------------------------------------------------
st.set_page_config(page_title="NYC Pricing Agent", page_icon="🟣", layout="wide")

st.markdown("""
    <style>
    /* 1. TYPOGRAPHY (The "Accenture" Graphik Look) */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', 'Graphik', sans-serif;
    }
    
    /* 2. BACKGROUND (Clean High-Tech White/Grey) */
    .stApp {
        background-color: #ffffff;
        background-image: linear-gradient(180deg, #ffffff 0%, #f4f4f4 100%);
    }
    
    /* 3. THE BRAND MARK (The Purple "Greater Than" Symbol) */
    .brand-mark {
        background-color: #A100FF; /* Accenture Purple */
        color: #ffffff;
        width: 60px;
        height: 60px;
        border-radius: 4px; /* Sharp, tech corners */
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 900;
        font-size: 30px;
        box-shadow: 0 4px 10px rgba(161, 0, 255, 0.3);
        margin-right: 15px;
    }
    
    /* 4. CARDS (Sharp & Minimalist) */
    div.css-1r6slb0, div.css-12oz5g7 {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        border-radius: 0px; /* Accenture uses sharp corners */
        padding: 25px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.05);
    }
    
    /* 5. PRICE CARD (Purple Accent) */
    .price-card {
        background: #fafafa;
        border-left: 6px solid #A100FF; /* Purple Strip */
        padding: 25px;
        margin-bottom: 15px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-shadow: 0 2px 10px rgba(0,0,0,0.03);
    }
    .price-main {
        font-size: 48px;
        font-weight: 900; /* Extra Bold */
        color: #000000; /* Stark Black */
        margin: 0;
        line-height: 1;
    }
    .price-sub {
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 2px;
        color: #A100FF;
        font-weight: 700;
        margin-bottom: 5px;
    }
    .price-small {
        font-size: 16px;
        color: #666;
        font-weight: 500;
        text-align: right;
    }
    
    /* 6. HEADERS (Bold Black) */
    h1 {
        color: #000000;
        font-weight: 900;
        letter-spacing: -1px;
    }
    h3 {
        font-weight: 700;
        color: #333;
    }

    /* 7. CHAT PANEL (Clean Sidebar) */
    .chat-header {
        background-color: #000000; /* Black Header */
        color: white;
        padding: 15px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 15px;
    }
    .pulsing-dot {
        height: 8px;
        width: 8px;
        background-color: #A100FF; /* Purple Dot */
        border-radius: 50%;
        display: inline-block;
        margin-right: 6px;
        box-shadow: 0 0 0 rgba(161, 0, 255, 0.4);
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(161, 0, 255, 0.4); }
        70% { box-shadow: 0 0 0 6px rgba(161, 0, 255, 0); }
        100% { box-shadow: 0 0 0 0 rgba(161, 0, 255, 0); }
    }
    
    /* Disclaimer */
    .disclaimer {
        font-size: 11px;
        color: #999;
        margin-top: 40px;
        border-top: 1px solid #eee;
        padding-top: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------
# 🏗️ LAYOUT STRUCTURE
# ---------------------------------------------------------
left_col, right_col = st.columns([2.5, 1], gap="large")

# =========================================================
# 👈 LEFT COLUMN: THE WORKBENCH
# =========================================================
with left_col:
    
    # Header
    h_c1, h_c2 = st.columns([0.6, 5])
    with h_c1:
        # The Accenture-style ">" Symbol
        st.markdown('<div class="brand-mark">&gt;</div>', unsafe_allow_html=True)
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

    # 2. Results
    st.divider()
    st.markdown("### 2. Price Check Result")
    
    # Price Card
    st.markdown(f"""
    <div class="price-card">
        <div>
            <div class="price-sub">Typical Market Range</div>
            <div class="price-main">${low_range:.2f} - ${high_range:.2f}</div>
        </div>
        <div class="price-small">
            Target Estimate<br>
            <span style="font-size: 24px; color: #000; font-weight: 800;">${price:.2f}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Advice Banner
    if distance < 1.5:
        st
