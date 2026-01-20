import streamlit as st
import random
import json
import pandas as pd
import os

# --- CONFIG & CSS ---
st.set_page_config(page_title="Incident Commander: Reigns", page_icon="👑", layout="centered")

st.markdown("""
<style>
    .stApp { background-color: #1a1a2e; color: #e94560; }
    .card-container {
        background-color: #16213e; border: 2px solid #0f3460;
        border-radius: 15px; padding: 40px; text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.5); margin-bottom: 20px;
    }
    .emoji-icon { font-size: 80px; margin-bottom: 20px; }
    .scenario-title { color: #fff; font-size: 28px; font-weight: bold; }
    .scenario-desc { color: #a2a8d3; font-size: 18px; margin-top: 10px; }
    
    /* Metrics Styling */
    div[data-testid="stMetric"] {
        background-color: #0f3460; border-radius: 8px; padding: 10px;
        border: 1px solid #533483;
    }
    div[data-testid="stMetricLabel"] { color: #a2a8d3; }
    div[data-testid="stMetricValue"] { color: #fff; }
</style>
""", unsafe_allow_html=True)

# --- LOAD DATA ---
@st.cache_data
def load_scenarios():
    if not os.path.exists("scenarios.json"):
        return []
    with open("scenarios.json", "r") as f:
        return json.load(f)

# --- INITIALIZE STATE ---
if "state" not in st.session_state:
    st.session_state.state = {
        # METRICS (0-100 Scale)
        "budget": 50,      # 💵 Money
        "rep": 50,         # 🗣️ Reputation
        "risk": 20,        # 🔥 Risk (Keep Low!)
        "time": 50,        # ⏳ Bandwidth
        
        "week": 1,
        "history": [],
        "game_over": False,
        "outcome": "",
        "scenario": None
    }

# Load scenarios if needed
if st.session_state.state["scenario"] is None:
    scenarios = load_scenarios()
    if scenarios:
        st.session_state.state["scenario"] = random.choice(scenarios)

s = st.session_state.state

# --- GAME OVER SCREEN ---
if s["game_over"]:
    st.title("💀 GAME OVER")
    st.markdown(f"### {s['outcome']}")
    st.markdown("---")
    
    # Analytics
    st.write("#### Final Metrics")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("💵 Budget", f"{s['budget']}%")
    col2.metric("🗣️ Reputation", f"{s['rep']}%")
    col3.metric("🔥 Risk", f"{s['risk']}%")
    col4.metric("⏳ Bandwidth", f"{s['time']}%")
    
    st.write("#### Decision History")
    for log in s["history"]:
        st.caption(log)
        
    if st.button("Try Again"):
        del st.session_state.state
        st.rerun()
    st.stop()

# --- MAIN HUD (METRICS) ---
st.title(f"👑 Week {s['week']}")

# Metrics Row
m1, m2, m3, m4 = st.columns(4)
m1.metric("Budget", f"{s['budget']}", delta_color="normal")
m2.metric("Reputation", f"{s['rep']}", delta_color="normal")
m3.metric("Risk", f"{s['risk']}", delta_color="inverse") # Inverse because Red (High) is bad
m4.metric("Bandwidth", f"{s['time']}", delta_color="normal")

# Progress Bars for visual flair
st.caption("🔥 Risk Meter (Don't hit 100!)")
st.progress(min(s['risk'], 100) / 100)

# --- CARD UI ---
scen = s["scenario"]
if scen:
    st.markdown(f"""
    <div class="card-container">
        <div class="emoji-icon">{scen['image']}</div>
        <div class="scenario-title">{scen['title']}</div>
        <div class="scenario-desc">{scen['desc']}</div>
    </div>
    """, unsafe_allow_html=True)

    # --- CONTROLS (Swipe Left / Swipe Right) ---
    c_left, c_right = st.columns(2)
    
    choice = None
    
    # Left Button
    if c_left.button(f"⬅️ {scen['left']['text']}", use_container_width=True):
        choice = scen['left']
        
    # Right Button
    if c_right.button(f"{scen['right']['text']} ➡️", use_container_width=True):
        choice = scen['right']

    # --- PROCESS TURN ---
    if choice:
        # Apply Impacts
        s['budget'] = max(0, min(100, s['budget'] + choice['impact']['budget']))
        s['rep']    = max(0, min(100, s['rep']    + choice['impact']['rep']))
        s['risk']   = max(0, min(100, s['risk']   + choice['impact']['risk']))
        s['time']   = max(0, min(100, s['time']   + choice['impact']['time']))
        
        # Log History
        s['history'].insert(0, f"Wk {s['week']}: {scen['title']} -> {choice['text']}")
        
        # Check Win/Loss
        if s['budget'] <= 0:
            s['game_over'] = True
            s['outcome'] = "Bankrupt! The board dissolved your department."
        elif s['rep'] <= 0:
            s['game_over'] = True
            s['outcome'] = "Fired! You lost the trust of the executives."
        elif s['risk'] >= 100:
            s['game_over'] = True
            s['outcome'] = "Breach! The company suffered a catastrophic data loss."
        elif s['time'] <= 0:
            s['game_over'] = True
            s['outcome'] = "Burnout! Your team quit en masse."
        elif s['week'] >= 52:
            s['game_over'] = True
            s['outcome'] = "Victory! You survived the fiscal year."

        # Next Turn
        s['week'] += 1
        scenarios = load_scenarios()
        s['scenario'] = random.choice(scenarios)
        st.rerun()
