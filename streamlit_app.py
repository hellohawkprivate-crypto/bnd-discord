import streamlit as st
import requests
from urllib.parse import urlencode
import os

# 設定
CLIENT_ID = os.getenv("DISCORD_CLIENT_ID")
CLIENT_SECRET = os.getenv("DISCORD_CLIENT_SECRET")
REDIRECT_URI = os.getenv("DISCORD_REDIRECT_URI")
GUILD_ID = os.getenv("DISCORD_GUILD_ID")  # 所属サーバーのID

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
    st.write("🔍 Discordからの応答ステータス:", r.status_code)
    st.write("🔍 Discordからの応答テキスト:", r.text)
    try:
        return r.json()  # JSONとして返す
    except Exception:
        st.error(f"Discordから予期しない応答: {r.text}")
        return {}
    return data

def get_user_guilds(access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    r = requests.get("https://discord.com/api/users/@me/guilds", headers=headers)

    try:
        data = r.json()
    except Exception:
        st.error(f"Discordから予期しない応答を受け取りました: {r.text}")
        return []

    # Discord APIがエラーを返した場合
    if isinstance(data, dict) and data.get("message"):
        st.error(f"Discordエラー: {data.get('message')}")
        return []

    # dataがリストでない場合も防御
    if not isinstance(data, list):
        st.error("サーバー情報の形式が不正です。以下が受信内容です：")
        st.json(data)
        return []

    return data

# --- メイン処理 ---
if "login" not in st.session_state:
    st.session_state.login = False

if not st.session_state.login:
    st.markdown("[Discordでログイン](" + get_discord_auth_url() + ")")

    params = st.experimental_get_query_params()
    code = params.get("code", [None])[0] if "code" in params else None

    # st.write("params:", params)

    # ---- codeを一度だけ処理して即座に交換・rerun ----
    if code and "used_code" not in st.session_state:
        st.session_state["used_code"] = True
        token_res = exchange_code_for_token(code)
        st.session_state["token_response"] = token_res
        st.session_state["used_code"] = True
        st.rerun()  # rerunして二重送信を防止
    else:
        token_res = st.session_state.get("token_response", None)

    if token_res:
        access_token = token_res.get("access_token")
        if not access_token:
            st.error("Discordトークンが取得できませんでした。")
            st.json(token_res)
            st.stop()
    
        guilds = get_user_guilds(access_token)
        if any(isinstance(g, dict) and str(g.get("id")) == str(GUILD_ID) for g in guilds):
            st.session_state.login = True
            st.session_state.access_token = access_token
            st.rerun()
        else:
            st.error("指定サーバーに所属していません。")

else:
    st.success("✅ ログイン成功！")
    # uploaded_files = st.file_uploader("スクリーンショットをアップロード", accept_multiple_files=True, type=["png", "jpg"])
    if uploaded_files:
        st.write(f"{len(uploaded_files)}件のファイルが選択されています。")
        if st.button("処理実行"):
            st.write("処理を開始します...")
            # ここに Google Drive保存 + OCR処理 + Sheets更新 のロジック
            st.success("処理完了！")
