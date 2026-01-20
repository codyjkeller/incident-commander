import streamlit as st
import random
import time

# --- CONFIGURATION ---
st.set_page_config(page_title="CISO Commander", page_icon="🛡️", layout="centered")

# --- CUSTOM CSS ---
st.markdown("""
<style>
    /* Main Background */
    .stApp {
        background-color: #0b0d12;
        color: #e0e6ed;
        font-family: 'Helvetica Neue', sans-serif;
    }
    
    /* CARD STYLING */
    .game-card {
        background-color: #161b22;
        border-radius: 12px;
        padding: 0px;
        margin: 20px auto;
        box-shadow: 0 20px 50px rgba(0,0,0,0.6);
        border: 1px solid #30363d;
        text-align: center;
        overflow: hidden;
        max-width: 650px;
    }
    .card-img-container {
        width: 100%;
        height: 250px;
        background-color: #000;
        overflow: hidden;
        border-bottom: 1px solid #30363d;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .card-img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        opacity: 0.9;
    }
    .card-content { padding: 30px; }
    .card-title { font-size: 24px; font-weight: 700; color: #fff; margin-bottom: 10px; letter-spacing: 0.5px; }
    .card-desc { font-size: 16px; color: #8b949e; line-height: 1.5; margin-bottom: 25px; }

    /* STATS BAR */
    .stat-box {
        background-color: #161b22;
        padding: 12px;
        border-radius: 8px;
        text-align: center;
        border: 1px solid #30363d;
    }
    .stat-label { font-size: 11px; color: #8b949e; text-transform: uppercase; letter-spacing: 1px; font-weight: 600; }
    .stat-value { font-size: 24px; font-weight: 700; font-family: 'Courier New', monospace; }
    
    /* Colors */
    .c-green { color: #3fb950; }
    .c-blue { color: #58a6ff; }
    .c-red { color: #f85149; }
    .c-yellow { color: #d29922; }

    /* BUTTONS */
    div.stButton > button {
        background-color: #21262d; 
        color: #c9d1d9;
        border: 1px solid #30363d;
        border-radius: 6px;
        padding: 12px 20px;
        font-size: 14px;
        font-weight: 600;
        width: 100%;
        transition: all 0.2s;
    }
    div.stButton > button:hover {
        background-color: #30363d;
        border-color: #8b949e;
        color: #fff;
    }

    /* FEEDBACK PILL */
    .feedback-pill {
        background: #161b22;
        border: 1px solid #30363d;
        padding: 8px 16px;
        border-radius: 20px;
        font-size: 12px;
        color: #8b949e;
        display: inline-block;
    }
</style>
""", unsafe_allow_html=True)

# --- GAME DATA ---
# NOTE: Replace 'https://placehold.co/600x400/161b22/FFF' with actual image paths or URLs
EVENTS = [
    {
        "id": 1,
        "image": "https://images.unsplash.com/photo-1563206767-5b1d97299337?auto=format&fit=crop&w=800&q=80", # Hacker/Code
        "title": "Ransomware Detected",
        "text": "SOC alerts a lateral movement attempt in Finance. The payload is encrypted.",
        "choice_a": "Isolate Subnet (Downtime)",
        "choice_b": "Monitor to Trace Source",
        "impact_a": {"budget": 0, "risk": -15, "rep": -5, "bandwidth": -5},
        "impact_b": {"budget": 0, "risk": +20, "rep": 0, "bandwidth": -10}
    },
    {
        "id": 2,
        "image": "https://images.unsplash.com/photo-1573164713714-d95e436ab8d6?auto=format&fit=crop&w=800&q=80", # Meeting/Audit
        "title": "Vendor Compliance Fail",
        "text": "A critical AI vendor failed their SOC 2 Type 2. The CTO needs this tool for a product launch.",
        "choice_a": "Block Integration",
        "choice_b": "Accept Risk Exception",
        "impact_a": {"budget": 0, "risk": -5, "rep": -10, "bandwidth": -5},
        "impact_b": {"budget": 0, "risk": +15, "rep": +5, "bandwidth": 0}
    },
    {
        "id": 3,
        "image": "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?auto=format&fit=crop&w=800&q=80", # Matrix Code
        "title": "Zero-Day Rumors",
        "text": "Dark web chatter suggests a vulnerability in our VPN concentrator.",
        "choice_a": "Emergency Patch (Overtime)",
        "choice_b": "Wait for Vendor Advisory",
        "impact_a": {"budget": -10, "risk": -10, "rep": +5, "bandwidth": -20},
        "impact_b": {"budget": 0, "risk": +25, "rep": 0, "bandwidth": 0}
    },
    {
        "id": 4,
        "image": "https://images.unsplash.com/photo-1556761175-5973dc0f32e7?auto=format&fit=crop&w=800&q=80", # Boardroom
        "title": "Budget Cuts",
        "text": "CFO asks you to reduce spend by 10% to help Q4 numbers.",
        "choice_a": "Cut Training Budget",
        "choice_b": "Reduce Tool Licensing",
        "impact_a": {"budget": +10, "risk": +5, "rep": -5, "bandwidth": +5},
        "impact_b": {"budget": +10, "risk": +15, "rep": 0, "bandwidth": -5}
    },
]

