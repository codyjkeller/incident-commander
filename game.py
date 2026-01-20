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
        background-color: #0E1117;
        color: #FAFAFA;
    }
    
    /* CARD STYLING */
    .game-card {
        background-color: #1E232F;
        border-radius: 20px;
        padding: 40px;
        margin: 20px auto;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        border: 2px solid #333;
        text-align: center;
        transition: all 0.3s ease;
    }
    .game-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(0,229,255,0.1); /* Subtle Blue Glow */
        border-color: #00E5FF;
    }
    .card-emoji { font-size: 80px; margin-bottom: 20px; }
    .card-title { font-size: 26px; font-weight: 800; color: #FFF; margin-bottom: 15px; }
    .card-desc { font-size: 18px; color: #CCC; line-height: 1.6; margin-bottom: 30px; }

    /* STATS BAR */
    .stat-box {
        background-color: #262730;
        padding: 15px;
        border-radius: 12px;
        text-align: center;
        border: 1px solid #444;
        box-shadow: inset 0 0 10px rgba(0,0,0,0.5);
    }
    .stat-label { font-size: 12px; color: #AAA; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 5px; }
    .stat-value { font-size: 28px; font-weight: 900; }
    
    /* Neon Colors */
    .color-budget { color: #00FF94; text-shadow: 0 0 10px rgba(0,255,148,0.3); }
    .color-rep { color: #00E5FF; text-shadow: 0 0 10px rgba(0,229,255,0.3); }
    .color-risk { color: #FF2E63; text-shadow: 0 0 10px rgba(255,46,99,0.3); }
    .color-bw { color: #FFC700; text-shadow: 0 0 10px rgba(255,199,0,0.3); }

    /* BUTTON FIXES */
    /* Force buttons to be visible and distinct */
    div.stButton > button {
        background-color: #2B313E; 
        color: #FFFFFF;
        border: 1px solid #4A4A4A;
        border-radius: 10px;
        padding: 15px 20px;
        font-size: 16px;
        font-weight: bold;
        width: 100%;
        transition: all 0.2s;
    }
    div.stButton > button:hover {
        background-color: #3A4250;
        border-color: #00E5FF;
        color: #00E5FF;
        transform: scale(1.02);
    }

    /* IMPACT DELTAS (The visual cues) */
    .impact-positive { color: #00FF94; font-weight: bold; }
    .impact-negative { color: #FF2E63; font-weight: bold; }
    .impact-neutral { color: #888; }
    
</style>
""", unsafe_allow_html=True)

# --- GAME DATA ---
EVENTS = [
    {
        "id": 1,
        "emoji": "💀",
        "title": "Ransomware Attack",
        "text": "Finance reports their laptops are encrypted. Hackers want $50k in Bitcoin immediately.",
        "choice_a": "Pay Ransom ($50k)",
        "choice_b": "Restore Backup (2 Days)",
        "impact_a": {"budget": -20, "risk": -10, "rep": -5, "bandwidth": 0},
        "impact_b": {"budget": 0, "risk": +5, "rep": +5, "bandwidth": -20}
    },
    {
        "id": 2,
        "emoji": "🕵️",
        "title": "Vendor Audit Fail",
        "text": "A critical AI vendor failed their SOC 2 audit. The CEO wants to use them anyway.",
        "choice_a": "Block Vendor",
        "choice_b": "Sign Waiver",
        "impact_a": {"budget": 0, "risk": -10, "rep": +10, "bandwidth": -5},
        "impact_b": {"budget": +10, "risk": +20, "rep": -5, "bandwidth": 0}
    },
    {
        "id": 3,
        "emoji": "🐛",
        "title": "Zero-Day Leak",
        "text": "Twitter is buzzing about a flaw in our VPN. No patch exists yet.",
        "choice_a": "Kill VPN (Halt Work)",
        "choice_b": "Monitor Logs",
        "impact_a": {"budget": -10, "risk": -20, "rep": -10, "bandwidth": 0},
        "impact_b": {"budget": 0, "risk": +30, "rep": 0, "bandwidth": -10}
    },
    {
        "id": 4,
        "emoji": "🎤",
        "title": "Keynote Invite",
        "text": "You are invited to speak at Black Hat. It's great PR, but you're drowning in work.",
        "choice_a": "Accept (Travel)",
        "choice_b": "Decline (Focus)",
        "impact_a": {"budget": -5, "risk": 0, "rep": +25, "bandwidth": -20},
        "impact_b": {"budget": 0, "risk": 0, "rep": -5, "bandwidth": +10}
    },
    {
        "id": 5,
        "emoji": "💾",
        "title": "Legacy Server Dies",
        "text": "The payroll server from 1998 finally died. It wasn't backed up.",
        "choice_a": "Hire Data Recovery",
        "choice_b": "Manual Entry (All Hands)",
        "impact_a": {"budget": -15, "risk": -5, "rep": 0, "bandwidth": 0},
        "impact_b": {"budget": 0, "risk": +10, "rep": -10, "bandwidth": -30}
    }
]

# --- STATE INITIALIZATION ---
if 'game_active' not in st.session_state:
    st.session_state['game_active'] = False
if 'stats' not in st.session_state:
    st.session_state['stats'] = {'budget': 50, 'rep': 50, 'risk': 20, 'bandwidth': 50}
if 'week' not in st.session_state:
    st.session_state['week'] = 1
if 'deck' not in st.session_state:
    deck = list(range(len(EVENTS)))
    random.shuffle(deck)
    st.session_state['deck'] = deck
if 'current_card_idx' not in st.session_state:
    st.session_state['current_card_idx'] = st.session_state['deck'].pop()
if 'last_impact' not in st.session_state:
    st.session_state['last_impact'] = None

# --- FUNCTIONS ---
def start_game():
    st.session_state['game_active'] = True
    st.session_state['stats'] = {'budget': 50, 'rep': 50, 'risk': 20, 'bandwidth': 50}
    st.session_state['week'] = 1
    st.session_state['last_impact'] = None
    st.rerun()

def apply_choice(impact):
    # Store impact for visual cue on next turn
    st.session_state['last_impact'] = impact
    
    # Update Stats
    for key, value in impact.items():
        st.session_state['stats'][key] = max(0, min(100, st.session_state['stats'][key] + value))
    
    # Advance Turn
    st.session_state['week'] += 1
    if not st.session_state['deck']:
        deck = list(range(len(EVENTS)))
        random.shuffle(deck)
        st.session_state['deck'] = deck
    st.session_state['current_card_idx'] = st.session_state['deck'].pop()
    
    time.sleep(0.1)
    st.rerun()

def render_impact_cue():
    """Displays a summary of what changed in the last turn."""
    if st.session_state['last_impact']:
        imp = st.session_state['last_impact']
        cols = st.columns(4)
        
        # Helper to format delta
        def fmt(val):
            if val > 0: return f"⬆ +{val}", "impact-positive"
            if val < 0: return f"⬇ {val}", "impact-negative"
            return "-", "impact-neutral"

        # Show deltas under the stats
        items = [('budget', imp['budget']), ('rep', imp['rep']), ('risk', imp['risk']), ('bandwidth', imp['bandwidth'])]
        
        # We create a small notification bar
        html_str = "<div style='text-align:center; padding: 10px; background: rgba(255,255,255,0.05); border-radius:10px; margin-bottom: 20px; display: flex; justify-content: space-around;'>"
        for k, v in items:
            text, css = fmt(v)
            if v != 0:
                html_str += f"<span>{k.title()}: <span class='{css}'>{text}</span></span>"
        html_str += "</div>"
        st.markdown(html_str, unsafe_allow_html=True)

# --- START SCREEN ---
if not st.session_state['game_active']:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; font-size: 60px;'>🛡️ Incident Commander</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 20px; color: #888;'>Balance Budget, Reputation, and Risk as the new CISO.</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 START NEW CAREER", use_container_width=True):
            start_game()
            
    st.markdown("<p style='text-align: center; font-size: 14px; color: #555; margin-top: 50px;'>v1.0 | Created with Streamlit</p>", unsafe_allow_html=True)

else:
    # --- MAIN GAME LOOP ---
    
    # 1. SIDEBAR MENU
    with st.sidebar:
        st.title("Pause Menu")
        st.write("Current Career:")
        st.progress(st.session_state['week'] / 52, text=f"Week {st.session_state['week']}")
        if st.button("Quit / Restart"):
            st.session_state['game_active'] = False
            st.rerun()

    # 2. CHECK GAME OVER
    s = st.session_state['stats']
    if s['risk'] >= 100:
        st.error("💀 GAME OVER: You were breached massively. Risk hit 100%.")
        if st.button("Try Again"): start_game()
        st.stop()
    elif s['budget'] <= 0:
        st.error("💸 GAME OVER: You ran out of budget. The CFO fired you.")
        if st.button("Try Again"): start_game()
        st.stop()
    elif s['bandwidth'] <= 0:
        st.error("😫 GAME OVER: Burnout! Your entire security team quit.")
        if st.button("Try Again"): start_game()
        st.stop()

    # 3. STATS DASHBOARD
    st.markdown(f"### 📅 Week {st.session_state['week']}")
    
    c1, c2, c3, c4 = st.columns(4)
    c1.markdown(f"""<div class="stat-box"><div class="stat-label">Budget</div><div class="stat-value color-budget">{s['budget']}k</div></div>""", unsafe_allow_html=True)
    c2.markdown(f"""<div class="stat-box"><div class="stat-label">Reputation</div><div class="stat-value color-rep">{s['rep']}</div></div>""", unsafe_allow_html=True)
    c3.markdown(f"""<div class="stat-box"><div class="stat-label">Risk</div><div class="stat-value color-risk">{s['risk']}%</div></div>""", unsafe_allow_html=True)
    c4.markdown(f"""<div class="stat-box"><div class="stat-label">Bandwidth</div><div class="stat-value color-bw">{s['bandwidth']}</div></div>""", unsafe_allow_html=True)

    st.write("") # Spacer

    # 4. LAST TURN FEEDBACK
    render_impact_cue()

    # 5. RENDER CARD
    current_event = EVENTS[st.session_state['current_card_idx']]
    
    st.markdown(f"""
    <div class="game-card">
        <div class="card-emoji">{current_event['emoji']}</div>
        <div class="card-title">{current_event['title']}</div>
        <div class="card-desc">{current_event['text']}</div>
    </div>
    """, unsafe_allow_html=True)

    # 6. ACTION BUTTONS
    b1, b2 = st.columns(2)
    with b1:
        if st.button(f"⬅️ {current_event['choice_a']}", use_container_width=True):
            apply_choice(current_event['impact_a'])
    with b2:
        if st.button(f"➡️ {current_event['choice_b']}", use_container_width=True):
            apply_choice(current_event['impact_b'])
