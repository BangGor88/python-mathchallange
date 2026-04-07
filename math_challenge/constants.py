"""Application constants for Math Challenge."""

from __future__ import annotations

from datetime import date

# UI configuration
APP_TITLE = "Math Challenge 🧮"
WINDOW_WIDTH = 1080
WINDOW_HEIGHT = 900

COLORS = {
    "background": "#EAF7EC",
    "panel": "#DDF1E1",
    "card": "#F4FBF6",
    "accent": "#2F8F4E",
    "accent_hover": "#287A42",
    "secondary": "#66B37A",
    "correct": "#27AE60",
    "wrong": "#E74C3C",
    "bonus": "#FFB300",
    "text": "#1E3A2B",
    "muted": "#557A66",
}

FONTS = {
    "title": ("Bahnschrift", 30, "bold"),
    "header": ("Bahnschrift", 20, "bold"),
    "question": ("Bahnschrift", 15, "bold"),
    "label": ("Bahnschrift", 13),
    "button": ("Bahnschrift", 16, "bold"),
    "score": ("Bahnschrift", 52, "bold"),
    "star": ("Bahnschrift", 30, "bold"),
}

SECTION_HEADINGS = {
    "addition": "➕ Addition",
    "subtraction": "➖ Subtraction",
    "multiplication": "✖️ Multiplication",
    "division": "➗ Division",
    "story": "📖 Story Questions",
    "bonus": "⭐ Bonus Question",
}

LANGUAGE_OPTIONS = {
    "English": "en",
    "Svenska": "sv",
    "Deutsch": "de",
    "Bahasa Indonesia": "id",
}

