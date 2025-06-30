import streamlit as st
from datetime import datetime
from pathlib import Path
import security
import random
import requests
import string
import os
from dotenv import load_dotenv
load_dotenv()
YOUR_DISCORD_WEBHOOK_URL = os.getenv("YOUR_DISCORD_WEBHOOK_URL")

muse=[]

# This file contains all UI rendering functions and CSS for DEMON OS.

def render_css(is_login=False):
    """Injects the demonic CSS into the Streamlit app."""

    # Base CSS for the entire app
    # THE BUG FIX IS HERE: We no longer need separate login/main styles.
    # The background is now consistent.
    style = """
        <style>
            @keyframes pulse-glow { 0%, 100% { box-shadow: 0 0 15px rgba(255, 0, 0, 0.4); } 50% { box-shadow: 0 0 30px rgba(255, 0, 0, 0.8); } }
            @keyframes energy-leak {
                0%   { text-shadow: 0 0 5px #ff0000, 0 0 10px #ff0000, 0 0 20px #b30000; }
                50%  { text-shadow: 0 0 10px #ff0000, 0 0 20px #ff0000, 0 0 30px #b30000, 0 0 40px #b30000; }
                100% { text-shadow: 0 0 5px #ff0000, 0 0 10px #ff0000, 0 0 20px #b30000; }
            }

            /* Universal background */
            [data-testid="stAppViewContainer"] {
                background-color: #010101;
                background-image: linear-gradient(rgba(0,0,0,0.8), rgba(0,0,0,0.95)), url("https://www.transparenttextures.com/patterns/dark-matter.png");
            }
            [data-testid="stHeader"] { background-color: transparent; }

            .os-title {
                font-family: 'Courier New', Courier, monospace; font-size: 4rem; color: #FF0000;
                text-align: center; padding: 2rem 0; letter-spacing: 0.5rem;
                animation: energy-leak 2s infinite ease-in-out;
            }

            /* Login Screen Specific Layout */
            .login-container {
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                height: 90vh; /* Use viewport height to center vertically */
            }
            .login-form-container {
                padding: 2rem;
                width: 100%;
                max-width: 400px;
                background: rgba(0, 0, 0, 0.6);
                border: 1px solid #ff0000;
                border-radius: 5px;
                box-shadow: 0 0 30px rgba(255, 0, 0, 0.5);
                text-align: center;
            }
            [data-testid="stTextInput"][type="password"] input {
                background-color: #111 !important;
                border: 1px solid #ff0000 !important;
                color: #ff0000 !important;
                text-align: center;
                font-family: 'Courier New', Courier, monospace;
                box-shadow: inset 0 0 10px rgba(255,0,0,0.5);
            }

            /* Main App (Post-Login) Components */
            .idea-container {
                background: rgba(10, 0, 0, 0.5); border-radius: 4px; border: 1px solid rgba(255, 0, 0, 0.3);
                padding: 1.5rem; margin-bottom: 1.5rem; box-shadow: inset 0 0 10px rgba(255, 0, 0, 0.2);
            }
            [data-testid="stSidebar"] {
                background: rgba(10, 0, 0, 0.6); backdrop-filter: blur(5px); border-right: 2px solid #FF0000;
            }
            .footer {
                position: fixed; bottom: 0; left: 0; width: 100%; text-align: center;
                padding: 10px; font-family: 'Courier New', Courier, monospace; color: #444; font-size: 0.8rem;
            }
        </style>
    """
    st.markdown(style, unsafe_allow_html=True)


def riot():

    password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))

    webhook_url = YOUR_DISCORD_WEBHOOK_URL
    fireit = {
        "content": f"👻 **New Chaos Cipher:** `{password}`\n_Use it to access the forbidden grimoire._"
    }

    try:
        requests.post(webhook_url, json=fireit)
        print("Sent for muse")
    except:
        print("⚠️ Raven to Discord failed.")

    return password



