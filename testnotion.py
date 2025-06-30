import os
from notion_client import Client
from dotenv import load_dotenv

# --- TEST SCRIPT ---
# This script does one thing: It tries to connect to your Notion database
# and retrieve its properties. If it succeeds, your keys and permissions are correct.

print("🐍 Running Notion Connection Test...")

# 1. LOAD SECRETS
# Make sure your .env file is in the same folder as this script.
# It should contain:
# NOTION_API_KEY="secret_xxxxxxxx"
# NOTION_DATABASE_ID="xxxxxxxx"
try:
    load_dotenv()
    notion_token = os.getenv("NOTION_API_KEY")
    database_id = os.getenv("NOTION_DATABASE_ID")

    if not notion_token or not database_id:
        print("❌ FAILED: Make sure NOTION_API_KEY and NOTION_DATABASE_ID are in your .env file.")
        exit()

    print("✅ Secrets loaded successfully.")

except ImportError:
    print("❌ FAILED: `python-dotenv` is not installed. Please run `pip install python-dotenv`")
    exit()

# 2. INITIALIZE CLIENT
print("⚡️ Initializing Notion client...")
notion = Client(auth=notion_token)
print("✅ Client initialized.")

# 3. ATTEMPT TO CONNECT AND RETRIEVE DATABASE INFO
print(f"📡 Attempting to connect to database ID: {database_id}...")
try:
    # This is the core of the test. We're asking Notion for info about the database.
    db_info = notion.databases.retrieve(database_id=database_id)

    # If the above line doesn't fail, we have a successful connection.
    db_title = db_info['title'][0]['plain_text']

    print("\n" + "=" * 40)
    print("🏆 SUCCESS! CONNECTION ESTABLISHED!")
    print(f"    Database Title: {db_title}")
    print("    Your credentials and permissions are CORRECT.")
    print("    The problem is not here.")
    print("=" * 40 + "\n")

except Exception as e:
    # If the connection fails for any reason, we print the exact error.
    print("\n" + "=" * 40)
    print("❌ FAILED: COULD NOT CONNECT TO DATABASE.")
    print("\n--- RAW ERROR MESSAGE ---")
    print(e)
    print("\n--- END OF ERROR ---")
    print("\n--- DEBUGGING STEPS ---")
    print("1. Double-check your `NOTION_DATABASE_ID` in the .env file.")
    print("2. Confirm you've shared the database with your integration in Notion.")
    print("3. Ensure your `NOTION_API_KEY` is correct.")
    print("=" * 40 + "\n")
