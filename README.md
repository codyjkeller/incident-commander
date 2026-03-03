# Incident Commander: CISO Edition

> "Heavy is the head that wears the headset."

**Incident Commander** is a browser-based strategy card game that puts you in the seat of a CISO (Chief Information Security Officer). Inspired by *Reigns*, you must balance four volatile metrics across 52 weeks to survive the fiscal year.

## Play Now

**[Play Incident Commander](https://codyjkeller.github.io/incident-commander/)**

No install required. Works on desktop and mobile browsers.

## How to Play

You are presented with a series of scenario cards — ransomware attacks, surprise audits, vendor demands, insider threats. Each card offers two choices. Every choice shifts your resources. If any metric hits zero (or 100 for Risk), you're fired.

**Controls:**
- **Mobile:** Swipe left or right on the card
- **Desktop:** Click the choice buttons, or use Arrow Keys / A and D
- **Logs:** Tap the hamburger icon in the top bar to review past decisions

### The 4 Metrics

- **Budget** — Run out, and the board dissolves your department.
- **Trust** — Lose the board's confidence, and you're terminated.
- **Risk** — Hit 100%, and you suffer a catastrophic breach.
- **Team** — Run out of bandwidth, and your entire team quits.

### Card Types

- **Standard** — Day-to-day incidents, vendor requests, strategy decisions, personnel issues, and audits.
- **Legendary** — Rare high-impact events that can dramatically shift the game in your favor.
- **Boss (3-Phase)** — A multi-stage APT attack. Survive all three phases to earn a Trust bonus.

## Tech Stack

- **Single file:** One `index.html` — HTML, CSS, and JavaScript. No frameworks, no build step, no server.
- **Zero dependencies:** No external libraries, no CDN calls, no images to break.
- **Mobile-first:** Touch swipe gestures, responsive layout, add-to-home-screen capable.
- **Hosted on GitHub Pages.**

## Run Locally

```bash
git clone https://github.com/codyjkeller/incident-commander.git
cd incident-commander
open index.html
```

Or just double-click the file.

## License

MIT License — see [LICENSE](LICENSE) for details.
