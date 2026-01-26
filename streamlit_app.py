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
# 🎨 UI CONFIGURATION (Purple "Tech" Theme)
# ---------------------------------------------------------
st.set_page_config(page_title="NYC Pricing Agent", page_icon="🟣", layout="wide")

st.markdown("""
    <style>
    /* 1. TYPOGRAPHY (Clean, Professional) */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* 2. BACKGROUND (Clean White/Grey) */
    .stApp {
        background-color: #ffffff;
        background-image: linear-gradient(180deg, #ffffff 0%, #f4f4f4 100%);
    }
    
    /* 3. THE LOGO (Restored "NYC TAXI" but in Premium Purple) */
    .medallion {
        background-color: #A100FF; /* High-Tech Purple */
        color: #ffffff;
        width: 80px;
        height: 80px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-family: 'Inter', sans-serif;
        font-weight: 800;
        font-size: 22px;
        line-height: 1.1;
        text-align: center;
        box-shadow: 0 4px 10px rgba(161, 0, 255, 0.3);
        border: 2px solid #000000; /* Black Border for contrast */
        margin-right: 15px;
    }
    
    /* 4. CARDS (Sharp & Minimalist) */
    div.css-1r6slb0, div.css-12oz5g7 {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        border-radius: 8px; 
        padding: 25px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.05);
    }
    
    /* 5. PRICE CARD (Purple Accent) */
    .price-card {
        background: #fafafa;
        border-left: 8px solid #A100FF; /* Purple Strip */
        padding: 25px;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-shadow: 0 2px 10px rgba(0,0,0,0.03);
    }
    .price-main {
        font-size: 48px;
        font-weight: 900; 
        color: #000000; 
        margin: 0;
        line-height: 1;
    }
    .price-sub {
        font