UI_TEXT = {
    "en": {
        "today_prefix": "Today:",
        "language": "Language",
        "submit_answers": "Submit Answers",
        "quiz_completed_title": "Quiz Completed",
        "quiz_completed_message": "You already finished today's quiz! Your score was {score}/100.\n\nWould you like to open the app anyway for extra practice?",
        "popup_open_anyway": "Open Anyway",
        "popup_exit": "Exit",
        "unanswered_title": "Unanswered Questions",
        "unanswered_message": "You have {count} unanswered questions. Submit anyway?",
        "popup_submit_anyway": "Submit Anyway",
        "popup_go_back": "Go Back",
        "minimum_score_title": "Minimum Score",
        "minimum_score_message": "You need at least {minimum} points to finish today. Would you like to redo now?",
        "popup_redo_now": "Redo Now",
        "popup_later": "Later",
        "your_score": "Your Score",
        "section_breakdown": "Section A: {a}/60   Section B: {b}/20   Bonus: {bonus}/20",
        "retry_button": "🔄 Try Again (same questions)",
        "new_questions_button": "🆕 New Questions",
        "retry_focus": "Retry Focus (no answers shown)",
        "no_answer": "No Answer",
        "wrong_answer": "Wrong Answer",
        "none": "None",
        "perfect_message": "Amazing! You got every question right.",
        "score_log": "Daily Score Log (Last {days} Days)",
        "no_scores": "No completed scores yet.",
        "section_addition": "➕ Addition",
        "section_subtraction": "➖ Subtraction",
        "section_multiplication": "✖️ Multiplication",
        "section_division": "➗ Division",
        "section_story": "📖 Story Questions",
        "section_bonus": "⭐ Bonus Question",
    },
    "sv": {
        "today_prefix": "Idag:",
        "language": "Sprak",
        "submit_answers": "Skicka svar",
        "quiz_completed_title": "Quiz klar",
        "quiz_completed_message": "Du har redan gjort dagens quiz! Din poang var {score}/100.\n\nVill du oppna appen anda for extra ovning?",
        "popup_open_anyway": "Oppna anda",
        "popup_exit": "Avsluta",
        "unanswered_title": "Obesvarade fragor",
        "unanswered_message": "Du har {count} obesvarade fragor. Skicka anda?",
        "popup_submit_anyway": "Skicka anda",
        "popup_go_back": "Ga tillbaka",
        "minimum_score_title": "Minimipoang",
        "minimum_score_message": "Du behover minst {minimum} poang for att klara dagen. Vill du gora om nu?",
        "popup_redo_now": "Gor om nu",
        "popup_later": "Senare",
        "your_score": "Din poang",
        "section_breakdown": "Del A: {a}/60   Del B: {b}/20   Bonus: {bonus}/20",
        "retry_button": "🔄 Forsok igen (samma fragor)",
        "new_questions_button": "🆕 Nya fragor",
        "retry_focus": "Ovningsfokus (inga svar visas)",
        "no_answer": "Inget svar",
        "wrong_answer": "Fel svar",
        "none": "Inga",
        "perfect_message": "Fantastiskt! Alla svar var ratt.",
        "score_log": "Daglig poanglogg (senaste {days} dagar)",
        "no_scores": "Inga sparade poang an.",
        "section_addition": "➕ Addition",
        "section_subtraction": "➖ Subtraktion",
        "section_multiplication": "✖️ Multiplikation",
        "section_division": "➗ Division",
        "section_story": "📖 Sagofragor",
        "section_bonus": "⭐ Bonusfraga",
    },
    "de": {
        "today_prefix": "Heute:",
        "language": "Sprache",
        "submit_answers": "Antworten senden",
        "quiz_completed_title": "Quiz beendet",
        "quiz_completed_message": "Du hast das heutige Quiz schon beendet! Deine Punktzahl war {score}/100.\n\nMochtest du die App trotzdem fur extra Ubung offnen?",
        "popup_open_anyway": "Trotzdem offnen",
        "popup_exit": "Beenden",
        "unanswered_title": "Unbeantwortete Fragen",
        "unanswered_message": "Du hast {count} unbeantwortete Fragen. Trotzdem senden?",
        "popup_submit_anyway": "Trotzdem senden",
        "popup_go_back": "Zuruck",
        "minimum_score_title": "Mindestpunktzahl",
        "minimum_score_message": "Du brauchst mindestens {minimum} Punkte, um den Tag abzuschliessen. Jetzt wiederholen?",
        "popup_redo_now": "Jetzt wiederholen",
        "popup_later": "Spater",
        "your_score": "Dein Ergebnis",
        "section_breakdown": "Teil A: {a}/60   Teil B: {b}/20   Bonus: {bonus}/20",
        "retry_button": "🔄 Erneut versuchen (gleiche Fragen)",
        "new_questions_button": "🆕 Neue Fragen",
        "retry_focus": "Wiederholungsfokus (keine Losungen)",
        "no_answer": "Keine Antwort",
        "wrong_answer": "Falsche Antwort",
        "none": "Keine",
        "perfect_message": "Super! Alle Antworten waren richtig.",
        "score_log": "Tagesverlauf (letzte {days} Tage)",
        "no_scores": "Noch keine gespeicherten Ergebnisse.",
        "section_addition": "➕ Addition",
        "section_subtraction": "➖ Subtraktion",
        "section_multiplication": "✖️ Multiplikation",
        "section_division": "➗ Division",
        "section_story": "📖 Sachaufgaben",
        "section_bonus": "⭐ Bonusfrage",
    },
    "id": {
        "today_prefix": "Hari ini:",
        "language": "Bahasa",
        "submit_answers": "Kirim Jawaban",
        "quiz_completed_title": "Kuis Selesai",
        "quiz_completed_message": "Kamu sudah menyelesaikan kuis hari ini! Skormu {score}/100.\n\nMau tetap buka aplikasi untuk latihan tambahan?",
        "popup_open_anyway": "Tetap Buka",
        "popup_exit": "Keluar",
        "unanswered_title": "Pertanyaan Belum Dijawab",
        "unanswered_message": "Ada {count} pertanyaan belum dijawab. Tetap kirim?",
        "popup_submit_anyway": "Tetap Kirim",
        "popup_go_back": "Kembali",
        "minimum_score_title": "Skor Minimum",
        "minimum_score_message": "Kamu butuh minimal {minimum} poin untuk menyelesaikan hari ini. Mau coba ulang sekarang?",
        "popup_redo_now": "Ulang Sekarang",
        "popup_later": "Nanti",
        "your_score": "Skormu",
        "section_breakdown": "Bagian A: {a}/60   Bagian B: {b}/20   Bonus: {bonus}/20",
        "retry_button": "🔄 Coba Lagi (soal yang sama)",
        "new_questions_button": "🆕 Soal Baru",
        "retry_focus": "Fokus Ulangi (tanpa jawaban)",
        "no_answer": "Belum Dijawab",
        "wrong_answer": "Jawaban Salah",
        "none": "Tidak ada",
        "perfect_message": "Keren! Semua jawaban benar.",
        "score_log": "Log Skor Harian (10 hari terakhir)",
        "no_scores": "Belum ada skor tersimpan.",
        "section_addition": "➕ Penjumlahan",
        "section_subtraction": "➖ Pengurangan",
        "section_multiplication": "✖️ Perkalian",
        "section_division": "➗ Pembagian",
        "section_story": "📖 Soal Cerita",
        "section_bonus": "⭐ Soal Bonus",
    },
}

