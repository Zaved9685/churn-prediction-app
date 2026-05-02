import streamlit as st
import sqlite3

if "logged_in" not in st.session_state:
    st.stop()

if st.session_state.role != "admin":
    st.error("Admin only")
    st.stop()

st.title("👑 Admin Panel")

conn = sqlite3.connect("users.db")
data = conn.execute("SELECT username, role FROM users").fetchall()

st.write(data)
