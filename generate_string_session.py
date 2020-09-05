from pyrogram import Client

API_KEY = int(input("Masukkan API KEY: "))
API_HASH = input("Masukkan API HASH: ")
with Client(':memory:', api_id=API_KEY, api_hash=API_HASH) as app:
    print(app.export_session_string())