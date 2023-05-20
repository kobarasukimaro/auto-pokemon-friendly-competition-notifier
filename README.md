# このリポジトリについて
仲間大会の情報をツイッター上で自動でお知らせするアプリケーションのソースコードです。インフラコード、アプリケーションコード、CI/CDを含んでいます。
事前準備を行い、このリポジトリ内のワークフローからインフラとアプリケーションをデプロイすると仲間大会の自動ツイートを構築できます。
構築するために以下内容を順番に進めてください。

# このリポジトリの内容でできること
Googleスプレッドシートで管理している仲間大会の情報をAWS Lambdaが自動的に読み取りwitterに投稿します。
![スクリーンショット 2023-05-20 20 01 57](https://github.com/kobarasukimaro/auto-pokemon-friendly-competition-notifier/assets/17419944/a91d4b00-6da6-4868-899a-6b0d8bea30ea)

![スクリーンショット 2023-05-20 20 02 33](https://github.com/kobarasukimaro/auto-pokemon-friendly-competition-notifier/assets/17419944/95103dbe-6c05-43aa-ba78-2cba16a22514)


# 必要なサービス
- AWS アカウント
- Google スプレッドシート
- Twitter アカウント（要 Developer Portal 登録）
- GitHub アカウント

> **Warning**
> 各アカウントはご自身でご準備し、ご自身で管理をお願いします。セキュリティ漏洩による損害や発生したコストについて責任は負いかねます。

# 構築手順
詳細は各ページに記載します。
必ず始めに [common-resources](https://github.com/kobarasukimaro/auto-pokemon-friendly-competition-notifier/tree/main/common-resources) の準備を行ってください

- [common-resources](https://github.com/kobarasukimaro/auto-pokemon-friendly-competition-notifier/tree/main/common-resources) の構築
- [general-notifier](https://github.com/kobarasukimaro/auto-pokemon-friendly-competition-notifier/tree/main/general-notifier) の構築
- [competition-notifier](https://github.com/kobarasukimaro/auto-pokemon-friendly-competition-notifier/tree/main/competition-notifier) の構築
- [summary-notifier](https://github.com/kobarasukimaro/auto-pokemon-friendly-competition-notifier/tree/main/summary-notifier) の構築
