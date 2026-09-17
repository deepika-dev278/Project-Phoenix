
import streamlit as st
import sqlite3
from datetime import date, datetime

# =========================
# PHOENIX SETUP
# =========================
st.set_page_config(
    page_title="Phoenix | Learn Your Way",
    page_icon="🔥",
    layout="wide"
)

DB = "phoenix.db"

# =========================
# DATABASE
# =========================


def db():
    return sqlite3.connect(DB, check_same_thread=False)


def setup():
    with db() as con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS profile (
                id INTEGER PRIMARY KEY,
                name TEXT, age TEXT, education TEXT,
                institution TEXT, goal TEXT, target_date TEXT,
                subjects TEXT, weak_topics TEXT,
                study_minutes INTEGER, learning_style TEXT,
                study_time TEXT
            )
        """)
        con.execute("""
            CREATE TABLE IF NOT EXISTS stats (
                id INTEGER PRIMARY KEY,
                xp INTEGER DEFAULT 0,
                streak INTEGER DEFAULT 1
            )
        """)
        con.execute("""
            CREATE TABLE IF NOT EXISTS goals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT, minutes INTEGER,
                completed INTEGER DEFAULT 0
            )
        """)
        con.execute("""
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT, event_date TEXT
            )
        """)
        con.execute("""
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                rating TEXT, comment TEXT
            )
        """)
        con.execute("""
            INSERT OR IGNORE INTO stats (id, xp, streak)
            VALUES (1, 0, 1)
        """)


setup()


def get_profile():
    with db() as con:
        return con.execute(
            "SELECT * FROM profile WHERE id=1"
        ).fetchone()


def get_stats():
    with db() as con:
        return con.execute(
            "SELECT xp, streak FROM stats WHERE id=1"
        ).fetchone()


def earn_xp(points):
    with db() as con:
        con.execute(
            "UPDATE stats SET xp=xp+? WHERE id=1",
            (points,)
        )


# =========================
# DESIGN
# =========================
st.markdown("""
<style>
/* ===== PHOENIX: DARK-ONLY THEME ===== */

