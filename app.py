import gradio as gr
import requests
import os
import subprocess
import time
import sys

# --- Backend Management ---
proc = None
def start_backend():
    global proc
    # Kill existing if any (optional, but uvicorn might already be running)
    print("🚀 Starting FastAPI backend in background...")
    proc = subprocess.Popen([sys.executable, "-m", "uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8000"])
    time.sleep(3) # Give it a moment to initialize

start_backend()

BASE_URL = "http://127.0.0.1:8000"

# --- Premium Dark Mode Glassmorphism CSS ---
custom_css = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&family=Outfit:wght@500;700&display=swap');

:root {
    --primary-gradient: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
    --bg-dark: #070b14;
    --glass-bg: rgba(17, 25, 40, 0.85);
    --glass-border: rgba(255, 255, 255, 0.15);
    --sidebar-bg: rgba(7, 11, 20, 0.95);
    --text-primary: #f8fafc;
    --text-secondary: #94a3b8;
}

/* Force Dark Mode and Background */
body, .gradio-container {
    background: radial-gradient(circle at top right, #1e1b4b 0%, #070b14 70%) !important;
    font-family: 'Inter', sans-serif !important;
    color: var(--text-primary) !important;
    min-height: 100vh;
}

/* Sidebar Styling */
.sidebar-panel {
    background: var(--sidebar-bg) !important;
    border-right: 1px solid var(--glass-border) !important;
    padding: 2rem !important;
    min-height: 100vh !important;
}

/* Force dark inputs */
.dark input, .dark textarea, input, textarea, select {
    background: rgba(30, 41, 59, 0.8) !important;
    color: #f8fafc !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    border-radius: 10px !important;
}

/* Ensure labels and text are visible */
label, .label-wrap span, .svelte-1gfkn6j {
    color: #cbd5e1 !important;
}

/* Tab styling */
.tab-nav button {
    color: #94a3b8 !important;
    background: transparent !important;
}

.tab-nav button.selected {
    color: #818cf8 !important;
    border-bottom: 2px solid #818cf8 !important;
}

/* Glass Panels for Content */
.glass-panel {
    background: var(--glass-bg) !important;
    border-radius: 24px !important;
    border: 1px solid var(--glass-border) !important;
    backdrop-filter: blur(20px) !important;
    padding: 2rem !important;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.4) !important;
}

/* Hero Section */
.hero-title {
    font-family: 'Outfit', sans-serif;
    font-size: 3.5rem !important;
    font-weight: 800;
    background: linear-gradient(to right, #f8fafc, #818cf8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-align: center;
    margin-bottom: 0.5rem;
    animation: fadeInDown 1s ease-out;
}

.hero-subtitle {
    color: var(--text-secondary);
    font-size: 1.2rem;
    text-align: center;
    margin-bottom: 3rem;
}

/* Chat Styling */
.chatbot-container {
    border-radius: 20px !important;
    border: 1px solid var(--glass-border) !important;
    background: rgba(15, 23, 42, 0.5) !important;
    backdrop-filter: blur(10px);
}

/* Buttons */
.primary-btn {
    background: var(--primary-gradient) !important;
    border: none !important;
    border-radius: 14px !important;
    color: white !important;
    font-weight: 700 !important;
    padding: 0.8rem !important;
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
    text-transform: uppercase !important;
    letter-spacing: 1px !important;
    box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3) !important;
}

.primary-btn:hover {
    transform: translateY(-3px) scale(1.02) !important;
    box-shadow: 0 8px 25px rgba(124, 58, 237, 0.5) !important;
}

/* Sidebar Image Glow */
.sidebar-logo {
    filter: drop-shadow(0 0 12px rgba(99, 102, 241, 0.6));
    margin-bottom: 1rem;
}

