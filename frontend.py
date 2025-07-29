import streamlit as st
import requests
import sqlite3

# --- Setup SQLite DB ---
conn = sqlite3.connect("feedback.db", check_same_thread=False)
c = conn.cursor()
c.execute('''
    CREATE TABLE IF NOT EXISTS feedback (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        role TEXT NOT NULL,
        question TEXT NOT NULL,
        response TEXT NOT NULL,
        feedback TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
''')
conn.commit()

# --- Sidebar: Role Selection ---
st.sidebar.title("Select Role")
role = st.sidebar.radio("Who are you?", ("Employee", "Manager"))

st.title("🤖 Role-Based AI Assistant")

# --- Session State Setup ---
if "query" not in st.session_state:
    st.session_state.query = ""
if "result" not in st.session_state:
    st.session_state.result = ""

# --- Ask Question ---
query = st.text_input("Ask a question", value=st.session_state.query)

if st.button("Get Answer"):
    if query:
        response = requests.post("http://localhost:5000/ask", json={"query": query, "role": role})
        if response.status_code == 200:
            result = response.json()["response"]
            st.session_state.query = query
            st.session_state.result = result
            # st.success(result)
        else:
            st.error("Error: " + response.text)

# --- Show Result if available ---
if st.session_state.result:
    st.success(st.session_state.result)

    # --- Feedback section ---
    st.subheader("💬 Provide Feedback")
    feedback_text = st.text_area("How was the response?", key="feedback")

    if st.button("Submit Feedback"):
        if feedback_text.strip():
            c.execute('''
                INSERT INTO feedback (role, question, response, feedback)
                VALUES (?, ?, ?, ?)
            ''', (role, st.session_state.query, st.session_state.result, feedback_text.strip()))
            conn.commit()
            st.success("✅ Feedback submitted successfully!")
        else:
            st.warning("Feedback cannot be empty.")

# --- Manager-only Feedback View ---
if role == "Manager":
    st.subheader("📊 View All Feedback")
    cursor = conn.cursor()
    cursor.execute("SELECT role, question, response, feedback, timestamp FROM feedback ORDER BY timestamp DESC")
    rows = cursor.fetchall()

    if rows:
        for row in rows:
            with st.expander(f"Feedback from {row[0]} at {row[4]}"):
                st.write(f"**Question:** {row[1]}")
                st.write(f"**Response:** {row[2]}")
                st.write(f"**Feedback:** {row[3]}")
    else:
        st.info("No feedback submitted yet.")