POINTS_PER_SECTION = {
    "addition": 60 / 36,
    "subtraction": 60 / 36,
    "multiplication": 60 / 36,
    "division": 60 / 36,
    "story": 20 / 6,
    "bonus": 20,
}

QUESTION_COUNTS = {
    "operation_each": 9,
    "story": 6,
    "bonus": 1,
}

TRACKER_FILENAME = "daily_tracker.json"
MINIMUM_PASS_SCORE = 40
SCORE_LOG_DAYS = 10


def default_daily_seed() -> int:
    """Return deterministic seed in YYYYMMDD format for current day."""
    return int(date.today().strftime("%Y%m%d"))


STORY_TEMPLATES = [
    {
        "id": "story_1",
        "text": "Emma has {a} apples. She gives {b} to her friend. How many does she have left?",
        "generator": lambda rng: {
            "a": rng.randint(15, 60),
            "b": rng.randint(1, 14),
        },
        "answer": lambda values: values["a"] - values["b"],
    },
    {
        "id": "story_2",
        "text": "A box holds {a} chocolates. There are {b} boxes. How many chocolates in total?",
        "generator": lambda rng: {
            "a": rng.randint(6, 18),
            "b": rng.randint(2, 12),
        },
        "answer": lambda values: values["a"] * values["b"],
    },
    {
        "id": "story_3",
        "text": "A class of {a} students is split into groups of {b}. How many groups?",
        "generator": lambda rng: {
            "b": rng.randint(2, 10),
            "q": rng.randint(2, 8),
        },
        "answer": lambda values: values["a"] // values["b"],
        "post_process": lambda values: {**values, "a": values["b"] * values["q"]},
    },
    {
        "id": "story_4",
        "text": "Tom saves £{a} each week. How much does he save in {b} weeks?",
        "generator": lambda rng: {
            "a": rng.randint(3, 25),
            "b": rng.randint(2, 12),
        },
        "answer": lambda values: values["a"] * values["b"],
    },
    {
        "id": "story_5",
        "text": "There are {a} pages in a book. Maya reads {b} pages per day. How many days to finish?",
        "generator": lambda rng: {
            "b": rng.randint(5, 20),
            "q": rng.randint(3, 15),
        },
        "answer": lambda values: values["a"] // values["b"],
        "post_process": lambda values: {**values, "a": values["b"] * values["q"]},
    },
    {
        "id": "story_6",
        "text": "Lena has {a} stickers and buys {b} more packs with {c} stickers each. How many stickers now?",
        "generator": lambda rng: {
            "a": rng.randint(10, 40),
            "b": rng.randint(2, 6),
            "c": rng.randint(3, 10),
        },
        "answer": lambda values: values["a"] + values["b"] * values["c"],
    },
    {
        "id": "story_7",
        "text": "A farmer picks {a} eggs each day for {b} days. He sells {c} eggs. How many eggs remain?",
        "generator": lambda rng: {
            "a": rng.randint(8, 20),
            "b": rng.randint(2, 7),
            "c": rng.randint(10, 60),
        },
        "answer": lambda values: values["a"] * values["b"] - values["c"],
    },
    {
        "id": "story_8",
        "text": "A toy shop has {a} shelves with {b} toys on each shelf. {c} toys are sold. How many toys are left?",
        "generator": lambda rng: {
            "a": rng.randint(3, 8),
            "b": rng.randint(6, 15),
            "c": rng.randint(5, 40),
        },
        "answer": lambda values: values["a"] * values["b"] - values["c"],
    },
    {
        "id": "story_9",
        "text": "A coach has {a} players and splits them into {b} equal teams. How many players per team?",
        "generator": lambda rng: {
            "b": rng.randint(2, 6),
            "q": rng.randint(3, 10),
        },
        "answer": lambda values: values["a"] // values["b"],
        "post_process": lambda values: {**values, "a": values["b"] * values["q"]},
    },
    {
        "id": "story_10",
        "text": "Nina reads {a} chapters each week for {b} weeks, then rereads {c} chapters. How many chapters read in total?",
        "generator": lambda rng: {
            "a": rng.randint(1, 5),
            "b": rng.randint(3, 10),
            "c": rng.randint(1, 8),
        },
        "answer": lambda values: values["a"] * values["b"] + values["c"],
    },
]

