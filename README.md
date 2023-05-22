# About this repository
This is the source code of an application that automatically announces information about the Friendly Competition on Twitter. It includes infrastructure code, application code, and CI/CD. By preparing in advance and deploying the infrastructure and application from the workflows in this repository, you can build an automatic tweet for the Friendly Competition. Please proceed in order with the following contents to build it.

# What you can do with this repository
AWS Lambda automatically reads information about the Friendly Competition managed on Google Spreadsheet and posts it on Twitter. The tweets will look like this:

![スクリーンショット 2023-05-20 20 01 57](https://github.com/kobarasukimaro/auto-pokemon-friendly-competition-notifier/assets/17419944/a91d4b00-6da6-4868-899a-6b0d8bea30ea)

![スクリーンショット 2023-05-20 20 02 33](https://github.com/kobarasukimaro/auto-pokemon-friendly-competition-notifier/assets/17419944/95103dbe-6c05-43aa-ba78-2cba16a22514)


# Required services
- AWS account
- GCP account
- Twitter account (requires registration on Developer Portal)
- GitHub account

> **Warning**
> Please prepare and manage each account by yourself. We cannot take responsibility for any damage or costs incurred due to security leaks.

# Build instructions
Details will be posted on each page. Be sure to start by preparing the [common-resources](https://github.com/kobarasukimaro/auto-pokemon-friendly-competition-notifier/tree/main/common-resources).

- Build [common-resources](https://github.com/kobarasukimaro/auto-pokemon-friendly-competition-notifier/tree/main/common-resources)

Below are the functions to be tweeted. Please build only what you need for each.

- Build [general-notifier](https://github.com/kobarasukimaro/auto-pokemon-friendly-competition-notifier/tree/main/general-notifier)
- Build [competition-notifier](https://github.com/kobarasukimaro/auto-pokemon-friendly-competition-notifier/tree/main/competition-notifier)
- Build [summary-notifier](https://github.com/kobarasukimaro/auto-pokemon-friendly-competition-notifier/tree/main/summary-notifier)


---


# このリポジトリについて
仲間大会の情報をツイッター上で自動でお知らせするアプリケーションのソースコードです。インフラコード、アプリケーションコード、CI/CDを含んでいます。
事前準備を行い、このリポジトリ内のワークフローからインフラとアプリケーションをデプロイすると仲間大会の自動ツイートを構築できます。
構築するために以下内容を順番に進めてください。

# このリポジトリの内容でできること
Googleスプレッドシートで管理している仲間大会の情報をAWS Lambdaが自動的に読み取りwitterに投稿します。
以下のようなツイートとなります。

![スクリーンショット 2023-05-20 20 01 57](https://github.com/kobarasukimaro/auto-pokemon-friendly-competition-notifier/assets/17419944/a91d4b00-6da6-4868-899a-6b0d8bea30ea)

![スクリーンショット 2023-05-20 20 02 33](https://github.com/kobarasukimaro/auto-pokemon-friendly-competition-notifier/assets/17419944/95103dbe-6c05-43aa-ba78-2cba16a22514)


# 必要なサービス
- AWS アカウント
- GCP アカウント
- Twitter アカウント（要 Developer Portal 登録）
- GitHub アカウント

> **Warning**
> 各アカウントはご自身でご準備し、ご自身で管理をお願いします。セキュリティ漏洩による損害や発生したコストについて責任は負いかねます。

# 構築手順
詳細は各ページに記載します。
必ず始めに [common-resources](https://github.com/kobarasukimaro/auto-pokemon-friendly-competition-notifier/tree/main/common-resources) の準備を行ってください

- [common-resources](https://github.com/kobarasukimaro/auto-pokemon-friendly-competition-notifier/tree/main/common-resources) の構築

以下はツイートする機能になります。それぞれ必要なものだけ構築してください。

- [general-notifier](https://github.com/kobarasukimaro/auto-pokemon-friendly-competition-notifier/tree/main/general-notifier) の構築
- [competition-notifier](https://github.com/kobarasukimaro/auto-pokemon-friendly-competition-notifier/tree/main/competition-notifier) の構築
- [summary-notifier](https://github.com/kobarasukimaro/auto-pokemon-friendly-competition-notifier/tree/main/summary-notifier) の構築