@keyframes fadeInDown {
    from { opacity: 0; transform: translateY(-20px); }
    to { opacity: 1; transform: translateY(0); }
}
"""

# --- Logic Helper Functions ---
def login(email, password):
    try:
        res = requests.post(f"{BASE_URL}/login", json={"email": email, "password": password})
        if res.status_code == 200:
            token = res.json()["access_token"]
            return gr.update(visible=False), gr.update(visible=True), token, "👋 Welcome back!"
        return gr.update(visible=True), gr.update(visible=False), None, "❌ Authentication failed."
    except:
        return gr.update(visible=True), gr.update(visible=False), None, "⚠️ Backend connection error."

def signup(name, email, password):
    res = requests.post(f"{BASE_URL}/signup", json={"name": name, "email": email, "password": password})
    if res.status_code == 200:
        return "✅ Account created! You can now log in."
    return f"❌ {res.text}"

def add_website(url, token):
    if not token: return "Please login first."
    headers = {"Authorization": f"Bearer {token}"}
    res = requests.post(f"{BASE_URL}/add-website", json={"url": url}, headers=headers)
    if res.status_code == 200:
        return f"✅ Successfully indexed: {res.json()['total_chunks']} chunks."
    return f"❌ Error: {res.text}"

def chat_response(message, history, token):
    if not token:
        history.append({"role": "user", "content": message})
        history.append({"role": "assistant", "content": "Please login first."})
        return history, ""
    headers = {"Authorization": f"Bearer {token}"}
    try:
        res = requests.post(f"{BASE_URL}/chat", json={"message": message}, headers=headers)
        if res.status_code == 200:
            result = res.json()
            history.append({"role": "user", "content": message})
            history.append({"role": "assistant", "content": f"[{result['mode'].upper()}] {result['answer']}"})
            return history, ""
        history.append({"role": "user", "content": message})
        history.append({"role": "assistant", "content": "⚠️ Server issue."})
        return history, ""
    except:
        history.append({"role": "user", "content": message})
        history.append({"role": "assistant", "content": "⚠️ Connection lost."})
        return history, ""

def save_api_key(key):
    if not key.strip(): return "Invalid Key."
    with open(".env", "w") as f:
        f.write(f"GEMINI_API_KEY={key.strip()}\n")
    return "✅ API Key Updated!"

# --- Build UI with Sidebar ---
with gr.Blocks(title="AI Website Companion", css=custom_css) as demo:
    token_state = gr.State(None)
    
    with gr.Row():
        # Sidebar Column (Left)
        with gr.Column(scale=1, elem_classes="sidebar-panel"):
            gr.HTML("""
                <div style="text-align: center;">
                    <img src="https://huggingface.co/front/assets/huggingface_logo.svg" width="80" class="sidebar-logo">
                    <h2 style="font-size: 1.5rem; font-family: 'Outfit'; margin-bottom: 2rem;">CONTROL CENTER</h2>
                </div>
            """)
            
            gr.Markdown("### ⚙️ Settings")
            api_key_input = gr.Textbox(label="Google Gemini API", type="password", placeholder="Enter key...")
            save_key_btn = gr.Button("Save API Key", elem_classes="primary-btn")
            key_status = gr.Markdown()
            
            def check_backend():
                try:
                    return requests.get(BASE_URL).status_code == 200
                except:
                    return False

            status_text = "**Backend:** 🟢 Connected" if check_backend() else "**Backend:** 🟡 Initializing..."
            gr.Markdown(status_text)
            gr.Markdown("**Storage:** ChromaDB Active")
            
        # Main Content Column (Right)
        with gr.Column(scale=4, elem_id="main-content"):
            # Hero
            gr.HTML("""
                <div style="margin-top: 1rem; margin-bottom: 2rem;">
                    <h1 class="hero-title">🤖 AI Website Companion</h1>
                    <p class="hero-subtitle">High-Fidelity RAG Experience for Intelligent Web Interaction</p>
                </div>
            """)
            
            # Authentication Layer
            with gr.Column(visible=True) as auth_view:
                with gr.Column(elem_classes="glass-panel"):
                    with gr.Tabs():
                        with gr.Tab("LOGIN 🔑"):
                            lemail = gr.Textbox(label="Email Address", placeholder="your@email.com")
                            lpass = gr.Textbox(label="Password", type="password")
                            lbtn = gr.Button("Access Workspace", elem_classes="primary-btn")
                            lmsg = gr.Markdown()
                        with gr.Tab("SIGNUP 📝"):
                            sname = gr.Textbox(label="Full Name")
                            semail = gr.Textbox(label="Email Address")
                            spass = gr.Textbox(label="Password", type="password")
                            sbtn = gr.Button("Create Workspace", elem_classes="primary-btn")
                            smsg = gr.Markdown()

            # Main Operations Layer
            with gr.Column(visible=False) as main_view:
                with gr.Tabs():
                    # Chat Tab
                    with gr.Tab("💬 CONVERSATIONS"):
                        chatbot = gr.Chatbot(label="Verified Agent", elem_classes="chatbot-container", height=500)
                        with gr.Row():
                            msg_in = gr.Textbox(placeholder="Inquire about indexed sources...", scale=9, show_label=False)
                            send_btn = gr.Button("GO", scale=1, elem_classes="primary-btn")
                        clear = gr.ClearButton([msg_in, chatbot], size="sm")
                    
                    # Knowledge Tab
                    with gr.Tab("🌐 KNOWLEDGE ENGINE"):
                        with gr.Column(elem_classes="glass-panel"):
                            gr.Markdown("### Index Source")
                            url_in = gr.Textbox(label="Source URL", placeholder="https://docs.example.com/start")
                            index_btn = gr.Button("Inject to Brain", elem_classes="primary-btn")
                            index_res = gr.Markdown()

    # Event Wiring
    lbtn.click(login, [lemail, lpass], [auth_view, main_view, token_state, lmsg])
    sbtn.click(signup, [sname, semail, spass], smsg)
    save_key_btn.click(save_api_key, api_key_input, key_status)
    index_btn.click(add_website, [url_in, token_state], index_res)
    
    msg_in.submit(chat_response, [msg_in, chatbot, token_state], [chatbot, msg_in])
    send_btn.click(chat_response, [msg_in, chatbot, token_state], [chatbot, msg_in])

# Launch
if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)