STORY_TEMPLATE_TRANSLATIONS = {
    "sv": {
        "story_1": "Emma har {a} applen. Hon ger {b} till sin van. Hur manga har hon kvar?",
        "story_2": "En lada rymmer {a} chokladbitar. Det finns {b} lador. Hur manga chokladbitar totalt?",
        "story_3": "En klass med {a} elever delas in i grupper om {b}. Hur manga grupper blir det?",
        "story_4": "Tom sparar {a} kronor varje vecka. Hur mycket sparar han pa {b} veckor?",
        "story_5": "Det finns {a} sidor i en bok. Maya laser {b} sidor per dag. Hur manga dagar tar det?",
        "story_6": "Lena har {a} klistermarken och koper {b} paket till med {c} klistermarken i varje. Hur manga har hon nu?",
        "story_7": "En bonde samlar {a} agg varje dag i {b} dagar. Han saljer {c} agg. Hur manga agg ar kvar?",
        "story_8": "En leksaksbutik har {a} hyllor med {b} leksaker pa varje hylla. {c} leksaker saljs. Hur manga ar kvar?",
        "story_9": "En tranare har {a} spelare och delar dem i {b} lika lag. Hur manga spelare per lag?",
        "story_10": "Nina laser {a} kapitel varje vecka i {b} veckor och laser om {c} kapitel. Hur manga kapitel totalt?",
    },
    "de": {
        "story_1": "Emma hat {a} Apfel. Sie gibt {b} ihrem Freund. Wie viele hat sie noch?",
        "story_2": "Eine Schachtel enthalt {a} Pralinen. Es gibt {b} Schachteln. Wie viele Pralinen insgesamt?",
        "story_3": "Eine Klasse mit {a} Schuelern wird in Gruppen zu {b} geteilt. Wie viele Gruppen entstehen?",
        "story_4": "Tom spart jede Woche {a} Euro. Wie viel spart er in {b} Wochen?",
        "story_5": "Ein Buch hat {a} Seiten. Maya liest {b} Seiten pro Tag. Wie viele Tage braucht sie?",
        "story_6": "Lena hat {a} Sticker und kauft {b} weitere Packungen mit je {c} Stickern. Wie viele hat sie jetzt?",
        "story_7": "Ein Bauer sammelt {a} Eier pro Tag fuer {b} Tage. Er verkauft {c} Eier. Wie viele bleiben?",
        "story_8": "Ein Spielzeugladen hat {a} Regale mit je {b} Spielzeugen. {c} Spielzeuge werden verkauft. Wie viele bleiben?",
        "story_9": "Ein Trainer hat {a} Spieler und teilt sie in {b} gleich grosse Teams. Wie viele Spieler pro Team?",
        "story_10": "Nina liest {a} Kapitel pro Woche fuer {b} Wochen und liest danach {c} Kapitel erneut. Wie viele Kapitel insgesamt?",
    },
    "id": {
        "story_1": "Emma punya {a} apel. Dia memberi {b} ke temannya. Berapa apel yang tersisa?",
        "story_2": "Satu kotak berisi {a} cokelat. Ada {b} kotak. Berapa jumlah cokelat semuanya?",
        "story_3": "Satu kelas berisi {a} siswa dibagi menjadi kelompok berisi {b}. Ada berapa kelompok?",
        "story_4": "Tom menabung {a} rupiah setiap minggu. Berapa tabungannya dalam {b} minggu?",
        "story_5": "Ada {a} halaman dalam sebuah buku. Maya membaca {b} halaman per hari. Berapa hari sampai selesai?",
        "story_6": "Lena punya {a} stiker dan membeli {b} paket lagi, tiap paket berisi {c} stiker. Sekarang ada berapa stiker?",
        "story_7": "Seorang petani mengumpulkan {a} telur per hari selama {b} hari. Dia menjual {c} telur. Berapa telur yang tersisa?",
        "story_8": "Sebuah toko mainan punya {a} rak dengan {b} mainan di tiap rak. {c} mainan terjual. Berapa yang tersisa?",
        "story_9": "Seorang pelatih punya {a} pemain dan membaginya menjadi {b} tim yang sama besar. Berapa pemain per tim?",
        "story_10": "Nina membaca {a} bab per minggu selama {b} minggu, lalu membaca ulang {c} bab. Berapa total bab yang dibaca?",
    },
}

