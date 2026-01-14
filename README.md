# 🛡️ Incident Commander

**A Cybersecurity Governance & Risk Simulation**

## 🚨 Mission Brief
**Incident Commander** is a browser-based strategy simulation that puts players in the seat of a CISO (Chief Information Security Officer). 

In the real world, security is not just about hacking—it's about **Resource Management**, **Risk Acceptance**, and **Strategic Decision Making**. This tool gamifies those constraints.

[**👉 Click Here to Play the Live Demo**](#) *(Add your Streamlit link here after deploying)*

## 🎯 Learning Objectives
This project demonstrates the core "Soft Skills" of Cybersecurity:
- **Risk Assessment:** Evaluating threats (Phishing, Zero-Day, Supply Chain) against their potential impact.
- **Budget Governance:** Managing a finite security budget ($50k) effectively over a fiscal year.
- **Incident Response:** Making high-pressure decisions during active breach scenarios (e.g., Log4Shell events).

## 🛠️ Technical Architecture
- **Engine:** Python & Streamlit
- **State Management:** Uses `st.session_state` to track persistence across turns (Budget vs. Security Posture).
- **Logic:** Randomized event deck system with weighted outcomes based on player choices.

## 🚀 Installation

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/codyjkeller/incident-commander.git](https://github.com/codyjkeller/incident-commander.git)
   cd incident-commander
