import streamlit as st
import random
import time

# --- CONFIGURATION ---
st.set_page_config(page_title="CISO Commander", page_icon="🛡️", layout="centered")

# --- CUSTOM CSS (The "Corporate Arcade" Look) ---
st.markdown("""
<style>
    /* Global Font & Background */
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;700&display=swap');
    
    .stApp {
        background-color: #121212;
        color: #ffffff;
        font-family: 'Space Grotesk', sans-serif;
    }
    
    /* THE GAME CARD */
    .game-card {
        background-color: #1E1E24;
        border: 4px solid #444;
        border-radius: 20px;
        overflow: hidden;
        margin: 20px auto;
        max-width: 600px;
        box-shadow: 10px 10px 0px #000; /* Hard shadow for cartoon feel */
        transition: transform 0.2s;
    }
    .card-header {
        background-color: #2D2D35;
        padding: 15px;
        border-bottom: 4px solid #444;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .card-badge {
        background-color: #FF0055;
        color: white;
        padding: 5px 15px;
        border-radius: 50px;
        font-weight: bold;
        font-size: 12px;
        border: 2px solid #fff;
        text-transform: uppercase;
    }
    .card-img-container {
        width: 100%;
        height: 250px;
        background-color: #000;
        overflow: hidden;
        border-bottom: 4px solid #444;
    }
    .card-img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }
    .card-body { padding: 30px; text-align: center; }
    .card-title { font-size: 28px; font-weight: 800; margin-bottom: 10px; color: #fff; }
    .card-text { font-size: 18px; color: #ccc; line-height: 1.5; margin-bottom: 20px; }

    /* STATS DASHBOARD */
    .stats-container {
        display: flex;
        justify-content: space-between;
        background: #1E1E24;
        border: 3px solid #444;
        border-radius: 15px;
        padding: 10px;
        margin-bottom: 20px;
        box-shadow: 5px 5px 0px #000;
    }
    .stat-item { text-align: center; flex: 1; }
    .stat-label { font-size: 10px; font-weight: bold; color: #888; text-transform: uppercase; }
    .stat-val { font-size: 24px; font-weight: 800; }
    
    .c-green { color: #00FF9D; }
    .c-blue { color: #00E0FF; }
    .c-red { color: #FF4D4D; }
    .c-purp { color: #BD00FF; }

    /* BUTTONS */
    div.stButton > button {
        background-color: #2D2D35;
        color: white;
        border: 3px solid #555;
        border-radius: 12px;
        padding: 15px;
        font-weight: 800;
        font-size: 16px;
        width: 100%;
        box-shadow: 0px 5px 0px #000;
        transition: all 0.1s;
    }
    div.stButton > button:hover {
        transform: translateY(-2px);
        border-color: #BD00FF;
        color: #BD00FF;
    }
    div.stButton > button:active {
        transform: translateY(2px);
        box-shadow: 0px 0px 0px #000;
    }
    
    /* TOOLTIP FIX (Make them more visible) */
    div[data-baseweb="tooltip"] {
        background-color: #333 !important;
        color: #fff !important;
    }

</style>
""", unsafe_allow_html=True)