BONUS_TEMPLATES = [
    {
        "id": "bonus_1",
        "text": "A baker makes {a} loaves per day. Each loaf has {b} slices. If {c} slices are eaten, how many slices remain?",
        "generator": lambda rng: {
            "a": rng.randint(4, 12),
            "b": rng.randint(4, 10),
            "c": rng.randint(5, 25),
        },
        "answer": lambda values: values["a"] * values["b"] - values["c"],
    },
    {
        "id": "bonus_2",
        "text": "A school buys {a} packs of pencils with {b} pencils in each pack, then gives away {c} pencils. How many pencils are left?",
        "generator": lambda rng: {
            "a": rng.randint(3, 9),
            "b": rng.randint(6, 15),
            "c": rng.randint(10, 40),
        },
        "answer": lambda values: values["a"] * values["b"] - values["c"],
    },
    {
        "id": "bonus_3",
        "text": "A bus carries {a} children on each trip and makes {b} trips. If {c} children have already gone home, how many are still at school?",
        "generator": lambda rng: {
            "a": rng.randint(8, 20),
            "b": rng.randint(2, 5),
            "c": rng.randint(10, 50),
        },
        "answer": lambda values: values["a"] * values["b"] - values["c"],
    },
    {
        "id": "bonus_4",
        "text": "There are {a} teams with {b} players each. They share into groups of {c}. How many groups are made?",
        "generator": lambda rng: {
            "a": rng.randint(3, 8),
            "b": rng.randint(4, 9),
            "c": rng.randint(2, 6),
        },
        "answer": lambda values: (values["a"] * values["b"]) // values["c"],
        "post_process": lambda values: {
            **values,
            "b": values["b"] * values["c"],
        },
    },
]

BONUS_TEMPLATE_TRANSLATIONS = {
    "sv": {
        "bonus_1": "En bagare bakar {a} brod per dag. Varje brod har {b} skivor. Om {c} skivor ats upp, hur manga skivor ar kvar?",
        "bonus_2": "En skola koper {a} paket pennor med {b} pennor i varje paket och delar sedan ut {c} pennor. Hur manga pennor ar kvar?",
        "bonus_3": "En buss tar {a} barn per tur och gor {b} turer. Om {c} barn redan har gatt hem, hur manga ar fortfarande i skolan?",
        "bonus_4": "Det finns {a} lag med {b} spelare vardera. De delas in i grupper om {c}. Hur manga grupper bildas?",
    },
    "de": {
        "bonus_1": "Ein Backer backt {a} Brotlaibe pro Tag. Jeder Laib hat {b} Scheiben. Wenn {c} Scheiben gegessen werden, wie viele bleiben ubrig?",
        "bonus_2": "Eine Schule kauft {a} Packungen Bleistifte mit je {b} Bleistiften und gibt {c} Bleistifte weg. Wie viele Bleistifte bleiben ubrig?",
        "bonus_3": "Ein Bus befordert {a} Kinder pro Fahrt und macht {b} Fahrten. Wenn {c} Kinder schon nach Hause gegangen sind, wie viele sind noch in der Schule?",
        "bonus_4": "Es gibt {a} Teams mit je {b} Spielern. Sie werden in Gruppen zu je {c} aufgeteilt. Wie viele Gruppen entstehen?",
    },
    "id": {
        "bonus_1": "Seorang pembuat roti membuat {a} roti per hari. Setiap roti memiliki {b} irisan. Jika {c} irisan dimakan, berapa irisan yang tersisa?",
        "bonus_2": "Sebuah sekolah membeli {a} pak pensil dengan {b} pensil di setiap pak, lalu membagikan {c} pensil. Berapa pensil yang tersisa?",
        "bonus_3": "Sebuah bus membawa {a} anak per perjalanan dan membuat {b} perjalanan. Jika {c} anak sudah pulang, berapa anak yang masih di sekolah?",
        "bonus_4": "Ada {a} tim dengan {b} pemain masing-masing. Mereka dibagi menjadi kelompok berisi {c}. Berapa kelompok yang terbentuk?",
    },
}