# --- STATE MANAGEMENT ---
def init_state():
    if 'game_active' not in st.session_state: st.session_state['game_active'] = False
    if 'stats' not in st.session_state: st.session_state['stats'] = {'budget': 50, 'rep': 50, 'risk': 20, 'bandwidth': 50}
    if 'week' not in st.session_state: st.session_state['week'] = 1
    if 'deck' not in st.session_state: refill_deck()
    if 'current_card' not in st.session_state: draw_card()
    if 'last_impact' not in st.session_state: st.session_state['last_impact'] = None

def refill_deck():
    deck = list(range(len(EVENTS)))
    random.shuffle(deck)
    st.session_state['deck'] = deck

def draw_card():
    if not st.session_state['deck']: refill_deck()
    idx = st.session_state['deck'].pop()
    st.session_state['current_card'] = EVENTS[idx]

def apply_choice(impact):
    st.session_state['last_impact'] = impact
    for k, v in impact.items():
        st.session_state['stats'][k] = max(0, min(100, st.session_state['stats'][k] + v))
    st.session_state['week'] += 1
    draw_card()
    time.sleep(0.1)
    st.rerun()

init_state()

# --- UI COMPONENTS ---
def render_stats():
    s = st.session_state['stats']
    c1, c2, c3, c4 = st.columns(4)
    c1.markdown(f"""<div class="stat-box"><div class="stat-label">Budget</div><div class="stat-value c-green">{s['budget']}k</div></div>""", unsafe_allow_html=True)
    c2.markdown(f"""<div class="stat-box"><div class="stat-label">Trust</div><div class="stat-value c-blue">{s['rep']}</div></div>""", unsafe_allow_html=True)
    c3.markdown(f"""<div class="stat-box"><div class="stat-label">Risk</div><div class="stat-value c-red">{s['risk']}%</div></div>""", unsafe_allow_html=True)
    c4.markdown(f"""<div class="stat-box"><div class="stat-label">Team</div><div class="stat-value c-yellow">{s['bandwidth']}</div></div>""", unsafe_allow_html=True)

def render_feedback():
    if st.session_state['last_impact']:
        imp = st.session_state['last_impact']
        changes = []
        for k, v in imp.items():
            if v != 0:
                symbol = "▲" if v > 0 else "▼"
                color = "#3fb950" if (k != 'risk' and v > 0) or (k == 'risk' and v < 0) else "#f85149"
                changes.append(f"<span style='color:{color}; margin: 0 10px;'>{k.upper()} {symbol}{abs(v)}</span>")
        
        if changes:
            st.markdown(f"<div style='text-align:center; margin-top:10px;'><div class='feedback-pill'>{''.join(changes)}</div></div>", unsafe_allow_html=True)

# --- SCREENS ---
if not st.session_state['game_active']:
    # START SCREEN
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; font-size: 50px;'>🛡️ CISO COMMANDER</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #8b949e;'>Survive 1 Year as the CISO of a targeted enterprise.</p>", unsafe_allow_html=True)
    
    # Just a placeholder hero image for the menu
    st.image("https://images.unsplash.com/photo-1550751827-4bd374c3f58b?auto=format&fit=crop&w=1000&q=80", use_column_width=True)
    
    if st.button("INITIALIZE SEQUENCE", use_container_width=True):
        st.session_state['game_active'] = True
        st.rerun()

else:
    # MAIN GAME
    with st.sidebar:
        st.header("PAUSE")
        st.progress(min(100, st.session_state['week'] * 2), text=f"Week {st.session_state['week']} / 52")
        if st.button("Resign (Reset)"):
            st.session_state.clear()
            st.rerun()
            
    # Check Game Over
    s = st.session_state['stats']
    if s['risk'] >= 100 or s['budget'] <= 0 or s['bandwidth'] <= 0:
        st.error("❌ TERMINATED: CRITICAL FAILURE")
        st.markdown(f"You survived {st.session_state['week']} Weeks.")
        if st.button("RESTART SYSTEM"):
            st.session_state.clear()
            st.rerun()
        st.stop()

    render_stats()
    render_feedback()
    
    card = st.session_state['current_card']
    
    # CARD CONTAINER
    st.markdown(f"""
    <div class="game-card">
        <div class="card-img-container">
            <img src="{card['image']}" class="card-img">
        </div>
        <div class="card-content">
            <div class="card-title">{card['title']}</div>
            <div class="card-desc">{card['text']}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # BUTTONS
    c1, c2 = st.columns(2)
    with c1:
        if st.button(f"{card['choice_a']}", use_container_width=True):
            apply_choice(card['impact_a'])
    with c2:
        if st.button(f"{card['choice_b']}", use_container_width=True):
            apply_choice(card['impact_b'])
