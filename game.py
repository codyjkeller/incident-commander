import streamlit as st
import random
import time
import json

# --- CONFIGURATION ---
st.set_page_config(page_title="CISO Commander", page_icon="🛡️", layout="centered")

# --- CUSTOM CSS (Cyber-Holographic) ---
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
        padding: 4px; 
        margin: 20px auto;
        max-width: 550px;
        box-shadow: 0 0 40px rgba(0, 0, 0, 0.8);
        overflow: hidden;
        transition: transform 0.2s;
    }
    
    /* Holographic Border */
    .game-card::before {
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        border-radius: 18px; 
        padding: 2px;
        background: linear-gradient(45deg, #FF0055, #00E0FF, #BD00FF);
        -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
        -webkit-mask-composite: xor;
        mask-composite: exclude;
        pointer-events: none;
    }

    /* INNER CONTENT */
    .card-inner {
        background: #131318;
        border-radius: 16px;
        overflow: hidden;
        height: 100%;
    }

    /* HEADER */
    .card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 15px 20px;
        background: rgba(255, 255, 255, 0.03);
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    }
    .card-type-badge {
        font-family: 'Orbitron', sans-serif;
        font-size: 10px;
        background: #333;
        color: #fff;
        padding: 4px 10px;
        border-radius: 4px;
        letter-spacing: 1px;
        text-transform: uppercase;
    }
    .card-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 20px;
        font-weight: 700;
        color: #fff;
        text-transform: uppercase;
        letter-spacing: 1px;
        text-shadow: 0 0 10px rgba(0, 224, 255, 0.4);
    }

    /* IMAGE */
    .card-image-frame {
        height: 240px;
        overflow: hidden;
        position: relative;
        border-bottom: 1px solid rgba(255,255,255,0.05);
    }
    .card-img {
        width: 100%; height: 100%; object-fit: cover;
        opacity: 0.9;
        transition: transform 0.5s;
    }
    .game-card:hover .card-img { transform: scale(1.05); }

    /* BODY */
    .card-body { padding: 20px 25px; text-align: center; }
    .card-desc { font-size: 18px; font-weight: 500; color: #d1d5db; line-height: 1.5; margin-bottom: 15px; }
    .flavor-text {
        font-size: 13px;
        font-style: italic;
        color: #666;
        border-top: 1px solid #333;
        padding-top: 10px;
        font-family: 'Georgia', serif;
    }

    /* HUD */
    .hud-container {
        display: flex;
        justify-content: space-around;
        background: rgba(10, 10, 15, 0.8);
        border: 1px solid #333;
        border-radius: 12px;
        padding: 12px;
        margin-bottom: 25px;
        backdrop-filter: blur(10px);
    }
    .hud-box { text-align: center; width: 22%; }
    .hud-label { font-size: 9px; color: #888; letter-spacing: 2px; font-family: 'Orbitron'; margin-bottom: 4px; }
    .hud-val { font-size: 24px; font-weight: 700; font-family: 'Rajdhani'; }

    .c-green { color: #00FF9D; text-shadow: 0 0 10px rgba(0,255,157,0.2); }
    .c-blue { color: #00E0FF; text-shadow: 0 0 10px rgba(0,224,255,0.2); }
    .c-red { color: #FF0055; text-shadow: 0 0 10px rgba(255,0,85,0.2); }
    .c-purp { color: #BD00FF; text-shadow: 0 0 10px rgba(189,0,255,0.2); }

    /* BUTTONS */
    .stButton > button {
        background: linear-gradient(180deg, #2b2b35 0%, #1a1a20 100%) !important;
        border: 1px solid #444 !important;
        color: #e0e6ed !important;
        font-family: 'Orbitron', sans-serif !important;
        font-size: 14px !important;
        padding: 16px !important;
        transition: all 0.2s ease !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .stButton > button:hover {
        border-color: #00E0FF !important;
        box-shadow: 0 0 20px rgba(0, 224, 255, 0.15) !important;
        color: #fff !important;
        transform: translateY(-2px);
    }
    
    /* BOSS OVERLAY */
    .boss-mode {
        border: 2px solid #FF0000;
        box-shadow: 0 0 20px #FF0000;
    }
</style>
""", unsafe_allow_html=True)

# --- DATA LOADER ---
@st.cache_data
def load_scenarios():
    try:
        with open('scenarios.json', 'r') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        st.error("scenarios.json not found! Please ensure the file exists.")
        return []

def get_deck_by_type(all_cards, card_type):
    # Filter cards based on type (LEGENDARY, BOSS, or standard)
    if card_type == "STANDARD":
        return [c for c in all_cards if "BOSS" not in c['type'] and "LEGENDARY" not in c['type']]
    elif card_type == "LEGENDARY":
        return [c for c in all_cards if c['type'] == "LEGENDARY"]
    elif card_type == "BOSS":
        # Sort boss cards by ID to ensure order (apt_1, apt_2, etc)
        boss_cards = [c for c in all_cards if "BOSS" in c['type']]
        return sorted(boss_cards, key=lambda x: x['id'])
    return []

# --- GAME ENGINE ---

def init_game():
    # Load Data
    all_cards = load_scenarios()
    
    if 'stats' not in st.session_state:
        # HARDER STARTING STATS
        st.session_state.stats = {'budget': 40, 'rep': 50, 'risk': 20, 'bandwidth': 30}
    if 'week' not in st.session_state:
        st.session_state.week = 1
    if 'history' not in st.session_state:
        st.session_state.history = []
    
    # Initialize Decks in Session State
    if 'standard_deck' not in st.session_state:
        deck = get_deck_by_type(all_cards, "STANDARD")
        random.shuffle(deck)
        st.session_state.standard_deck = deck
        st.session_state.legendary_deck = get_deck_by_type(all_cards, "LEGENDARY")
        st.session_state.boss_deck = get_deck_by_type(all_cards, "BOSS")
    
    # Boss Logic
    if 'boss_mode' not in st.session_state:
        st.session_state.boss_mode = False
        st.session_state.boss_stage = 0
    
    # Initial Draw
    if 'current_card' not in st.session_state:
        draw_card()

def draw_card():
    # 1. BOSS CHECK
    if st.session_state.boss_mode:
        if st.session_state.boss_stage < len(st.session_state.boss_deck):
            st.session_state.current_card = st.session_state.boss_deck[st.session_state.boss_stage]
            return
        else:
            # Boss Defeated
            st.session_state.boss_mode = False
            st.session_state.boss_stage = 0
            st.toast("🏆 BOSS DEFEATED! Reputation +20")
            st.session_state.stats['rep'] += 20

    # 2. TRIGGER BOSS (5% Chance after week 3)
    if not st.session_state.boss_mode and random.random() < 0.05 and st.session_state.week > 3:
        st.session_state.boss_mode = True
        st.session_state.boss_stage = 0
        st.session_state.current_card = st.session_state.boss_deck[0]
        st.toast("🚨 ALERT: APT GROUP DETECTED!")
        return

    # 3. LEGENDARY CARD (5% Chance)
    if random.random() < 0.05 and st.session_state.legendary_deck:
        st.session_state.current_card = random.choice(st.session_state.legendary_deck)
        st.toast("✨ LEGENDARY EVENT!")
        return

    # 4. STANDARD DRAW
    # Refill if empty
    if not st.session_state.standard_deck:
        all_cards = load_scenarios()
        deck = get_deck_by_type(all_cards, "STANDARD")
        random.shuffle(deck)
        st.session_state.standard_deck = deck
    
    if st.session_state.standard_deck:
        st.session_state.current_card = st.session_state.standard_deck.pop()

def apply_effect(impact, choice_text):
    # Update Stats
    for k, v in impact.items():
        st.session_state.stats[k] = max(0, min(100, st.session_state.stats[k] + v))
    
    # Log
    st.session_state.history.insert(0, f"Week {st.session_state.week}: {choice_text}")
    
    # Advance Turn
    st.session_state.week += 1
    
    # Advance Boss State if active
    if st.session_state.boss_mode:
        st.session_state.boss_stage += 1
        
    draw_card()
    time.sleep(0.1)
    st.rerun()

def get_impact_string(impact):
    parts = []
    for k, v in impact.items():
        if v > 0: parts.append(f"📈 {k.upper()}")
        elif v < 0: parts.append(f"📉 {k.upper()}")
    return " | ".join(parts) if parts else "No major impact"

init_game()

# --- RENDER UI ---

# 1. SIDEBAR
with st.sidebar:
    st.markdown("### 🎒 CISO LOGS")
    st.progress(min(100, int((st.session_state.week / 52) * 100)), text=f"Week {st.session_state.week} / 52")
    for log in st.session_state.history[:6]:
        st.caption(log)
    if st.button("🛑 RESIGN"):
        st.session_state.clear()
        st.rerun()

# 2. WIN / LOSS CHECKS
s = st.session_state.stats

# LOSS CONDITIONS
if s['risk'] >= 100:
    st.error("💀 GAME OVER: DATA BREACH")
    st.markdown("The New York Times just published your emails. Congress is calling.")
    if st.button("Try Again"): st.session_state.clear(); st.rerun()
    st.stop()
elif s['budget'] <= 0:
    st.error("💸 GAME OVER: BANKRUPTCY")
    st.markdown("The CFO dissolved your department. You now work at Best Buy.")
    if st.button("Try Again"): st.session_state.clear(); st.rerun()
    st.stop()
elif s['rep'] <= 0:
    st.error("📉 GAME OVER: FIRED")
    st.markdown("The Board voted 10-0 to terminate your contract. Your badge doesn't work.")
    if st.button("Try Again"): st.session_state.clear(); st.rerun()
    st.stop()
elif s['bandwidth'] <= 0:
    st.error("😫 GAME OVER: BURNOUT")
    st.markdown("Your entire team quit on the same day. You are the only one left.")
    if st.button("Try Again"): st.session_state.clear(); st.rerun()
    st.stop()

# WIN CONDITION
if st.session_state.week >= 52:
    st.balloons()
    st.success("🎉 VICTORY: YOU SURVIVED THE YEAR!")
    st.markdown(f"""
    ### PERFORMANCE REVIEW
    - **Final Budget:** ${s['budget']}k
    - **Reputation:** {s['rep']}/100
    - **Risk Level:** {s['risk']}%
    
    *The Board has approved your contract renewal.*
    """)
    if st.button("Start Year 2 (Reset)"): st.session_state.clear(); st.rerun()
    st.stop()

# 3. STATS HUD
st.markdown(f"""
<div class="hud-container">
    <div class="hud-box"><div class="hud-label">BUDGET</div><div class="hud-val c-green">${s['budget']}k</div></div>
    <div class="hud-box"><div class="hud-label">TRUST</div><div class="hud-val c-blue">{s['rep']}</div></div>
    <div class="hud-box"><div class="hud-label">RISK</div><div class="hud-val c-red">{s['risk']}%</div></div>
    <div class="hud-box"><div class="hud-label">TEAM</div><div class="hud-val c-purp">{s['bandwidth']}</div></div>
</div>
""", unsafe_allow_html=True)

# 4. CARD RENDER
if 'current_card' in st.session_state and st.session_state.current_card:
    card = st.session_state.current_card

    # Dynamic Border Color for Boss Mode
    border_class = "boss-mode" if st.session_state.boss_mode else ""

    st.markdown(f"""
    <div class="game-card {border_class}">
        <div class="card-inner">
            <div class="card-header">
                <div class="card-title">{card['title']}</div>
                <div class="card-type-badge">{card['type']}</div>
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

    # 5. ACTION BUTTONS
    c1, c2 = st.columns(2)
    with c1:
        if st.button(f"⬅ {card['choice_a']}", help=get_impact_string(card['impact_a'])):
            apply_effect(card['impact_a'], card['choice_a'])
    with c2:
        if st.button(f"➡ {card['choice_b']}", help=get_impact_string(card['impact_b'])):
            apply_effect(card['impact_b'], card['choice_b'])
else:
    st.error("No card loaded. Check scenarios.json")
