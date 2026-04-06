# 🧮 Math Challenge

> A daily math quiz desktop app for kids — fun, fast, and gets a little trickier as you go!

![Platform](https://img.shields.io/badge/platform-Windows-blue?logo=windows)
![Python](https://img.shields.io/badge/python-3.10%2B-yellow?logo=python)
![License](https://img.shields.io/badge/license-MIT-green)

---

## ⬇️ Download (Windows — no install needed)

**Download the Windows executable from GitHub Releases:**

- Direct download (latest release):
	[Download EXE](https://github.com/BangGor88/python-mathchallange/releases/latest/download/MathChallenge.exe)
- Releases page (if direct link is not available yet):
	[Latest Release](https://github.com/BangGor88/python-mathchallange/releases/latest)

1. Open one of the links above.
2. Download **MathChallenge.exe**.
3. Double-click it to run (no Python install required).

If you do not see `MathChallenge.exe` yet, it means the asset has not been uploaded to the latest release.

> The app saves your daily score log in a `daily_tracker.json` file next to the executable.

---

## ✨ Features

| Feature | Detail |
|---|---|
| 📐 43 questions per day | 9 × Addition, Subtraction, Multiplication, Division · 6 Story problems · 1 Bonus |
| 🎲 Fresh questions daily | Seeded by today's date — same questions if you reopen the same day |
| 🟢 Easy start | First 3 questions in each operation are simpler to warm up |
| 🏆 Score out of 100 | Weighted sections (A: 60 pts · B: 20 pts · Bonus: 20 pts) |
| ⭐ Star rating | 0 – 5 stars based on your final score |
| 📊 Score history chart | Last 10 days shown on the results screen |
| 🎉 Celebration animations | Confetti, pulsing AMAZING message, and encouragement |
| 🔄 Try Again / New Questions | Replay the same set or generate a fresh one |
| ✅ Minimum passing score | Must reach **40 points** to mark the day as complete |
| 📅 Daily completion tracking | Already done today? The app asks if you want extra practice |

---

## 🖥️ Screenshots

> *(Add screenshots here after first run)*

---

## 🚀 Running from Source

**Requirements:** Python 3.10+, Windows 10 or newer.

```bash
# 1 — Clone the repo
git clone https://github.com/BangGor88/python-mathchallange.git
cd python-mathchallange/math_challenge

# 2 — Create a virtual environment (recommended)
python -m venv ../.venv
../.venv/Scripts/activate

# 3 — Install dependencies
pip install -r requirements.txt

# 4 — Run
python main.py
```

Or just double-click **`run_app.bat`** after installing dependencies.

---

## 🔨 Build the EXE Yourself

A fully automated PowerShell build script generates a kid-friendly icon and packages everything into one file.

```powershell
# Inside the math_challenge folder
powershell -ExecutionPolicy Bypass -File .\package_exe.ps1
```

Output: **`dist/MathChallenge.exe`**

---

## 🧪 Tests

```bash
pytest tests/
```

All 13 unit tests cover question generation, scoring weights, and daily tracker persistence.

---

## 📁 Project Structure

```
math_challenge/
├── main.py              ← Entry point
├── app.py               ← Main CustomTkinter window and all UI
├── questions.py         ← Deterministic question generation
├── scorer.py            ← Answer checking and weighted scoring
├── tracker.py           ← Daily JSON read/write tracking
├── animations.py        ← Confetti and celebration effects
├── constants.py         ← Colours, fonts, templates, config
├── tests/               ← Pytest unit tests
├── package_exe.ps1      ← Auto-build script (icon + PyInstaller)
├── run_app.bat          ← Quick launcher for Windows
└── requirements.txt     ← customtkinter · pytest
```

---

## 📜 License

MIT — free to use, share, and modify.

