You are a senior Python developer. Build a complete Windows 10 desktop 
app called "Math Challenge" for an 11-year-old child using Python 3 
and CustomTkinter (pip install customtkinter). Follow every instruction 
below precisely. Deploy in numbered steps and run tests after each step 
before continuing.

════════════════════════════════════════════
OVERVIEW
════════════════════════════════════════════
A daily math quiz app. Every calendar day the child gets a fresh set of 
randomised questions (seeded with today's date so they stay consistent 
if the app is reopened the same day). The child types answers directly 
into the app, presses Submit, and gets a score out of 100 with a 
celebration animation.

════════════════════════════════════════════
QUESTION STRUCTURE  (total: 46 questions)
════════════════════════════════════════════
Section A – Pure operations (40 questions, 10 per operation)
  • 10 × Addition        (numbers 1–100, single answers, whole numbers)
  • 10 × Subtraction     (larger minus smaller so answer ≥ 0, whole numbers)
  • 10 × Multiplication  (numbers 2–12 × numbers 1–20, whole numbers)
  • 10 × Division        (generate quotient first, then multiply to get 
                          dividend — always exact, no remainders)

Section B – Story problems (5 questions)
  Use a pool of at least 10 story question templates. Pick 5 at random 
  each day. Each template uses placeholder numbers filled in randomly:
  Example templates:
    "Emma has {a} apples. She gives {b} to her friend. How many does she 
     have left?"
    "A box holds {a} chocolates. There are {b} boxes. How many chocolates 
     in total?"
    "A class of {a} students is split into groups of {b}. How many groups?"
    "Tom saves £{a} each week. How much does he save in {b} weeks?"
    "There are {a} pages in a book. Maya reads {b} pages per day. How 
     many days to finish?"
  (Provide all 10 templates in the code.)

Section C – Bonus question (1 question, worth extra points — see scoring)
  A two-step word problem combining two operations. Example:
    "A baker makes {a} loaves of bread per day. Each loaf is cut into 
     {b} slices. If {c} slices are eaten, how many slices remain?"
  Use at least 4 bonus templates and pick one at random per day.

════════════════════════════════════════════
RANDOMISATION RULES
════════════════════════════════════════════
- Use Python random module seeded with: int(date.today().strftime("%Y%m%d"))
- Seed once at the start of question generation so all questions for the 
  day are deterministic.
- Division: always create exact-division questions (quotient × divisor = 
  dividend). Divisors: 2–10, quotients: 2–12.

════════════════════════════════════════════
SCORING (total: 100 points)
════════════════════════════════════════════
- Section A: 40 questions × 1.5 points each = 60 points
- Section B:  5 questions × 4 points each  = 20 points
- Section C:  1 bonus question              = 20 points
- Total: 100 points maximum
- Accept minor whitespace differences; strip and compare as integers or 
  floats where relevant.
- If the answer field is blank, count as 0.

════════════════════════════════════════════
DAILY TRACKING
════════════════════════════════════════════
- Store progress in a JSON file: daily_tracker.json in the app folder.
- Format: { "YYYY-MM-DD": { "score": 87, "completed": true } }
- On app launch, check today's date in the JSON.
  – If completed today: show a friendly popup "You already finished 
    today's quiz! Your score was {score}/100. Come back tomorrow!" 
    with an OK button. App then exits gracefully.
  – If NOT completed: launch the quiz normally.
- After a successful submission, write today's record to the JSON.

════════════════════════════════════════════
UI / UX REQUIREMENTS
════════════════════════════════════════════
General:
- Window title: "Math Challenge 🧮"
- Window size: 750 × 900, resizable, centred on screen
- Font: large, child-friendly (size 15–18 for questions, 13 for labels)
- Colour scheme: bright and cheerful. Use these CustomTkinter colours:
    Background: "#F0F4FF"    (light blue-white)
    Accent:     "#5B6EF5"    (purple-blue)
    Correct:    "#27AE60"    (green)
    Wrong:      "#E74C3C"    (red)
    Bonus:      "#F39C12"    (gold)

