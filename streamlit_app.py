import streamlit as st
import requests
from urllib.parse import urlencode
import os

# 設定
CLIENT_ID = os.getenv("DISCORD_CLIENT_ID")
CLIENT_SECRET = os.getenv("DISCORD_CLIENT_SECRET")
REDIRECT_URI = os.getenv("DISCORD_REDIRECT_URI")
GUILD_ID = os.getenv("DISCORD_GUILD_ID") # 所属サーバーのID

def get_discord_auth_url():
    params = {
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": "identify guilds"
    }
    return f"https://discord.com/api/oauth2/authorize?{urlencode(params)}"

def exchange_code_for_token(code):
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "scope": "identify guilds"
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    r = requests.post("https://discord.com/api/oauth2/token", data=data, headers=headers)
    return r.json()

def get_user_guilds(access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    r = requests.get("https://discord.com/api/users/@me/guilds", headers=headers)
    return r.json()

if "login" not in st.session_state:
    st.session_state.login = False

if not st.session_state.login:
    st.markdown("[Discordでログイン]("+ get_discord_auth_url() +")")
    code = st.experimental_get_query_params().get("code")
    if code:
        token_res = exchange_code_for_token(code[0])
        access_token = token_res.get("access_token")
        guilds = get_user_guilds(access_token)
        if any(g["id"] == GUILD_ID for g in guilds):
            st.session_state.login = True
            st.session_state.access_token = access_token
            st.experimental_rerun()
        else:
            st.error("指定サーバーに所属していません")
else:
    st.write("ログイン成功！アップロード画面へ進んでください。")
    uploaded_files = st.file_uploader("スクリーンショットをアップロード", accept_multiple_files=True, type=["png","jpg"])
    if uploaded_files:
        st.write(f"{len(uploaded_files)}件のファイルが選択されています。")
        if st.button("処理実行"):
            st.write("処理を開始します...")
            # ここに Google Drive保存 + OCR処理 + Sheets更新 のロジック
            st.success("処理完了!")
