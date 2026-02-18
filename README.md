# Incident Commander: CISO Edition

> "Heavy is the head that wears the headset."

**Incident Commander** is a browser-based strategy simulation that puts you in the seat of a CISO (Chief Information Security Officer). Inspired by games like *Reigns*, you must balance four volatile metrics to survive the fiscal year.

## How to Play
You are presented with a series of binary choices (cards). Swiping Left or Right will impact your resources. If any resource hits **0** or **100** (for Risk), you are fired.

### The 4 Metrics
* **Budget:** Run out, and the board dissolves your department.
* **Reputation:** Lose trust, and you are fired.
* **Risk:** Hit 100%, and you suffer a catastrophic breach.
* **Bandwidth:** Run out, and your team quits from burnout.

## Tech Stack
* **Engine:** Python (Streamlit)
* **State Management:** Session State for persistence.
* **Data:** JSON-based scenario loader.
* **CI/CD:** GitHub Actions for automated linting.

## Installation & Usage

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/codyjkeller/incident-commander.git](https://github.com/codyjkeller/incident-commander.git)
   cd incident-commander
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   streamlit run game.py
   ```

## License
This project is licensed under the MIT License - see the LICENSE file for details.
