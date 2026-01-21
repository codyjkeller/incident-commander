import streamlit as st
import random
import time

# --- CONFIGURATION ---
st.set_page_config(page_title="CISO Commander", page_icon="🛡️", layout="centered")

# --- CUSTOM CSS (Premium "Holo-Card" Style) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;500;700&display=swap');
    
    .stApp {
        background-color: #050505;
        background-image: radial-gradient(circle at 50% 50%, #1a1a2e 0%, #000000 100%);
        color: #e0e6ed;
        font-family: 'Rajdhani', sans-serif;
    }

    /* THE CARD CONTAINER */
    .game-card {
        position: relative;
        background: linear-gradient(145deg, #1a1a24, #101014);
        border-radius: 18px;
        padding: 6px; /* Creates the border width */
        margin: 20px auto;
        max-width: 500px;
        box-shadow: 0 0 30px rgba(0, 224, 255, 0.1);
        overflow: hidden;
    }
    
    /* The "Holographic" Border Gradient */
    .game-card::before {
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        border-radius: 18px; 
        padding: 2px;
        background: linear-gradient(45deg, #FF0055, #00E0FF, #BD00FF);
        -webkit-mask: 
            linear-gradient(#fff 0 0) content-box, 
            linear-gradient(#fff 0 0);
        -webkit-mask-composite: xor;
        mask-composite: exclude;
        pointer-events: none;
    }

    /* INNER CARD CONTENT */
    .card-inner {
        background: #131318;
        border-radius: 14px;
        overflow: hidden;
        height: 100%;
        position: relative;
    }

    /* HEADER: Type Icon & Title */
    .card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 12px 15px;
        background: rgba(255, 255, 255, 0.03);
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    }
    .card-type-icon {
        font-size: 20px;
        background: #222;
        width: 35px; height: 35px;
        display: flex; align-items: center; justify-content: center;
        border-radius: 50%;
        border: 1px solid #444;
        box-shadow: 0 0 10px rgba(0,0,0,0.5);
    }
    .card-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 18px;
        font-weight: 700;
        color: #fff;
        text-transform: uppercase;
        letter-spacing: 1px;
        text-shadow: 0 0 5px rgba(0, 224, 255, 0.5);
    }

    /* IMAGE WINDOW */
    .card-image-frame {
        margin: 10px;
        border: 2px solid #333;
        border-radius: 8px;
        height: 220px;
        overflow: hidden;
        position: relative;
    }
    .card-img {
        width: 100%; height: 100%; object-fit: cover;
        filter: contrast(1.1) saturate(1.1);
    }

    /* BODY TEXT */
    .card-body {
        padding: 15px 20px;
        text-align: left;
    }
    .card-desc {
        font-size: 18px;
        font-weight: 500;
        line-height: 1.4;
        color: #d1d5db;
        min-height: 80px;
    }
    .flavor-text {
        font-size: 12px;
        font-style: italic;
        color: #666;
        margin-top: 10px;
        border-top: 1px solid #333;
        padding-top: 5px;
        text-align: center;
    }

    /* STATS HUD */
    .hud-container {
        display: flex;
        justify-content: space-around;
        background: rgba(0,0,0,0.4);
        border: 1px solid #333;
        border-radius: 12px;
        padding: 10px;
        margin-bottom: 25px;
        backdrop-filter: blur(5px);
    }
    .hud-box { text-align: center; width: 22%; }
    .hud-label { font-size: 10px; color: #888; letter-spacing: 1px; font-family: 'Orbitron'; }
    .hud-val { font-size: 22px; font-weight: 700; font-family: 'Rajdhani'; }

    .c-green { color: #00FF9D; text-shadow: 0 0 8px rgba(0,255,157,0.3); }
    .c-blue { color: #00E0FF; text-shadow: 0 0 8px rgba(0,224,255,0.3); }
    .c-red { color: #FF0055; text-shadow: 0 0 8px rgba(255,0,85,0.3); }
    .c-purp { color: #BD00FF; text-shadow: 0 0 8px rgba(189,0,255,0.3); }

    /* BUTTONS */
    .stButton > button {
        background: linear-gradient(180deg, #2b2b35 0%, #1a1a20 100%) !important;
        border: 1px solid #444 !important;
        color: #fff !important;
        font-family: 'Orbitron', sans-serif !important;
        letter-spacing: 1px;
        padding: 15px !important;
        transition: all 0.2s ease !important;
    }
    .stButton > button:hover {
        border-color: #00E0FF !important;
        box-shadow: 0 0 15px rgba(0, 224, 255, 0.2) !important;
        transform: translateY(-2px);
    }
</style>
""", unsafe_allow_html=True)

# --- ADVANCED GAME DATA ---
# Added "Boss" Logic and "Flavor Text"
EVENTS = [
    {
        "id": 1,
        "type": "INCIDENT",
        "icon": "💀",
        "image": "https://img.freepik.com/free-vector/hacker-operating-laptop-cartoon-icon-illustration-technology-icon-concept-isolated-flat-cartoon-style_138676-2387.jpg", 
        "title": "RANSOMWARE",
        "text": "Your SOC dashboard lights up red. A variant of LockBit has encrypted the Finance drive.",
        "flavor": "\"We accept Bitcoin or Monero. You have 24 hours.\"",
        "choice_a": "Pay $50k Ransom",
        "choice_b": "Rebuild (3 Days)",
        "impact_a": {"budget": -25, "risk": -10, "rep": -5, "bandwidth": 0},
        "impact_b": {"budget": 0, "risk": +5, "rep": +5, "bandwidth": -25}
    },
    {
        "id": 2,
        "type": "VENDOR",
        "icon": "🤝",
        "image": "https://img.freepik.com/free-vector/business-deal-cartoon-concept_1284-11440.jpg", 
        "title": "SALES OVERRIDE",
        "text": "The CRO demands we whitelist a sketchy AI tool to close a $1M deal before quarter-end.",
        "flavor": "\"Just enable it for this one demo, please!\"",
        "choice_a": "Block (Policy)",
        "choice_b": "Allow (Revenue)",
        "impact_a": {"budget": 0, "risk": -5, "rep": -15, "bandwidth": 0},
        "impact_b": {"budget": +5, "risk": +20, "rep": +10, "bandwidth": 0}
    },
    {
        "id": 3,
        "type": "AUDIT",
        "icon": "📋",
        "image": "https://img.freepik.com/free-vector/checklist-concept-illustration_114360-479.jpg", 
        "title": "SURPRISE AUDIT",
        "text": "The regulator walked in 2 months early. Your evidence repository is... incomplete.",
        "flavor": "\"I'd like to see your Access Control Logs for last year.\"",
        "choice_a": "Stall / Delay",
        "choice_b": "Full Transparency",
        "impact_a": {"budget": 0, "risk": +5, "rep": -10, "bandwidth": -10},
        "impact_b": {"budget": 0, "risk": +15, "rep": +5, "bandwidth": 0}
    },
    # ... Add more events here ...
]

# --- STATE & FUNCTIONS (Simplified for brevity) ---
if 'stats' not in st.session_state:
    st.session_state.stats = {'budget': 60, 'rep': 50, 'risk': 20, 'bandwidth': 50}
if 'deck' not in st.session_state:
    st.session_state.deck = list(range(len(EVENTS)))
    random.shuffle(st.session_state.deck)
if 'current_card' not in st.session_state:
    st.session_state.current_card = EVENTS[st.session_state.deck.pop()]

def apply_effect(impact):
    for k, v in impact.items():
        st.session_state.stats[k] = max(0, min(100, st.session_state.stats[k] + v))
    
    if not st.session_state.deck:
        st.session_state.deck = list(range(len(EVENTS)))
        random.shuffle(st.session_state.deck)
    
    st.session_state.current_card = EVENTS[st.session_state.deck.pop()]
    st.rerun()

# --- MAIN RENDER ---
s = st.session_state.stats
card = st.session_state.current_card

# 1. HEADER HUD
st.markdown(f"""
<div class="hud-container">
    <div class="hud-box"><div class="hud-label">BUDGET</div><div class="hud-val c-green">${s['budget']}k</div></div>
    <div class="hud-box"><div class="hud-label">TRUST</div><div class="hud-val c-blue">{s['rep']}</div></div>
    <div class="hud-box"><div class="hud-label">RISK</div><div class="hud-val c-red">{s['risk']}%</div></div>
    <div class="hud-box"><div class="hud-label">TEAM</div><div class="hud-val c-purp">{s['bandwidth']}</div></div>
</div>
""", unsafe_allow_html=True)

# 2. THE CARD
st.markdown(f"""
<div class="game-card">
    <div class="card-inner">
        <div class="card-header">
            <div class="card-title">{card['title']}</div>
            <div class="card-type-icon">{card['icon']}</div>
        </div>
        <div class="card-image-frame">
            <img src="{card['image']}" class="card-img">
        </div>
        <div class="card-body">
            <div class="card-desc">{card['text']}</div>
            <div class="flavor-text">{card['flavor']}</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# 3. ACTIONS
c1, c2 = st.columns(2)
with c1:
    if st.button(f"⬅ {card['choice_a']}"):
        apply_effect(card['impact_a'])
with c2:
    if st.button(f"➡ {card['choice_b']}"):
        apply_effect(card['impact_b'])
