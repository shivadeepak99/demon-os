import streamlit as st
import os
from dotenv import load_dotenv
from datetime import datetime
import security
# Import our separated modules
import notion_api
import ui_components

# --- 💀 CONFIGURATION ---
load_dotenv()
NOTION_API_KEY = os.getenv("NOTION_API_KEY")
NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")
APP_SEED = os.getenv("APP_SEED", "GHOST")
MAX_ATTEMPTS = 3


def get_daily_cipher():
    """Generates the passcode based on the secret seed and current day."""
    return f"{APP_SEED}{datetime.now().strftime('%A')}"


# --- 🚀 MAIN APP LOGIC ---
def main_app():
    """Renders the main application view after successful login."""
    # Initialize Notion client
    notion_client = notion_api.init_notion_client(NOTION_API_KEY)

    # --- Sidebar: Command & Control ---
    with st.sidebar:
        st.header("Create Manifestation")
        with st.form("new_idea_form", clear_on_submit=True):
            name = st.text_input("Name")
            desc = st.text_area("Description")
            res = st.text_area("Resources")
            c1, c2 = st.columns(2)
            priority = c1.selectbox("Priority", ["High", "Medium", "Low"])
            status = c2.selectbox("Status", ["💭 Idea", "⏳ In Progress", "✅ Done"])
            deadline = st.date_input("Deadline", value=None)

            if st.form_submit_button("Forge"):
                if name:
                    props = {
                        "Name": {"title": [{"text": {"content": name}}]},
                        "Description": {"rich_text": [{"text": {"content": desc}}]},
                        "Resources": {"rich_text": [{"text": {"content": res}}]},
                        "Priority": {"select": {"name": priority}},
                        "Status": {"select": {"name": status}},
                        "Deadline": {"date": {"start": deadline.isoformat()}} if deadline else None
                    }
                    notion_api.create_idea_in_notion(notion_client, NOTION_DATABASE_ID, props)
                    st.cache_data.clear()
                else:
                    st.warning("A soul requires a name.")

        st.divider()
        if st.button("🔄 Resync Reality"):
            st.cache_data.clear()
            st.rerun()
        if st.button("Disengage"):
            st.session_state['authenticated'] = False
            st.rerun()

    # --- Main Panel: Data Visualization ---
    st.title("DEMON OS")
    all_ideas = notion_api.get_all_ideas(notion_client, NOTION_DATABASE_ID)

    if not all_ideas:
        st.warning("The void is empty. Forge something new.")
    else:
        in_progress = [i for i in all_ideas if i['status'] == '⏳ In Progress']
        idea_stage = [i for i in all_ideas if i['status'] == '💭 Idea']
        done = [i for i in all_ideas if i['status'] == '✅ Done']

        tab1, tab2, tab3 = st.tabs(
            [f"Forging ({len(in_progress)})", f"Incubating ({len(idea_stage)})", f"Conquered ({len(done)})"])

        with tab1:
            for idea in in_progress: ui_components.render_idea_card(idea, notion_api, notion_client)
        with tab2:
            for idea in idea_stage: ui_components.render_idea_card(idea, notion_api, notion_client)
        with tab3:
            for idea in done: ui_components.render_idea_card(idea, notion_api, notion_client)

    ui_components.render_footer()


# --- LAUNCHER ---
ui_components.render_css()

if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

if st.session_state['authenticated']:
    main_app()
else:
    # We now pass the MAX_ATTEMPTS constant from our new security module
    ui_components.render_login_screen(get_daily_cipher, security.MAX_ATTEMPTS)