.stApp {
    background:
        radial-gradient(ellipse at top right, #32120f 0%, transparent 42%),
        linear-gradient(135deg, #090909, #160d0c 60%, #210d09);
    color: #f5e9e5;
    font-family: "Segoe UI", Arial, sans-serif;
}

h1, h2, h3 {
    color: #ff7547 !important;
    font-weight: 800 !important;
}

p, label, li {
    color: #f0e4df;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0c0909, #260d0b);
    border-right: 1px solid #542018;
}

section[data-testid="stSidebar"] * {
    color: #f5e9e5;
}

/* Dashboard metric cards */
[data-testid="stMetric"] {
    background: linear-gradient(145deg, #211513, #151010);
    border: 1px solid #54251c;
    border-radius: 16px;
    padding: 18px;
}

[data-testid="stMetricValue"] {
    color: #ff7547 !important;
    font-weight: 850;
}

/* Forms and task cards */
div[data-testid="stForm"],
div[data-testid="stCheckbox"] {
    background: #1b1312;
    border: 1px solid #4a241c;
    border-radius: 13px;
    padding: 12px;
}

/* Input fields */
.stTextInput input,
.stTextArea textarea {
    background: #211817 !important;
    color: #ffffff !important;
    border: 1px solid #603126 !important;
}

/* Dropdowns */
div[data-baseweb="select"] > div {
    background: #211817;
    color: white;
    border-color: #603126;
}

/* Buttons */
.stButton button,
.stFormSubmitButton button {
    background: linear-gradient(110deg, #b91c1c, #e85d24);
    color: white !important;
    border: 1px solid #f07843;
    border-radius: 11px;
    font-weight: 750;
}

.stButton button:hover,
.stFormSubmitButton button:hover {
    background: linear-gradient(110deg, #dc2626, #fb923c);
    color: white !important;
}

/* Progress bar */
div[data-testid="stProgress"] > div > div {
    background: linear-gradient(90deg, #dc2626, #fb923c);
}

/* Checkbox labels */
div[data-testid="stCheckbox"] label p {
    color: #fff0e8 !important;
    font-weight: 600 !important;
}

/* Captions and separators */
.stCaption, small {
    color: #cbb8b0 !important;
}

hr {
    border-color: #54251c !important;
}
}</style>
""", unsafe_allow_html=True)

# =========================
# SIDEBAR
# =========================
st.sidebar.title("🔥 PHOENIX")
st.sidebar.caption("Your personal learning coach")

page = st.sidebar.radio(
    "YOUR SPACE",
    [
        "🏠 Dashboard",
        "👤 My Profile",
        "🧠 Skill Check",
        "🗺️ Learning Roadmap",
        "📅 Study Planner",
        "💬 Feedback"
    ]
)

st.sidebar.divider()
st.sidebar.markdown("### 💎 Free Plan")
st.sidebar.caption("Learn • Practise • Earn XP")

# =========================
# DASHBOARD
# =========================
if page == "🏠 Dashboard":
    st.title("Welcome to Phoenix 🔥")
    st.write("Small steps. Personalised learning. Real progress.")

    xp, streak = get_stats()

    with db() as con:
        completed = con.execute(
            "SELECT COUNT(*) FROM goals WHERE completed=1"
        ).fetchone()[0]

    c1, c2, c3 = st.columns(3)
    c1.metric("⭐ XP Points", xp)
    c2.metric("🔥 Streak", f"{streak} days")
    c3.metric("✅ Tasks completed", completed)

    st.divider()

    profile = get_profile()

    if profile:
        st.subheader(f"Hey, {profile[1] or 'Learner'}! 👋")
        st.write(
            f"**Your goal:** {profile[6] or profile[5] or 'Set a learning goal in My Profile'}")
        st.write(
            f"**Your subjects:** {profile[8] or 'Add subjects in My Profile'}")
        st.write(
            f"**Topics to improve:** {profile[9] or 'Add weak topics in My Profile'}")
    else:
        st.info("Start by setting up your learner profile.")
        st.write("Open **My Profile** in the sidebar.")

    st.divider()
    st.subheader("🌤️ How are you feeling today?")

    energy = st.radio(
        "Choose your current energy level",
        ["Low energy", "Doing okay", "Feeling focused"],
        horizontal=True
    )

    if energy == "Low energy":
        st.info("Try one small 10-minute task. A little progress counts!")
        suggested_minutes = 10
    elif energy == "Doing okay":
        st.info("A 20-minute study session could work well today.")
        suggested_minutes = 20
    else:
        st.info("You could try a focused 30-minute learning session.")
        suggested_minutes = 30

    st.caption(
        f"Suggested session: {suggested_minutes} minutes. "
        "This is a flexible suggestion, not a strict target."
    )

    st.divider()
    st.subheader("🎯 Today's Tasks")

    with db() as con:
        tasks = con.execute(
            "SELECT id, title, minutes, completed FROM goals ORDER BY id DESC"
        ).fetchall()

    if not tasks:
        st.info("No tasks yet. Add one in Study Planner.")
    else:
        for task_id, title, minutes, completed in tasks:
            checked = st.checkbox(
                f"{title} · {minutes} min",
                value=bool(completed),
                key=f"dash_task_{task_id}"
            )

            if checked != bool(completed):
                with db() as con:
                    con.execute(
                        "UPDATE goals SET completed=? WHERE id=?",
                        (int(checked), task_id)
                    )
                if checked:
                    earn_xp(10)
                    st.toast("Task complete! +10 XP 🎉")
                st.rerun()

# =========================
# PROFILE / ONBOARDING
# =========================
elif page == "👤 My Profile":
    st.title("👤 Personalise Your Learning")

    st.write(
        "Tell Phoenix about your goals and preferences "
        "so it can help you plan your learning."
    )

    old = get_profile()

    with st.form("profile_form"):
        name = st.text_input(
            "What should we call you?",
            value=old[1] if old else ""
        )

        age = st.selectbox(
            "Age range",
            ["Under 13", "13–15", "16–18", "19+"],
            index=2
        )

        education = st.selectbox(
            "Education level",
            ["Middle school", "High school",
             "Undergraduate", "Postgraduate", "Other"]
        )

        institution = st.text_input(
            "School / college / field of study",
            value=old[4] if old else ""
        )

        goal = st.text_input(
            "What is your main learning goal?",
            value=old[5] if old else "",
            placeholder="Example: Prepare for my programming exam"
        )

        target_date = st.date_input(
            "Target date",
            value=date.today()
        )

        subjects = st.multiselect(
            "Choose your subjects",
            ["Mathematics", "Physics", "Chemistry",
             "Computer Science", "Biology", "English", "Other"],
            default=[
                s for s in (old[8] or "").split(", ")
            ] if old else []
        )

        weak = st.text_area(
            "Topics you find difficult",
            value=old[9] if old else "",
            placeholder="Example: Python loops, matrices"
        )

        study_minutes = st.select_slider(
            "How much time can you usually study daily?",
            options=[10, 20, 30, 45, 60, 90],
            value=30
        )

        learning_style = st.selectbox(
            "How do you prefer to learn?",
            ["Step-by-step examples", "Short explanations",
             "Practice questions", "Visual diagrams", "Videos"]
        )

        study_time = st.selectbox(
            "When do you prefer to study?",
            ["Morning", "Afternoon", "Evening", "It varies"]
        )

        save = st.form_submit_button("💾 Save my profile")

    if save:
        with db() as con:
            con.execute("""
                INSERT OR REPLACE INTO profile
                VALUES (1, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                name, age, education, institution, goal,
                target_date.isoformat(), ", ".join(subjects),
                weak, study_minutes, learning_style, study_time
            ))
        st.success("Profile saved! Your learning plan is ready.")

# =========================
# DIAGNOSTIC SKILL CHECK
# =========================
elif page == "🧠 Skill Check":
    st.title("🧠 Quick Skill Check")
    st.write("Answer a few questions to check your starting point.")

    topic = st.selectbox(
        "Choose a topic",
        ["Python Basics", "Matrices", "Chemistry"]
    )

    questions = {
        "Python Basics": [
            ("Which keyword defines a function?",
             ["func", "def", "function", "make"], "def"),
            ("Which type stores True or False?",
             ["int", "str", "bool", "float"], "bool"),
            ("What is 2 + 3?",
             ["23", "5", "6", "1"], "5")
        ],
        "Matrices": [
            ("A matrix with one row is a…",
             ["Row matrix", "Column matrix", "Square matrix"], "Row matrix"),
            ("A square matrix has…",
             ["Equal rows and columns", "One row", "One column"],
             "Equal rows and columns"),
            ("The diagonal entries of an identity matrix are…",
             ["0", "1", "2"], "1")
        ],
        "Chemistry": [
            ("What is the formula of water?",
             ["CO2", "H2O", "O2"], "H2O"),
            ("A catalyst generally changes the…",
             ["Reaction rate", "Equilibrium constant", "Products only"],
             "Reaction rate"),
            ("Neutral pH at 25°C is…",
             ["0", "7", "14"], "7")
        ]
    }

    with st.form("diagnostic"):
        answers = []
        for i, (question, options, correct) in enumerate(questions[topic]):
            answers.append(
                st.radio(
                    f"Q{i+1}. {question}",
                    options,
                    key=f"diag_{topic}_{i}"
                )
            )
        submitted = st.form_submit_button("Check my answers")

    if submitted:
        correct_count = sum(
            answers[i] == questions[topic][i][2]
            for i in range(len(answers))
        )
        st.session_state[f"score_{topic}"] = correct_count

        st.success(
            f"You got {correct_count} out of {len(answers)} correct."
        )

        if correct_count == len(answers):
            st.write("**Suggested next step:** Try a more advanced topic.")
        elif correct_count == 0:
            st.write("**Suggested next step:** Review the basics first.")
        else:
            st.write("**Suggested next step:** Practise the questions you missed.")

        st.caption(
            "This is a small demo assessment, not a complete measure "
            "of your ability."
        )

# =========================
# LEARNING ROADMAP
# =========================
elif page == "🗺️ Learning Roadmap":
    st.title("🗺️ Your Learning Roadmap")

    profile = get_profile()

    if not profile:
        st.info("Set up your profile first.")
    else:
        st.write(f"### Goal: {profile[5] or 'Your learning goal'}")
        st.write(f"**Target date:** {profile[6]}")
        st.write(f"**Preferred learning style:** {profile[10]}")
        st.write(f"**Preferred study time:** {profile[11]}")

        st.divider()
        st.subheader("Your learning path")

        st.markdown("""
        **1. Start with the basics**  
        Review the key ideas and prerequisites.

        **2. Check your skills**  
        Take the Skill Check and identify topics to practise.

        **3. Practise in small steps**  
        Break a difficult topic into short study tasks.

        **4. Review mistakes**  
        Revisit questions you missed and try again.

        **5. Track your progress**  
        Mark completed tasks and check your XP.
        """)

        st.divider()
        st.subheader("🧩 Skill-gap overview")

        if profile[9]:
            st.warning(
                f"Topics you identified for practice: {profile[9]}"
            )
        else:
            st.info("Add topics you find difficult in My Profile.")

        st.write("### Diagnostic results")
        for subject in ["Python Basics", "Matrices", "Chemistry"]:
            score = st.session_state.get(f"score_{subject}")
            if score is not None:
                st.write(f"**{subject}:** {score}/3 correct")

        st.caption(
            "Roadmap and skill-gap suggestions are rule-based in this MVP. "
            "They are not yet generated by an AI model."
        )

# =========================
# STUDY PLANNER
# =========================
elif page == "📅 Study Planner":
    st.title("📅 Study Planner")
    st.write("Plan study sessions, assignments, and deadlines.")

    st.subheader("➕ Add a study task")

    with st.form("task_form"):
        title = st.text_input(
            "Task",
            placeholder="Example: Practise Python loops"
        )
        minutes = st.selectbox(
            "Task length",
            [10, 20, 30, 45, 60]
        )
        add_task = st.form_submit_button("Add task")

    if add_task and title.strip():
        with db() as con:
            con.execute(
                "INSERT INTO goals (title, minutes) VALUES (?, ?)",
                (title.strip(), minutes)
            )
        st.success("Task added!")
        st.rerun()

    st.divider()
    st.subheader("🗓️ Add a deadline")

    with st.form("event_form"):
        event = st.text_input(
            "Event or deadline",
            placeholder="Example: Chemistry test"
        )
        event_day = st.date_input("Date", value=date.today())
        add_event = st.form_submit_button("Save deadline")

    if add_event and event.strip():
        with db() as con:
            con.execute(
                "INSERT INTO events (title, event_date) VALUES (?, ?)",
                (event.strip(), event_day.isoformat())
            )
        st.success("Deadline saved!")
        st.rerun()

    st.divider()
    st.subheader("📌 Upcoming deadlines")

    with db() as con:
        events = con.execute(
            "SELECT id, title, event_date FROM events ORDER BY event_date"
        ).fetchall()

    if not events:
        st.info("No deadlines yet.")
    else:
        for event_id, event_title, event_date in events:
            left, right = st.columns([4, 1])
            left.write(f"**{event_date}** — {event_title}")

            if right.button("Delete", key=f"del_{event_id}"):
                with db() as con:
                    con.execute(
                        "DELETE FROM events WHERE id=?",
                        (event_id,)
                    )
                st.rerun()

    st.divider()
    st.subheader("🔄 Missed a task?")

    st.write(
        "No need to restart your whole plan. "
        "Choose a smaller task or move it to another day."
    )

    with db() as con:
        incomplete = con.execute(
            "SELECT id, title, minutes FROM goals WHERE completed=0"
        ).fetchall()

    if incomplete:
        options = {
            f"{title} ({minutes} min)": task_id
            for task_id, title, minutes in incomplete
        }

        selected = st.selectbox(
            "Choose a task to break into a smaller step",
            list(options.keys())
        )

        if st.button("Make a 10-minute version"):
            smaller_title = "10-min starter: " + selected.split(" (")[0]
            with db() as con:
                con.execute(
                    "INSERT INTO goals (title, minutes) VALUES (?, ?)",
                    (smaller_title, 10)
                )
            st.success("Added a smaller starter task!")
            st.rerun()

# =========================
# FEEDBACK
# =========================
elif page == "💬 Feedback":
    st.title("💬 Help Phoenix improve")

    with st.form("feedback_form"):
        rating = st.select_slider(
            "How useful is Phoenix?",
            options=[
                "Not useful", "A little", "Okay",
                "Useful", "Very useful"
            ]
        )

        comment = st.text_area(
            "What should we improve?",
            placeholder="Tell us what you liked or would change..."
        )

        submit = st.form_submit_button("Send feedback")

    if submit:
        with db() as con:
            con.execute(
                "INSERT INTO feedback (rating, comment) VALUES (?, ?)",
                (rating, comment)
            )
        st.success("Thanks for helping Phoenix grow! 💜")

    st.caption(
        "Phoenix MVP • Free Plan • Progress saved locally in SQLite"
    )
