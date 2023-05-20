# このリポジトリについて
仲間大会の情報をツイッター上で自動でお知らせするアプリケーションのソースコードです。インフラコード、アプリケーションコード、CI/CDを含んでいます。
事前準備を行い、このリポジトリ内のワークフローからインフラとアプリケーションをデプロイすると仲間大会の自動ツイートを構築できます。
構築するために以下内容を順番に進めてください。

# このリポジトリの内容でできること
Googleスプレッドシートで管理している仲間大会の情報をAWS Lambdaが自動的に読み取りwitterに投稿します。


# 必要なサービス
- AWS アカウント
- Google スプレッドシート
- Twitter アカウント（要 Developer Portal 登録）

# 構築手順
詳細は各ページに記載します。必ず始めに [common-resources](https://github.com/kobarasukimaro/auto-pokemon-friendly-competition-notifier/tree/main/common-resources) の準備を行ってください