import streamlit as st
import requests
import os
import subprocess
import time
import sys

# Ensure FastAPI backend is running
@st.cache_resource
def start_backend():
    # Only start if port 8000 isn't already taken (simple check)
    print("🚀 Starting FastAPI backend in background...")
    proc = subprocess.Popen([sys.executable, "-m", "uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8000"])
    time.sleep(3) # Give it a moment to initialize
    return proc

backend_proc = start_backend()

BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="AI Website Assistant", layout="wide")

st.title("🤖 AI Website Chatbot")

if "token" not in st.session_state:
    st.session_state.token = None

# --- Sidebar ---
st.sidebar.header("⚙️ Settings")

# Gemini API Key input in sidebar
api_key = st.sidebar.text_input("🔑 Gemini API Key", type="password", help="Enter your Google Gemini API key")

if st.sidebar.button("Save API Key"):
    if api_key.strip():
        env_path = os.path.join(os.path.dirname(__file__), ".env")
        with open(env_path, "w") as f:
            f.write(f"GEMINI_API_KEY={api_key.strip()}\n")
        st.sidebar.success("✅ API Key saved! Restart the backend server to apply.")
    else:
        st.sidebar.error("Please enter a valid API key")

st.sidebar.markdown("---")

menu = st.sidebar.selectbox(
    "Navigation",
    ["Signup", "Login", "Add Website", "Ask AI"]
)


if menu == "Signup":

    st.header("Create Account")

    name = st.text_input("Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Signup"):

        data = {
            "name": name,
            "email": email,
            "password": password
        }

        res = requests.post(f"{BASE_URL}/signup", json=data)

        if res.status_code == 200:
            st.success("Account created successfully")
        else:
            st.error(res.text)


elif menu == "Login":

    st.header("Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        data = {
            "email": email,
            "password": password
        }

        res = requests.post(f"{BASE_URL}/login", json=data)

        if res.status_code == 200:

            token = res.json()["access_token"]
            st.session_state.token = token

            st.success("Login successful")

        else:
            st.error("Invalid credentials")


elif menu == "Add Website":

    st.header("Add Website Knowledge")

    if st.session_state.token is None:
        st.warning("Please login first")
        st.stop()

    url = st.text_input("Website URL")

    if st.button("Process Website"):

        headers = {
            "Authorization": f"Bearer {st.session_state.token}"
        }

        data = {
            "url": url
        }

        res = requests.post(
            f"{BASE_URL}/add-website",
            json=data,
            headers=headers
        )

        if res.status_code == 200:

            result = res.json()

            st.success("Website processed successfully")
            st.write("Total chunks:", result["total_chunks"])

        else:
            st.error(res.text)


elif menu == "Ask AI":

    st.header("Ask AI")

    if st.session_state.token is None:
        st.warning("Please login first")
        st.stop()

    question = st.text_input("Ask something")

    if st.button("Send"):

        headers = {
            "Authorization": f"Bearer {st.session_state.token}"
        }

        data = {
            "message": question
        }

        res = requests.post(
            f"{BASE_URL}/chat",
            json=data,
            headers=headers
        )

        if res.status_code == 200:

            result = res.json()

            st.write("### Your Question")
            st.write(result["question"])

            st.write("### AI Answer")
            st.write(result["answer"])

            st.write("Mode:", result["mode"])

        else:
            st.error(res.text)