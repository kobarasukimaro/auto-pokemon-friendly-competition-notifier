---
# About competition-notifier

## The role of this feature
This feature periodically tweets (once every hour) about individual friendly competitions. The content is as follows:

![Screenshot 2023-05-20 20 01 57](https://github.com/kobarasukimaro/auto-pokemon-friendly-competition-notifier/assets/17419944/b0e6fcaf-ca98-4a96-92fa-0a713e29f542)

## Mechanism
It regularly executes Lambda via EventBridge. Inside the Lambda, it tweets using the Twitter token set [here](https://github.com/kobarasukimaro/auto-pokemon-friendly-competition-notifier/blob/main/common-resources/README.md#register-with-the-parameter-store). Information about the friendly competitions is obtained from a Google Spreadsheet, and the state is saved in DynamoDB.

Here is something I brought over from a previous note:
![image](https://github.com/kobarasukimaro/auto-pokemon-friendly-competition-notifier/assets/17419944/04fcd5a0-0c41-45a9-b982-ce91ffb07302)

## Code Configuration

## CI/CD
### Deployment
When modifying the program or schedule and applying those changes, please use GitHub Actions.
To execute the workflow, select `Run workflow` from [Deploy competition notice tweet](https://github.com/kobarasukimaro/auto-pokemon-friendly-competition-notifier/actions/workflows/deploy_competition_notice_tweet.yml), and choose the branch you wish to deploy.

### Removal
If you wish to remove the competition-notifier, please use GitHub Actions.
To execute the workflow, select `Run workflow` from [Remove competition notice tweet](https://github.com/kobarasukimaro/auto-pokemon-friendly-competition-notifier/actions/workflows/remove_competition_notice_tweet.yml), choose the branch you wish to deploy, and select `yes` for `remove ok?`.

---

# competition-notifier について

## この機能の役割
定期的（1時間に1回）に個々の仲間大会についてツイートします。
以下のような内容です。

![スクリーンショット 2023-05-20 20 01 57](https://github.com/kobarasukimaro/auto-pokemon-friendly-competition-notifier/assets/17419944/b0e6fcaf-ca98-4a96-92fa-0a713e29f542)



## 仕組み
EventBridgeで定期的にLambdaを実行します。Lambdaの中では[こちら](https://github.com/kobarasukimaro/auto-pokemon-friendly-competition-notifier/blob/main/common-resources/README.md#register-with-the-parameter-store) で設定したTwitterのトークンを使用してツイートします。
仲間大会の情報はGoogleスプレッドシートから取得し、状態を DynamoDB に保存します。

以前noteに貼ったものを持ってきました
![image](https://github.com/kobarasukimaro/auto-pokemon-friendly-competition-notifier/assets/17419944/04fcd5a0-0c41-45a9-b982-ce91ffb07302)

## コードの構成

## CI/CD
### デプロイ
プログラムやスケジュールを修正し、それを反映する場合は GitHub Actions を使用してください。
[Deploy competition notice tweet](https://github.com/kobarasukimaro/auto-pokemon-friendly-competition-notifier/actions/workflows/deploy_competition_notice_tweet.yml)から `Run workflow` を選択し、デプロイ対象のブランチを選択してワークフローを実行してください。

### 削除
competition-notifier を削除する場合は GitHub Actions を使用してください。
[Remove competition notice tweet](https://github.com/kobarasukimaro/auto-pokemon-friendly-competition-notifier/actions/workflows/remove_competition_notice_tweet.yml)から `Run workflow` を選択し、 デプロイ対象のブランチを選択して `remove ok?` で `yes` を選択してワークフローを実行してください。