# --- GAME DATA (Now with 9 Scenarios) ---
EVENTS = [
    {
        "id": 1,
        "type": "INCIDENT",
        "image": "https://img.freepik.com/free-vector/hacker-operating-laptop-cartoon-icon-illustration-technology-icon-concept-isolated-flat-cartoon-style_138676-2387.jpg", 
        "title": "Ransomware!",
        "text": "A skull pops up on the CFO's laptop. They want 50 BTC or the financial data gets leaked.",
        "choice_a": "Pay the Ransom ($$$)",
        "choice_b": "Format & Restore (Time)",
        "impact_a": {"budget": -25, "risk": -10, "rep": -5, "bandwidth": 0},
        "impact_b": {"budget": 0, "risk": +5, "rep": +5, "bandwidth": -25}
    },
    {
        "id": 2,
        "type": "STRATEGY",
        "image": "https://img.freepik.com/free-vector/robotic-artificial-intelligence-technology-smart-lerning-from-bigdata_1150-48136.jpg", 
        "title": "Shadow AI",
        "text": "Marketing is pasting customer data into 'ChatBot Pro' (a sketchy free tool).",
        "choice_a": "Block the Tool",
        "choice_b": "Buy Enterprise License",
        "impact_a": {"budget": 0, "risk": -10, "rep": -15, "bandwidth": -5},
        "impact_b": {"budget": -15, "risk": -20, "rep": +10, "bandwidth": 0}
    },
    {
        "id": 3,
        "type": "PEOPLE",
        "image": "https://img.freepik.com/free-vector/confused-man-working-laptop-cartoon-icon-illustration_138676-2422.jpg", 
        "title": "Phishing Click",
        "text": "Dave from HR clicked a link promising 'Free Donuts'. It was a pentest... but he failed.",
        "choice_a": "Mandatory Training",
        "choice_b": "Public Shaming",
        "impact_a": {"budget": -5, "risk": -5, "rep": -5, "bandwidth": -5},
        "impact_b": {"budget": 0, "risk": 0, "rep": -20, "bandwidth": 0}
    },
    {
        "id": 4,
        "type": "AUDIT",
        "image": "https://img.freepik.com/free-vector/checklist-concept-illustration_114360-479.jpg", 
        "title": "Surprise Audit",
        "text": "A regulator is here early. The evidence folder is... messy.",
        "choice_a": "Delay Them (Stall)",
        "choice_b": "Show What We Have",
        "impact_a": {"budget": 0, "risk": +5, "rep": -10, "bandwidth": -10},
        "impact_b": {"budget": 0, "risk": +15, "rep": +5, "bandwidth": 0}
    },
    {
        "id": 5,
        "type": "VENDOR",
        "image": "https://img.freepik.com/free-vector/business-deal-cartoon-concept_1284-11440.jpg",
        "title": "Sales Override",
        "text": "VP of Sales wants to bypass the security review for a 'critical' new vendor.",
        "choice_a": "Block (Follow Process)",
        "choice_b": "Allow (Speed)",
        "impact_a": {"budget": 0, "risk": -5, "rep": -15, "bandwidth": 0},
        "impact_b": {"budget": 0, "risk": +20, "rep": +10, "bandwidth": 0}
    },
    {
        "id": 6,
        "type": "INFRA",
        "image": "https://img.freepik.com/free-vector/server-room-concept-illustration_114360-437.jpg",
        "title": "Cloud Bill Shock",
        "text": "A developer left a massive GPU cluster running all weekend. It cost $20k.",
        "choice_a": "Eat the Cost",
        "choice_b": "Restrict Access",
        "impact_a": {"budget": -20, "risk": 0, "rep": 0, "bandwidth": 0},
        "impact_b": {"budget": 0, "risk": -5, "rep": -10, "bandwidth": -5}
    },
    {
        "id": 7,
        "type": "PEOPLE",
        "image": "https://img.freepik.com/free-vector/tired-worker-concept-illustration_114360-534.jpg",
        "title": "Burnout Warning",
        "text": "Your lead engineer is exhausted and threatening to quit.",
        "choice_a": "Give Bonus ($$$)",
        "choice_b": "Mandatory Time Off",
        "impact_a": {"budget": -10, "risk": 0, "rep": +5, "bandwidth": +10},
        "impact_b": {"budget": 0, "risk": +10, "rep": +5, "bandwidth": -10}
    },
    {
        "id": 8,
        "type": "INCIDENT",
        "image": "https://img.freepik.com/free-vector/bug-fixing-concept-illustration_114360-3945.jpg",
        "title": "Legacy Code",
        "text": "A critical vulnerability was found in a system nobody has touched in 5 years.",
        "choice_a": "Rewrite It (Hard)",
        "choice_b": "WAF It (Band-aid)",
        "impact_a": {"budget": -10, "risk": -20, "rep": +5, "bandwidth": -25},
        "impact_b": {"budget": -5, "risk": +10, "rep": 0, "bandwidth": 0}
    },
    {
        "id": 9,
        "type": "STRATEGY",
        "image": "https://img.freepik.com/free-vector/public-relations-concept-illustration_114360-2445.jpg",
        "title": "Journalist Inquiry",
        "text": "A reporter is asking about a 'rumored' breach. It's technically false, but close.",
        "choice_a": "No Comment",
        "choice_b": "Deny Everything",
        "impact_a": {"budget": 0, "risk": 0, "rep": -10, "bandwidth": 0},
        "impact_b": {"budget": 0, "risk": +15, "rep": +10, "bandwidth": 0}
    }
]

# --- GAME STATE ---
def init_game():
    if 'game_active' not in st.session_state: st.session_state['game_active'] = False
    if 'stats' not in st.session_state: st.session_state['stats'] = {'budget': 60, 'rep': 50, 'risk': 20, 'bandwidth': 50}
    if 'inventory' not in st.session_state: st.session_state['inventory'] = {'scapegoat': 1}
    if 'deck' not in st.session_state: refill_deck()
    if 'current_card' not in st.session_state: draw_card()
    if 'week' not in st.session_state: st.session_state['week'] = 1
    if 'history' not in st.session_state: st.session_state['history'] = []