Layout:
- Header bar with title "Math Challenge 🧮" and today's date
- Scrollable frame containing all 46 questions grouped by section with 
  clear headings:
    "➕ Addition"  "➖ Subtraction"  "✖️ Multiplication"  "➗ Division"
    "📖 Story Questions"  "⭐ Bonus Question"
- Each question: bold question text on one line, answer Entry field 
  directly below it (or beside it for shorter questions)
- At the bottom (outside scroll): a large "Submit Answers" button 
  (accent colour, width 300px)

════════════════════════════════════════════
SUBMISSION & SCORE SCREEN
════════════════════════════════════════════
When the child clicks "Submit Answers":
1. Validate all fields. If any are empty, show a popup:
   "You have {n} unanswered questions. Submit anyway?" → Yes / Go Back
2. Check every answer and colour-code each Entry field:
   • Correct → green background
   • Wrong   → red background, show correct answer as small grey text 
     below the field
3. Clear the quiz area and show a full SCORE SCREEN in the same window:
   • Large animated score counter that counts up from 0 to the final 
     score (e.g. 0 → 87) over 1.5 seconds
   • Star rating (0–5 stars) based on score thresholds:
       < 40 → 0 stars,  40–59 → 2 stars,  60–74 → 3 stars,
       75–89 → 4 stars,  90–100 → 5 stars
   • Section breakdown: A: X/60  B: X/20  Bonus: X/20
   • Celebration animation (see below)
   • Two buttons: "🔄 Try Again (same questions)" and "🆕 New Questions"
     – Try Again: reloads the exact same questions (same seed) with 
       blank fields. Does NOT overwrite the JSON record.
     – New Questions: generates a new random seed (use a different seed 
       offset, e.g. date + 1) and loads fresh questions. Does NOT 
       overwrite the JSON record.

Celebration animation (use Tkinter Canvas):
- On score >= 60: spawn 60 coloured confetti rectangles that fall from 
  the top of the score area, rotating and fading over 3 seconds.
- On score >= 90: additionally display a large "🌟 AMAZING! 🌟" message 
  that pulses (scales up and down) for 2 seconds.
- On score < 40: show an encouraging "Keep practising! You'll get it 🤓" 
  message in orange, no confetti.

════════════════════════════════════════════
FILE STRUCTURE
════════════════════════════════════════════
math_challenge/
├── main.py              ← entry point
├── app.py               ← main App class (CustomTkinter window)
├── questions.py         ← question generation logic
├── scorer.py            ← scoring and answer checking logic
├── tracker.py           ← daily JSON read/write logic
├── animations.py        ← confetti and celebration animations
├── constants.py         ← colours, fonts, story templates, config
├── tests/
│   ├── test_questions.py
│   ├── test_scorer.py
│   └── test_tracker.py
├── daily_tracker.json   ← auto-created on first run
└── requirements.txt     ← customtkinter, pytest

════════════════════════════════════════════
DEPLOYMENT STEPS — follow in strict order
════════════════════════════════════════════

STEP 1 — Environment & scaffolding
  a) List all files to create with one-line descriptions.
  b) Create requirements.txt and constants.py.
  c) Verify Python 3.10+ compatibility.
  TEST: Confirm requirements.txt is valid and constants.py imports 
  without error.

STEP 2 — Question generation (questions.py)
  a) Implement all four operation generators.
  b) Implement all 10 story templates.
  c) Implement all 4 bonus templates.
  d) Expose a single generate_questions(seed) function that returns a 
     list of dicts: {id, section, question_text, correct_answer}
  TEST: Run test_questions.py:
    - Check generate_questions returns exactly 46 items.
    - Check division questions always have integer answers.
    - Check same seed → same questions; different seed → different.
    - Check all correct_answers are numeric.

