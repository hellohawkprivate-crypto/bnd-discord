"""Streamlit アプリ — Discord incoming webhook デモ

使い方（簡単）:
- Streamlit Cloud にデプロイする場合は、Secrets に DISCORD_WEBHOOK を設定してください。
  （Key: DISCORD_WEBHOOK, Value: https://discord.com/api/webhooks/...）
- ローカルで試す場合は .streamlit/secrets.toml に DISCORD_WEBHOOK を設定するか、
  アプリの入力欄に webhook URL を直接貼り付けてください。
"""
import streamlit as st
import requests

st.set_page_config(page_title="Discord webhook demo", page_icon=":speech_balloon:")

st.title("Discord Webhook demo — Streamlit")
st.write("このサンプルは、Discord の incoming webhook にメッセージを送る簡単なデモです。")

# Streamlit secrets から取得（Cloud またはローカルの .streamlit/secrets.toml）
webhook_from_secrets = None
try:
    # st.secrets は dict ライクなので get を使える
    webhook_from_secrets = st.secrets.get("DISCORD_WEBHOOK") if hasattr(st, "secrets") else None
except Exception:
    webhook_from_secrets = None

webhook = webhook_from_secrets or st.text_input("Discord incoming webhook URL", placeholder="https://discord.com/api/webhooks/...")

st.markdown("**設定メモ**: Streamlit Cloud の Secrets に `DISCORD_WEBHOOK` を追加することを推奨します。公開リポジトリに webhook を置かないでください。")
st.markdown("---")

with st.form("message_form"):
    username = st.text_input("送信するユーザー名 (任意)", value="Streamlit Bot")
    avatar_url = st.text_input("アバター画像の URL (任意)", value="")
    content = st.text_area("メッセージ本文", value="こんにちは！Streamlit からのテストメッセージです。", height=140)
    send_button = st.form_submit_button("送信する")

if send_button:
    if not webhook:
        st.error("Webhook URL が指定されていません。Streamlit Secrets に DISCORD_WEBHOOK を設定するか、上の入力欄に webhook URL を貼ってください。")
    else:
        payload = {"content": content}
        if username:
            payload["username"] = username
        if avatar_url:
            payload["avatar_url"] = avatar_url

        try:
            res = requests.post(webhook, json=payload, timeout=10)
            # Discord incoming webhook は成功時に 204 を返すことが多いです
            if res.status_code in (200, 204):
                st.success("送信に成功しました！")
                st.write("ステータスコード:", res.status_code)
            else:
                st.error(f"送信に失敗しました。ステータスコード: {res.status_code}")
                st.write("レスポンスボディ:", res.text)
        except Exception as e:
            st.error(f"エラーが発生しました: {e}")

st.markdown("---")
st.subheader("デプロイ手順（簡易）")
st.write(
    "1. このリポジトリを GitHub に push\n"
    "2. https://streamlit.io/cloud にアクセスして GitHub アカウントでログイン\n"
    "3. リポジトリを選択してデプロイ\n"
    "4. （推奨）Streamlit Cloud の `Secrets` に `DISCORD_WEBHOOK` を設定\n"
    "5. アプリを開いてメッセージを送信して確認"
)
st.info("注意: Webhook URL は機密情報です。公開リポジトリに直接書き込まないでください。")
