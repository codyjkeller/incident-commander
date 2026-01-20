import streamlit as st
import random
import time

# --- CONFIGURATION & ASSETS ---
st.set_page_config(page_title="CISO Commander", page_icon="🛡️", layout="centered")

# --- CUSTOM CSS FOR "REIGNS" STYLE UI ---
st.markdown("""
<style>
    /* Main Background */
    .stApp {
        background-color: #0E1117;
        color: #FAFAFA;
    }
    
    /* The Game Card Container */
    .game-card {
        background-color: #1E232F;
        border-radius: 20px;
        padding: 40px;
        margin: 20px auto;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        border: 2px solid #333;
        text-align: center;
        max-width: 600px;
        transition: transform 0.2s;
    }
    .game-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(0,0,0,0.6);
        border-color: #4B4B4B;
    }
    
    /* Typography */
    .card-title {
        font-size: 24px;
        font-weight: bold;
        color: #E0E0E0;
        margin-bottom: 20px;
    }
    .card-emoji {
        font-size: 80px;
        margin-bottom: 20px;
    }
    .card-desc {
        font-size: 18px;
        color: #B0B0B0;
        line-height: 1.6;
        margin-bottom: 30px;
    }
    
    /* Stats Bar Custom Styling */
    .stat-box {
        background-color: #262730;
        padding: 10px;
        border-radius: 10px;
        text-align: center;
        border: 1px solid #444;
    }
    .stat-label { font-size: 12px; color: #888; text-transform: uppercase; letter-spacing: 1px; }
    .stat-value { font-size: 24px; font-weight: bold; }
    
    /* Neon Text Colors for Stats */
    .color-budget { color: #00FF94; } /* Neon Green */
    .color-rep { color: #00E5FF; }    /* Neon Blue */
    .color-risk { color: #FF2E63; }   /* Neon Red */
    .color-bw { color: #FFC700; }     /* Neon Yellow */

</style>
""", unsafe_allow_html=True)

# --- EVENT LIBRARY ---
EVENTS = [
    {
        "id": 1,
        "emoji": "💀",
        "title": "Ransomware Detected",
        "text": "An endpoint in Finance is encrypted. The attacker demands $50k in Bitcoin.",
        "choice_a": "Pay the Ransom ($50k)",
        "choice_b": "Restore from Backup (2 days)",
        "impact_a": {"budget": -20, "risk": -10, "rep": -5, "bandwidth": 0},
        "impact_b": {"budget": 0, "risk": +5, "rep": +5, "bandwidth": -20}
    },
    {
        "id": 2,
        "emoji": "🕵️",
        "title": "Vendor Audit",
        "text": "A key vendor failed their SOC 2 audit. Sales wants to onboard them anyway to close a deal.",
        "choice_a": "Block the Vendor",
        "choice_b": "Grant Exception",
        "impact_a": {"budget": 0, "risk": -10, "rep": +10, "bandwidth": -5},
        "impact_b": {"budget": +10, "risk": +20, "rep": -5, "bandwidth": 0}
    },
    {
        "id": 3,
        "emoji": "🐛",
        "title": "Zero-Day Rumor",
        "text": "Twitter is buzzing about a vulnerability in our VPN. No patch exists yet.",
        "choice_a": "Disable VPN (Halt Work)",
        "choice_b": "Monitor Logs & Pray",
        "impact_a": {"budget": -10, "risk": -20, "rep": -10, "bandwidth": 0},
        "impact_b": {"budget": 0, "risk": +30, "rep": 0, "bandwidth": -10}
    },
    {
        "id": 4,
        "emoji": "🎤",
        "title": "Tech Conference",
        "text": "You are invited to speak at Black Hat. It's great exposure but requires prep time.",
        "choice_a": "Accept Invitation",
        "choice_b": "Decline (Focus on Work)",
        "impact_a": {"budget": -5, "risk": 0, "rep": +20, "bandwidth": -15},
        "impact_b": {"budget": 0, "risk": 0, "rep": -5, "bandwidth": +5}
    },
    {
        "id": 5,
        "emoji": "🍕",
        "title": "Developer Mutiny",
        "text": "Engineers are complaining that the new security tools are 'too slow'. They want them disabled.",
        "choice_a": "Enforce Controls",
        "choice_b": "Relax Policies",
        "impact_a": {"budget": 0, "risk": -5, "rep": -15, "bandwidth": -5},
        "impact_b": {"budget": 0, "risk": +15, "rep": +10, "bandwidth": 0}
    }
]

