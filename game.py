import streamlit as st
import random
import time

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

# --- GAME CONTENT ---

# 1. STANDARD DECK
STANDARD_EVENTS = [
    {
        "id": "ransomware",
        "type": "INCIDENT",
        "icon": "💀",
        "title": "Ransomware",
        "image": "https://img.freepik.com/free-vector/hacker-operating-laptop-cartoon-icon-illustration-technology-icon-concept-isolated-flat-cartoon-style_138676-2387.jpg",
        "text": "A skull pops up on the CFO's laptop. They want 50 BTC or the financial data gets leaked.",
        "flavor": "\"We accept Bitcoin or Monero. Tick tock.\"",
        "choice_a": "Pay $50k Ransom",
        "choice_b": "Rebuild (3 Days)",
        "impact_a": {"budget": -25, "risk": -10, "rep": -5, "bandwidth": 0},
        "impact_b": {"budget": 0, "risk": +5, "rep": +5, "bandwidth": -25}
    },
    {
        "id": "sales_override",
        "type": "VENDOR",
        "icon": "🤝",
        "title": "Sales Override",
        "image": "https://img.freepik.com/free-vector/business-deal-cartoon-concept_1284-11440.jpg",
        "text": "The CRO demands we whitelist a sketchy AI tool to close a $1M deal before quarter-end.",
        "flavor": "\"Just enable it for this one demo, please!\"",
        "choice_a": "Block (Policy)",
        "choice_b": "Allow (Revenue)",
        "impact_a": {"budget": 0, "risk": -5, "rep": -15, "bandwidth": 0},
        "impact_b": {"budget": +5, "risk": +20, "rep": +10, "bandwidth": 0}
    },
    {
        "id": "audit_fail",
        "type": "AUDIT",
        "icon": "📋",
        "title": "Surprise Audit",
        "image": "https://img.freepik.com/free-vector/checklist-concept-illustration_114360-479.jpg",
        "text": "The regulator walked in 2 months early. Your evidence repository is... incomplete.",
        "flavor": "\"I'd like to see your Access Control Logs for last year.\"",
        "choice_a": "Stall / Delay",
        "choice_b": "Full Transparency",
        "impact_a": {"budget": 0, "risk": +5, "rep": -10, "bandwidth": -10},
        "impact_b": {"budget": 0, "risk": +15, "rep": +5, "bandwidth": 0}
    },
    {
        "id": "shadow_ai",
        "type": "STRATEGY",
        "icon": "🤖",
        "title": "Shadow AI",
        "image": "https://img.freepik.com/free-vector/robotic-artificial-intelligence-technology-smart-lerning-from-bigdata_1150-48136.jpg",
        "text": "Marketing is pasting customer data into 'ChatBot Pro' (a sketchy free tool).",
        "flavor": "\"But it writes such good emails!\"",
        "choice_a": "Block Tool",
        "choice_b": "Buy Enterprise Lic",
        "impact_a": {"budget": 0, "risk": -10, "rep": -10, "bandwidth": -5},
        "impact_b": {"budget": -15, "risk": -20, "rep": +5, "bandwidth": 0}
    },
    {
        "id": "bug_bounty",
        "type": "INCIDENT",
        "icon": "🐛",
        "title": "Bug Bounty",
        "image": "https://img.freepik.com/free-vector/bug-fixing-concept-illustration_114360-3945.jpg",
        "text": "A researcher found a SQL Injection in our login page. They want a payout.",
        "flavor": "\"Pay me or I tweet about it.\"",
        "choice_a": "Pay ($10k)",
        "choice_b": "Ignore (Risky)",
        "impact_a": {"budget": -10, "risk": -20, "rep": +5, "bandwidth": 0},
        "impact_b": {"budget": 0, "risk": +20, "rep": -10, "bandwidth": 0}
    },
    {
        "id": "phishing_test",
        "type": "PEOPLE",
        "icon": "🎣",
        "title": "Phishing Fail",
        "image": "https://img.freepik.com/free-vector/confused-man-working-laptop-cartoon-icon-illustration_138676-2422.jpg",
        "text": "The VP of Engineering clicked your phishing test link. Again.",
        "flavor": "\"I thought I won a free iPad...\"",
        "choice_a": "Enforce Training",
        "choice_b": "Let it slide",
        "impact_a": {"budget": 0, "risk": -5, "rep": -5, "bandwidth": -5},
        "impact_b": {"budget": 0, "risk": +10, "rep": +5, "bandwidth": 0}
    }
]

