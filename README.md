# Project Phoenix 2026
Team project for Codeathon
# 🔥 Project Phoenix - Personalized Learning Agent

> One-size-fits-all teaching fails 78% students. Phoenix is an AI agent that learns HOW you learn.

### 🎯 Problem Statement
Every student learns differently - some are visual learners, some learn by doing. But colleges teach everyone the same way. Students face issues in understanding, don't know their strengths/weaknesses, and use AI randomly without personalization.

### 💡 Our Solution
Project Phoenix is an intelligent learning companion that:
1.  **Detects Learning Style:** Visual / Auditory / Reading / Kinesthetic via interactive survey
2.  **Analyzes Strengths & Weaknesses:** Predicts which subjects need improvement
3.  **Personalized AI Tutor:** Recommends videos for visual learners, notes for reading learners, practicals for kinesthetic learners
4.  **AI Study Assistant:** Smart, context-aware help instead of generic ChatGPT answers

### ✨ Features
- 📊 Learning Style Assessment Test
- 🧠 Strength & Weakness Analyzer
- 🎯 Subject-wise Improvement Prediction
- 🤖 AI-Powered Personalized Study Recommendations
- 📈 Real Student Validation - Surveyed 45+ students

### 🛠️ Tech Stack
- **Frontend:** Streamlit
- **Backend:** Python
- **Database:** SQLite (`phoenix.db` - locally handled)
- **AI:** LLM Agent for personalized recommendations

### 📊 User Validation
We conducted a survey with 45+ students:
- 78% face issues with one common teaching method
- 82% use AI for studying but not personalized
- 85% said YES to a personalized AI agent that tells them HOW to study

[Insert your Google Form chart screenshot here]

### 🚀 How to Run Locally
```bash
git clone https://github.com/YOUR_USERNAME/Project-Phoenix.git
cd Project-Phoenix
pip install -r requirements.txt
python -m streamlit run app.py