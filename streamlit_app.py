import streamlit as st

# 🧠 THE MODEL BRAIN
INTERCEPT = 10.3838
COEF_DISTANCE = 4.6309
COEF_HOUR = 0.0935
COEF_WEEKEND = 0.0693
COEF_PASSENGER = 0.1288

# 🎨 THE APP
st.set_page_config(page_title="NYC Taxi AI Agent", page_icon="🚖", layout="centered")
st.title("🚖 NYC Taxi Fare Predictor")
st.markdown("""**"How much will my ride cost?"** This AI Agent uses a Linear Regression model trained on **2.7 million taxi trips**.""")

col1, col2 = st.columns(2)
with col1:
    distance = st.slider("Trip Distance (miles)", 0.5, 50.0, 5.0, step=0.5)
    hour = st.slider("Pickup Hour (24h format)", 0, 23, 14)
with col2:
    is_weekend = st.checkbox("Is it a Weekend?", value=False)
    passengers = st.number_input("Passengers", 1, 6, 1)

def predict_fare(dist, hr, weekend, pax):
    day_val = 7 if weekend else 2
    price = (INTERCEPT + (dist * COEF_DISTANCE) + (hr * COEF_HOUR) + (day_val * COEF_WEEKEND) + (pax * COEF_PASSENGER))
    return max(5.0, price)

estimated_price = predict_fare(distance, hour, is_weekend, passengers)
st.divider()
st.subheader(f"🤖 Agent Estimate: ${estimated_price:.2f}")
