from notion_client import Client
import streamlit as st
from datetime import datetime


# This file contains all functions that interact directly with the Notion API.

@st.cache_resource
def init_notion_client(api_key):
    """Initializes and returns a cached Notion client."""
    if not api_key:
        st.error("FATAL ERROR: NOTION_API_KEY not found. The veil is sealed.")
        st.stop()
    return Client(auth=api_key)


@st.cache_data(ttl=30)
def get_all_ideas(_notion_client, database_id):
    """
    Fetches and bulletproof-parses all ideas from the Notion database.
    This function is forged in paranoia to never fail on empty or missing properties.
    """
    try:
        response = _notion_client.databases.query(database_id=database_id)
        ideas = []
        for page in response.get('results', []):
            props = page.get('properties', {})

            # THE BUG FIX IS HERE: This new logic safely handles any missing data.
            name_prop = props.get('Name', {}).get('title', [])
            name = name_prop[0].get('plain_text', 'Untitled') if name_prop else 'Untitled'

            desc_prop = props.get('Description', {}).get('rich_text', [])
            description = desc_prop[0].get('plain_text', '') if desc_prop else ''

            res_prop = props.get('Resources', {}).get('rich_text', [])
            resources = res_prop[0].get('plain_text', '') if res_prop else ''

            status = (props.get('Status', {}).get('select') or {}).get('name', 'None')

            priority = (props.get('Priority', {}).get('select') or {}).get('name', 'None')

            deadline = (props.get('Deadline', {}).get('date') or {}).get('start')

            ideas.append({
                'id': page['id'],
                'name': name,
                'description': description,
                'status': status,
                'priority': priority,
                'deadline': deadline,
                'resources': resources
            })
        return ideas
    except Exception as e:
        st.error(f"❌ API Error: Could not penetrate Notion's veil. Details: {e}")
        return []


def update_idea_in_notion(_notion_client, page_id, properties):
    """Updates a page in the Notion database."""
    try:
        _notion_client.pages.update(page_id=page_id, properties=properties)
        st.success("✅ Reality has been altered.")
    except Exception as e:
        st.error(f"❌ Alteration failed: {e}")


def create_idea_in_notion(_notion_client, database_id, properties):
    """Creates a page in the Notion database."""
    try:
        _notion_client.pages.create(parent={"database_id": database_id}, properties=properties)
        st.success("✅ A new soul has been forged.")
    except Exception as e:
        st.error(f"❌ Forging failed: {e}")