# --- GAME STATE MANAGEMENT ---
if 'stats' not in st.session_state:
    st.session_state['stats'] = {'budget': 50, 'rep': 50, 'risk': 20, 'bandwidth': 50}
if 'week' not in st.session_state:
    st.session_state['week'] = 1
if 'deck' not in st.session_state:
    # Create a fresh shuffled deck of indices
    deck = list(range(len(EVENTS)))
    random.shuffle(deck)
    st.session_state['deck'] = deck
if 'current_card_idx' not in st.session_state:
    # Pop the first card
    st.session_state['current_card_idx'] = st.session_state['deck'].pop()

# --- HELPER FUNCTIONS ---
def update_stats(impact):
    """Updates stats and keeps them within 0-100 bounds."""
    for key, value in impact.items():
        st.session_state['stats'][key] = max(0, min(100, st.session_state['stats'][key] + value))

def next_turn():
    """Advances the game week and loads the next card."""
    st.session_state['week'] += 1
    
    # Refill deck if empty
    if not st.session_state['deck']:
        deck = list(range(len(EVENTS)))
        random.shuffle(deck)
        st.session_state['deck'] = deck
    
    # Load next card
    st.session_state['current_card_idx'] = st.session_state['deck'].pop()
    
    # Force a UI refresh
    time.sleep(0.1) # Smooth transition feel
    st.rerun()

# --- GAME OVER LOGIC ---
s = st.session_state['stats']
if s['risk'] >= 100:
    st.error("💀 GAME OVER: You were breached massively. Risk hit 100%.")
    if st.button("Restart Career"):
        st.session_state.clear()
        st.rerun()
    st.stop()
elif s['budget'] <= 0:
    st.error("💸 GAME OVER: You ran out of budget. The CFO fired you.")
    if st.button("Restart Career"):
        st.session_state.clear()
        st.rerun()
    st.stop()

# --- HEADER & STATS DISPLAY ---
st.title("👑 Incident Commander")
st.markdown(f"### 📅 Week {st.session_state['week']}")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f"""<div class="stat-box"><div class="stat-label">Budget</div><div class="stat-value color-budget">{s['budget']}</div></div>""", unsafe_allow_html=True)
with col2:
    st.markdown(f"""<div class="stat-box"><div class="stat-label">Reputation</div><div class="stat-value color-rep">{s['rep']}</div></div>""", unsafe_allow_html=True)
with col3:
    st.markdown(f"""<div class="stat-box"><div class="stat-label">Risk</div><div class="stat-value color-risk">{s['risk']}%</div></div>""", unsafe_allow_html=True)
with col4:
    st.markdown(f"""<div class="stat-box"><div class="stat-label">Bandwidth</div><div class="stat-value color-bw">{s['bandwidth']}</div></div>""", unsafe_allow_html=True)

# --- CARD RENDERER ---
current_event = EVENTS[st.session_state['current_card_idx']]

# Render the card container using HTML/CSS
st.markdown(f"""
<div class="game-card">
    <div class="card-emoji">{current_event['emoji']}</div>
    <div class="card-title">{current_event['title']}</div>
    <div class="card-desc">{current_event['text']}</div>
</div>
""", unsafe_allow_html=True)

# --- DECISION BUTTONS ---
# Using columns to center buttons slightly better
b_col1, b_col2 = st.columns(2)

with b_col1:
    if st.button(f"⬅️ {current_event['choice_a']}", use_container_width=True):
        update_stats(current_event['impact_a'])
        next_turn()

with b_col2:
    if st.button(f"➡️ {current_event['choice_b']}", use_container_width=True):
        update_stats(current_event['impact_b'])
        next_turn()