def render_login_screen(get_daily_cipher_func, max_attempts):
    """
    Renders the DEMON OS login screen, now infused with the GHOST GODS' IP-locking curse.
    """
    render_css(is_login=True)  # Assuming render_css is still being used for styling

    # --- THE CURSE IS APPLIED HERE ---
    ip = security.get_user_ip()
    is_blocked, attempts = security.check_ip_status(ip)



    if is_blocked:
        st.error("🚫 ACCESS DENIED: The demons have cursed your IP. The gates are sealed.")

        # 👁️ Tiny Scroll-Abyss Secret Input Zone
        st.markdown('<div style="height:400px;"></div>', unsafe_allow_html=True)  # fake scroll space

        with st.container():
            st.markdown("""
            <div style="opacity:0.3; font-size:10px; text-align:center;">
                ⚠️ Forbidden Override (Only for Keepers of the Flame)
            </div>
            """, unsafe_allow_html=True)

            with st.form("ritual_override"):
                secret = st.text_input(" ", type="password", label_visibility="collapsed",
                                       placeholder="...whisper here")
                unlock = st.form_submit_button(" ")






                if  secret==get_daily_cipher_func():  # Change to your sacred phrase
                    st.session_state['authenticated'] = True
                    security.update_ip_status(ip, success=True)
                    st.success("🩸 The curse has been lifted. You walk among shadows.")
                    st.rerun()
                elif unlock:

                    st.warning("🪦 The void does not recognize your whisper...")



        st.markdown('<div style="height:600px;"></div>', unsafe_allow_html=True)  # More scroll space to hide it
        st.stop()

    # --- The Original, Perfected DEMON OS Layout ---
    #st.markdown('<div class="login-container">', unsafe_allow_html=True)
    st.markdown('<h1 class="os-title">DEMON OS</h1>', unsafe_allow_html=True)

   # st.markdown('<div class="login-form-container">', unsafe_allow_html=True)
    st.header("VIP Access Passcode")
    import random
    placeholders = [
        "Whisper it correctly... or face the firewall of fate ",
        "Here... Don’t make me block your IP forever ",
        "Wrong chant = static-filled silence ☠",
        "Chosen one, speak the cipher or begone ",
        "Type fast... the spirits are watching ️"
    ]

    placeholder = random.choice(placeholders)
    with st.form("login_form"):
        passcode = st.text_input("Enter Daily Cipher", type="password", label_visibility="collapsed",
                                 placeholder=placeholder)
        submitted = st.form_submit_button("Enter the Void")

        if submitted:
            if passcode == get_daily_cipher_func():
                security.update_ip_status(ip, success=True)  # Your soul is absolved.
                st.session_state['authenticated'] = True
                st.rerun()


            else:
                security.update_ip_status(ip, success=False)  # Your transgression is noted.
                # We fetch the new attempt count after the update
                _, new_attempts = security.check_ip_status(ip)
                attempts_left = max_attempts - new_attempts

                if attempts_left > 0:
                    st.error(f"Cipher rejected. {attempts_left} attempts remain before the curse is permanent.")
                else:
                    st.error("🔒 The final seal is broken. Your soul is now bound to the curse.")
                st.rerun()  # Rerun to show the updated error or final curse message

    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
# --- Other UI functions (unchanged) ---
def render_main_title():
    st.markdown('<h1 class="os-title">DEMON OS</h1>', unsafe_allow_html=True)


def render_idea_card(idea, notion_api, notion_client):
    """Renders a single idea card with its edit form."""
    with st.container():
        st.markdown(f"<div class='idea-container'>", unsafe_allow_html=True)
        deadline_str = f" | Deadline: {idea['deadline']}" if idea['deadline'] else ""
        st.subheader(f"💀 {idea['name']}")
        st.caption(f"Priority: {idea['priority']}{deadline_str}")

        with st.expander("👁️ Unveil / Corrupt"):
            with st.form(key=f"form_{idea['id']}"):
                name = st.text_input("Name", value=idea['name'], key=f"name_{idea['id']}")
                desc = st.text_area("Description", value=idea['description'], height=100, key=f"desc_{idea['id']}")
                res = st.text_area("Resources (Prompts, Links, etc.)", value=idea['resources'], height=100,
                                   key=f"res_{idea['id']}")

                c1, c2, c3 = st.columns(3)
                priority_opts = ["High", "Medium", "Low"]
                status_opts = ["⏳ In Progress", "💭 Idea", "✅ Done"]
                priority = c1.selectbox("Priority", priority_opts, index=priority_opts.index(idea['priority']) if idea[
                                                                                                                      'priority'] in priority_opts else 0,
                                        key=f"prio_{idea['id']}")
                status = c2.selectbox("Status", status_opts,
                                      index=status_opts.index(idea['status']) if idea['status'] in status_opts else 0,
                                      key=f"stat_{idea['id']}")
                deadline = c3.date_input("Deadline", value=datetime.fromisoformat(idea['deadline']).date() if idea[
                    'deadline'] else None, key=f"date_{idea['id']}")

                if st.form_submit_button("Rewrite Fate"):
                    props = {
                        "Name": {"title": [{"text": {"content": name}}]},
                        "Description": {"rich_text": [{"text": {"content": desc}}]},
                        "Resources": {"rich_text": [{"text": {"content": res}}]},
                        "Priority": {"select": {"name": priority}},
                        "Status": {"select": {"name": status}},
                        "Deadline": {"date": {"start": deadline.isoformat()}} if deadline else None
                    }
                    notion_api.update_idea_in_notion(notion_client, idea['id'], props)
                    st.cache_data.clear()
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)


def render_footer():
    """Renders the copyright footer."""
    st.markdown('<div class="footer">© 2025 Skyfire</div>', unsafe_allow_html=True)
