# Math Challenge

Math Challenge is a Windows desktop quiz app built with Python and CustomTkinter for children to practice daily math.

## Features

- 43 questions per quiz (9 for each operation, 6 story questions, and 1 bonus)
- Daily deterministic question set based on date seed
- Score out of 100 with weighted sections
- Daily completion tracking in `daily_tracker.json`
- Animated score screen with stars, celebration, and a last-10-days score chart

## Requirements

- Python 3.10+
- Windows 10 or newer

## Setup

1. Open a terminal in the `math_challenge` folder.
2. Install dependencies:

```bash
python -m pip install -r requirements.txt
```

## Run

Use one of the following:

```bash
python main.py
```

Or double-click the Windows launcher:

- `run_app.bat`

## Build Single EXE (Windows)

A one-file executable builder with a fun kid-friendly icon is included.

1. Open PowerShell in the `math_challenge` folder.
2. Run:

```powershell
powershell -ExecutionPolicy Bypass -File .\package_exe.ps1
```

Build outputs:

- Executable: `dist/MathChallenge.exe`
- Generated icon: `build_assets/math_challenge_icon.ico`

## Test

Run all unit tests:

```bash
pytest tests/
```