STEP 3 — Scoring logic (scorer.py)
  a) Implement check_answers(questions, user_answers) → returns 
     {question_id: bool} dict.
  b) Implement calculate_score(results) → int 0–100.
  c) Implement get_star_rating(score) → int 0–5.
  TEST: Run test_scorer.py:
    - Perfect answers → 100.
    - Zero answers    →   0.
    - Spot-check section weightings.
    - Blank/whitespace answers handled as wrong.

STEP 4 — Daily tracker (tracker.py)
  a) Implement load_tracker(), save_today(score), has_completed_today().
  b) Use pathlib for file paths relative to the script location.
  TEST: Run test_tracker.py:
    - New file created if absent.
    - has_completed_today() returns False on empty file.
    - After save_today(85), has_completed_today() returns True 
      and score is 85.
    - Multiple days stored independently.

STEP 5 — Basic UI skeleton (app.py + main.py)
  a) Build the full window layout: header, scrollable question area 
     (placeholder labels), Submit button.
  b) Apply all colours from constants.py.
  c) Window centres on screen on launch.
  d) Integrate tracker: show reminder popup if already completed today,
     then exit.
  TEST (manual): Run main.py. Confirm window appears, is centred, 
  scrolls, and button is visible. Temporarily set today as completed 
  and confirm popup shows and app exits.

STEP 6 — Render questions in UI
  a) Call generate_questions() and render all 46 questions with Entry 
     fields in the scrollable frame.
  b) Group by section with styled headings.
  c) Tab order follows question order (top to bottom).
  TEST (manual): All 46 questions visible. Tab moves between fields. 
  Headings are clearly distinguishable.

STEP 7 — Submission & answer checking
  a) Wire "Submit Answers" button to collect all Entry values.
  b) Check for blank answers; show confirmation popup if any blank.
  c) Colour-code correct (green) and wrong (red) Entry fields.
  d) Show correct answer below wrong fields.
  e) Write result to daily_tracker.json.
  TEST (manual): Submit all correct answers → all green, score = 100. 
  Submit all wrong → all red with correct answers shown.

STEP 8 — Score screen
  a) Replace quiz area with score screen.
  b) Implement animated score counter (Tkinter after() loop).
  c) Show star rating, section breakdown, and both action buttons.
  d) Wire "Try Again" and "New Questions" buttons.
  TEST (manual): Score counts up smoothly. Stars display correctly for 
  scores 30, 65, 80, 95. Both buttons reload the correct questions.

STEP 9 — Celebration animations (animations.py)
  a) Implement confetti for score ≥ 60.
  b) Implement pulsing "AMAZING" message for score ≥ 90.
  c) Implement encouragement message for score < 40.
  TEST (manual): Force score to 95, 70, 30 and confirm each animation 
  triggers correctly. Confirm animation completes without freezing the UI.

STEP 10 — Final polish & packaging
  a) Add a README.md with setup instructions (pip install, how to run).
  b) Add a simple launcher script: run_app.bat for Windows.
  c) Confirm all unit tests pass: pytest tests/
  d) Do a full end-to-end walkthrough: launch → quiz → submit → score 
     screen → Try Again → submit → New Questions → submit.
  FINAL TEST: pytest tests/ must show 0 failures. Manual walkthrough 
  must complete without errors.

════════════════════════════════════════════
CONSTRAINTS & QUALITY RULES
════════════════════════════════════════════
- No external dependencies beyond customtkinter and pytest.
- All Tkinter UI updates must happen on the main thread.
- Animations must use Tkinter's after() — never time.sleep() in the UI.
- Handle FileNotFoundError and JSONDecodeError gracefully in tracker.py.
- Code must pass basic PEP 8 formatting.
- Comments in English, child-appropriate strings in the UI.
- Do not proceed to the next step until all tests for the current step 
  pass.

Begin with Step 1. List the files you will create, then start coding.