# 2. RARE CARDS (5% Drop Rate)
RARE_EVENTS = [
    {
        "id": "angel_investor",
        "type": "LEGENDARY",
        "icon": "💰",
        "title": "Angel Investor",
        "image": "https://img.freepik.com/free-vector/money-bag-concept-illustration_114360-639.jpg",
        "text": "A VC is impressed by your security posture. They wrote a check specifically for your department.",
        "flavor": "\"Security is a differentiator. Here's $50k.\"",
        "choice_a": "Hire Staff",
        "choice_b": "Buy New Toys",
        "impact_a": {"budget": +50, "risk": 0, "rep": +10, "bandwidth": +30},
        "impact_b": {"budget": +20, "risk": -20, "rep": +10, "bandwidth": 0}
    },
    {
        "id": "fbi_raid",
        "type": "LEGENDARY",
        "icon": "🚨",
        "title": "FBI Takedown",
        "image": "https://img.freepik.com/free-vector/police-car-concept-illustration_114360-1288.jpg",
        "text": "The FBI seized the servers of a vendor you were worried about. The threat is gone.",
        "flavor": "\"Ladies and gentlemen, we got him.\"",
        "choice_a": "Celebrate",
        "choice_b": "Analyze Logs",
        "impact_a": {"budget": 0, "risk": -30, "rep": 0, "bandwidth": +10},
        "impact_b": {"budget": 0, "risk": -40, "rep": +5, "bandwidth": -10}
    }
]

# 3. BOSS BATTLE: APT CAMPAIGN (Sequential)
BOSS_APT = [
    {
        "id": "apt_1",
        "type": "BOSS PHASE 1",
        "icon": "☠️",
        "title": "Suspicious Login",
        "image": "https://img.freepik.com/free-vector/cyber-attack-concept-illustration_114360-1897.jpg",
        "text": "BOSS BATTLE START! \n\nA admin account just logged in from North Korea. It's 3 AM.",
        "flavor": "Phase 1/3: Initial Access",
        "choice_a": "Reset Password",
        "choice_b": "Watch & Wait",
        "impact_a": {"budget": 0, "risk": -5, "rep": 0, "bandwidth": -5},
        "impact_b": {"budget": 0, "risk": +10, "rep": 0, "bandwidth": 0}
    },
    {
        "id": "apt_2",
        "type": "BOSS PHASE 2",
        "icon": "☠️",
        "title": "Lateral Movement",
        "image": "https://img.freepik.com/free-vector/hacker-activity-concept-illustration_114360-2330.jpg",
        "text": "The attacker is scanning the internal network. They found the Domain Controller.",
        "flavor": "Phase 2/3: Escalation",
        "choice_a": "Cut Internet",
        "choice_b": "Deploy Decoys",
        "impact_a": {"budget": -10, "risk": -10, "rep": -20, "bandwidth": 0},
        "impact_b": {"budget": 0, "risk": +5, "rep": 0, "bandwidth": -10}
    },
    {
        "id": "apt_3",
        "type": "BOSS PHASE 3",
        "icon": "☠️",
        "title": "Data Exfiltration",
        "image": "https://img.freepik.com/free-vector/data-extraction-concept-illustration_114360-4869.jpg",
        "text": "They are trying to upload 50GB of customer data to Dropbox.",
        "flavor": "Phase 3/3: The Finale",
        "choice_a": "Block IP Range",
        "choice_b": "Let it ride (Honeypot)",
        "impact_a": {"budget": 0, "risk": -20, "rep": +10, "bandwidth": 0},
        "impact_b": {"budget": 0, "risk": +50, "rep": +50, "bandwidth": 0} # High risk gamble
    }
]

# --- GAME ENGINE ---

def init_game():
    if 'stats' not in st.session_state:
        # HARDER STARTING STATS
        st.session_state.stats = {'budget': 40, 'rep': 50, 'risk': 20, 'bandwidth': 30}
    if 'week' not in st.session_state:
        st.session_state.week = 1
    if 'history' not in st.session_state:
        st.session_state.history = []
    
    # Deck Logic
    if 'deck' not in st.session_state:
        refill_deck()
    
    # Boss Logic
    if 'boss_mode' not in st.session_state:
        st.session_state.boss_mode = False
        st.session_state.boss_stage = 0
    
    # Initial Draw
    if 'current_card' not in st.session_state:
        draw_card()

def refill_deck():
    # Create a fresh shuffled list of standard event IDs
    st.session_state.deck = list(range(len(STANDARD_EVENTS)))
    random.shuffle(st.session_state.deck)

def draw_card():
    # 1. BOSS CHECK: Are we in a boss battle?
    if st.session_state.boss_mode:
        if st.session_state.boss_stage < len(BOSS_APT):
            st.session_state.current_card = BOSS_APT[st.session_state.boss_stage]
            return
        else:
            # Boss Defeated
            st.session_state.boss_mode = False
            st.session_state.boss_stage = 0
            st.toast("🏆 BOSS DEFEATED! Reputation +20")
            st.session_state.stats['rep'] += 20

    # 2. TRIGGER BOSS: 5% Chance to start Boss Battle (if not already in one)
    if not st.session_state.boss_mode and random.random() < 0.05 and st.session_state.week > 3:
        st.session_state.boss_mode = True
        st.session_state.boss_stage = 0
        st.session_state.current_card = BOSS_APT[0]
        st.toast("🚨 ALERT: APT GROUP DETECTED!")
        return

    # 3. RARE CARD: 5% Chance
    if random.random() < 0.05:
        st.session_state.current_card = random.choice(RARE_EVENTS)
        st.toast("✨ LEGENDARY EVENT!")
        return

    # 4. STANDARD DRAW
    if not st.session_state.deck:
        refill_deck()
    
    idx = st.session_state.deck.pop()
    st.session_state.current_card = STANDARD_EVENTS[idx]

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
