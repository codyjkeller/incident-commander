import streamlit as st
import random
import json
import pandas as pd
import os

# --- CONFIG ---
st.set_page_config(
    page_title="Incident Commander",
    page_icon="🚨",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- CSS FOR "CYBER" FEEL ---
st.markdown("""
<style>
    .stApp { background-color: #0E1117; color: #FFFFFF; }
    div[data-testid="stMetric"] {
        background-color: #1F2937; border: 1px solid #374151;
        border-radius: 8px; padding: 10px; text-align: center;
    }
    .event-card {
        background-color: #111827; border: 1px solid #3B82F6;
        border-radius: 12px; padding: 25px; text-align: center;
        margin-bottom: 20px;
    }
    .event-title { color: #60A5FA; font-size: 24px; font-weight: bold; margin-bottom: 10px;}
    .event-desc { color: #E5E7EB; font-size: 16px; }
    div.stButton > button {
        width: 100%; height: 3.5rem; font-weight: bold;
        background-color: #1F2937; color: white; border: 1px solid #4B5563;
    }
    div.stButton > button:hover { background-color: #2563EB; border-color: #2563EB; }
</style>
""", unsafe_allow_html=True)

# --- HELPER: LOAD DATA ---
@st.cache_data
def load_scenarios():
    """Loads threat scenarios from the JSON database."""
    file_path = "scenarios.json"
    if not os.path.exists(file_path):
        st.error("🚨 Critical Error: 'scenarios.json' not found in root directory.")
        st.stop()
    with open(file_path, "r") as f:
        return json.load(f)

# --- GAME LOGIC ---
if "state" not in st.session_state:
    # Initialize Game State
    scenarios = load_scenarios()
    st.session_state.state = {
        "budget": 50000, 
        "security": 60, 
        "week": 1,
        "history": [], 
        "score_history": [60],  # For Analytics Chart
        "game_over": False, 
        "outcome": "",
        "scenario": random.choice(scenarios)
    }

st.title("🚨 Incident Commander")
state = st.session_state.state

# HEADER METRICS
c1, c2, c3 = st.columns(3)
c1.metric("Week", f"{state['week']}/52")
c2.metric("Budget", f"${state['budget']:,}")
c3.metric("Security Posture", f"{state['security']}%")
st.progress(state["security"]/100)

# GAME OVER HANDLER
if state["game_over"]:
    st.markdown("---")
    if "Winner" in state["outcome"]:
        st.success(f"🎉 {state['outcome']}")
    else:
        st.error(f"💀 {state['outcome']}")
    
    # NEW: Post-Mortem Analytics
    st.subheader("🛡️ Security Posture Trend")
    chart_data = pd.DataFrame(state["score_history"], columns=["Security Score"])
    st.line_chart(chart_data)

    st.write("### Incident Log")
    for log in state["history"]: st.text(log)
    
    if st.button("New Operation"):
        del st.session_state.state
        st.rerun()
    st.stop()

# SCENARIO DISPLAY
scen = state["scenario"]
st.markdown(f"""
<div class="event-card">
    <div style="font-size: 60px;">{scen['icon']}</div>
    <div class="event-title">{scen['title']}</div>
    <div class="event-desc">{scen['desc']}</div>
</div>
""", unsafe_allow_html=True)

# DECISION BUTTONS
for choice in scen["choices"]:
    cost_str = f"-${choice['cost']:,}" if choice['cost'] > 0 else "Free"
    if st.button(f"{choice['text']} ({cost_str})", use_container_width=True):
        # Update State
        state["budget"] -= choice["cost"]
        new_security = max(0, min(100, state["security"] + choice["sec"]))
        state["security"] = new_security
        state["score_history"].append(new_security) # Track for chart
        
        state["history"].insert(0, f"Wk {state['week']}: {scen['title']} - {choice['msg']}")
        
        # Win/Loss Conditions
        if state["budget"] < 0:
            state["game_over"] = True
            state["outcome"] = "Operations Halted: Budget Depleted."
        elif state["security"] <= 0:
            state["game_over"] = True
            state["outcome"] = "Critical Breach: Data Exfiltrated."
        elif state["week"] >= 52:
            state["game_over"] = True
            state["outcome"] = "Winner: Network Secure for Fiscal Year."
        
        # Next Turn
        state["week"] += 1
        scenarios = load_scenarios() # Reload to ensure freshness
        state["scenario"] = random.choice(scenarios)
        st.rerun()

with st.expander("Mission Log"):
    for log in state["history"]: st.caption(log)