def refill_deck():
    # Create a fresh shuffled list of ALL event IDs
    st.session_state['deck'] = list(range(len(EVENTS)))
    random.shuffle(st.session_state['deck'])

def draw_card():
    # If deck is empty, reshuffle
    if not st.session_state['deck']:
        refill_deck()
    
    # Pop one unique card index
    idx = st.session_state['deck'].pop()
    st.session_state['current_card'] = EVENTS[idx]

def get_impact_string(impact):
    """Returns a string preview of what stats change (e.g. '📉 Budget | 📈 Risk')"""
    parts = []
    for k, v in impact.items():
        if v > 0: parts.append(f"📈 {k.title()}")
        elif v < 0: parts.append(f"📉 {k.title()}")
    return " | ".join(parts) if parts else "No major impact"

def apply_effect(impact, choice_text):
    for k, v in impact.items():
        st.session_state['stats'][k] = max(0, min(100, st.session_state['stats'][k] + v))
    
    st.session_state['history'].insert(0, f"Week {st.session_state['week']}: {choice_text}")
    st.session_state['week'] += 1
    draw_card()
    time.sleep(0.1)
    st.rerun()

def use_powerup(name):
    if st.session_state['inventory'].get(name, 0) > 0:
        st.session_state['inventory'][name] -= 1
        st.toast(f"Used {name.upper()}! Card skipped.")
        draw_card()
        st.rerun()

init_game()

# --- START MENU ---
if not st.session_state['game_active']:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; font-size: 72px; text-shadow: 4px 4px #BD00FF;'>👾 CISO ARCADE</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 20px;'>Can you survive 52 weeks without getting fired?</p>", unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns([1,2,1])
    with c2:
        if st.button("INSERT COIN (START GAME)", use_container_width=True):
            st.session_state['game_active'] = True
            st.rerun()

else:
    # --- MAIN GAME UI ---
    
    # 1. SIDEBAR
    with st.sidebar:
        st.markdown("### 🎒 TOOLKIT")
        scape_count = st.session_state['inventory']['scapegoat']
        if scape_count > 0:
            st.info(f"🃏 **Scapegoat ({scape_count})**\n\nSkip one crisis.")
            if st.button("Use Card"): use_powerup('scapegoat')
        else:
            st.markdown("*(Empty)*")
            
        st.divider()
        st.markdown("### 📜 LOGS")
        for log in st.session_state['history'][:5]:
            st.caption(log)
            
        if st.button("🛑 QUIT"):
            st.session_state.clear()
            st.rerun()

    # 2. GAME OVER CHECK
    s = st.session_state['stats']
    if s['risk'] >= 100:
        st.error("💀 GAME OVER: You were breached.")
        if st.button("Retry"): st.session_state.clear(); st.rerun()
        st.stop()
    elif s['budget'] <= 0:
        st.error("💸 GAME OVER: Bankrupt.")
        if st.button("Retry"): st.session_state.clear(); st.rerun()
        st.stop()

    # 3. HUD
    st.markdown(f"#### 🗓️ WEEK {st.session_state['week']} / 52")
    st.markdown(f"""
    <div class="stats-container">
        <div class="stat-item"><div class="stat-label">Budget</div><div class="stat-val c-green">${s['budget']}k</div></div>
        <div class="stat-item"><div class="stat-label">Reputation</div><div class="stat-val c-blue">{s['rep']}</div></div>
        <div class="stat-item"><div class="stat-label">Risk Level</div><div class="stat-val c-red">{s['risk']}%</div></div>
        <div class="stat-item"><div class="stat-label">Team Health</div><div class="stat-val c-purp">{s['bandwidth']}</div></div>
    </div>
    """, unsafe_allow_html=True)

    # 4. CARD
    card = st.session_state['current_card']
    st.markdown(f"""
    <div class="game-card">
        <div class="card-header">
            <span style="font-weight:bold; color:#888;">EVENT #{card['id']}</span>
            <span class="card-badge">{card['type']}</span>
        </div>
        <div class="card-img-container"><img src="{card['image']}" class="card-img"></div>
        <div class="card-body">
            <div class="card-title">{card['title']}</div>
            <div class="card-text">{card['text']}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 5. CONTROLS (With Hover Tooltips!)
    c1, c2 = st.columns(2)
    with c1:
        if st.button(f"⬅️ {card['choice_a']}", help=get_impact_string(card['impact_a'])):
            apply_effect(card['impact_a'], card['choice_a'])
    with c2:
        if st.button(f"➡️ {card['choice_b']}", help=get_impact_string(card['impact_b'])):
            apply_effect(card['impact_b'], card['choice_b'])
