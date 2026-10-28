# 🧮 Math Challenge

> A friendly math practice app for kids, with Grade 5 topic practice and a daily mixed challenge.

![Platform](https://img.shields.io/badge/platform-Windows-blue?logo=windows)
![Python](https://img.shields.io/badge/python-3.10%2B-yellow?logo=python)
![License](https://img.shields.io/badge/license-MIT-green)

![Math Challenge](Math%20Challange%20-%20Quiz.png)

---

## ⬇️ Download (Windows — no install needed)

**Download the Windows executable from this repository:**

- Download [MathChallenge.exe](https://github.com/BangGor88/python-mathchallange/blob/main/math_challenge/dist/MathChallenge.exe)

On GitHub, click **Download raw file**, then double-click `MathChallenge.exe` to run it. No Python installation is required.

The app saves preferences and scores in `daily_tracker.json` next to the executable. This includes the selected color mode, last topic, daily challenge scores, and separate topic practice scores.

---

## ✨ Features

| Feature | Detail |
|---|---|
| 🎯 Topic chooser | Choose Fractions, Decimals, Multiplication by tens and hundreds, or the original daily mixed challenge |
| 🔄 Change topics anytime | Use **Change Topic** in the top bar; unfinished answers are cleared only after confirmation |
| 💾 Remember the last topic | Reopens the last selected topic on the next launch; use **Change Topic** to choose another |
| 🌙 Dark mode | Toggle between light and dark using the top-bar button; the preference is remembered |
| ✏️ Focused practice | Ten deterministic questions per topic session, with hints and answer feedback |
| ➗ Fraction answers | Enter fractions such as `3/4`; equivalent forms such as `2/4` are accepted |
| 📊 Separate topic history | Each focused topic keeps its own score history without replacing the daily challenge score |
| 📐 43 questions per day | 9 × Addition, Subtraction, Multiplication, Division · 6 Story problems · 1 Bonus |
| 🎲 Fresh questions daily | Seeded by today's date — same questions if you reopen the same day |
| 🟢 Easy start | First 3 questions in each operation are simpler to warm up |
| 🏆 Score out of 100 | Weighted sections (A: 60 pts · B: 20 pts · Bonus: 20 pts) |
| ⭐ Star rating | 0 – 5 stars based on your final score |
| 📊 Score history chart | Last 10 days shown on the results screen |
| 🌍 Language options | English (default), Swedish, German, and Indonesian |
| 🗣️ Story translation | Story questions and popups follow selected language |
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

Unit tests cover daily and topic question generation, fraction answer checking, scoring weights, and score persistence.

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
