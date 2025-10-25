```markdown
# bnd-discord — Streamlit sample for Discord webhook

このリポジトリは、初めて Streamlit Cloud にデプロイする方向けのサンプルアプリを含みます。アプリは Discord の incoming webhook を使ってメッセージを送信する簡単なデモです。

## ファイル
- app.py — Streamlit アプリ本体
- requirements.txt — 必要なパッケージ
- .streamlit/secrets-example.toml — Secrets の例（実際のシークレットはここに置かない）

## デプロイ手順 (Streamlit Cloud)
1. GitHub にリポジトリを push
2. https://streamlit.io/cloud にアクセスして GitHub アカウントでログイン
3. リポジトリを選択してデプロイ
4. （推奨）Streamlit Cloud の "Secrets" に `DISCORD_WEBHOOK` を設定
   - Key: DISCORD_WEBHOOK
   - Value: https://discord.com/api/webhooks/...
5. アプリを開いてメッセージを送信して確認

## ローカルでの実行
1. Python 仮想環境を作成・有効化
2. pip install -r requirements.txt
3. .streamlit/secrets.toml に `DISCORD_WEBHOOK = "https://discord.com/api/webhooks/..."` を追加（ローカルで試す場合）
4. streamlit run app.py

## 注意点
- Webhook URL は機密情報です。決して公開リポジトリに埋め込まないでください。
- デモ用の簡素な実装です。実運用ではエラーハンドリングやログ、レート制限対策等を追加してください。
```
