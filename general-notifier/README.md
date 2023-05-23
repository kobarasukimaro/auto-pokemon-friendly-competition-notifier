---
# About general-notifier

## The role of this feature
This feature periodically tweets about any content other than information related to friendly competitions. Here are some of the things currently set up.

![Screenshot 2023-05-23 8 37 32](https://github.com/kobarasukimaro/auto-pokemon-friendly-competition-notifier/assets/17419944/9ff2a4f8-cec7-46cf-8c55-95e101a601b7)

## Mechanism
It regularly executes Lambda via EventBridge. Inside the Lambda, it tweets using the Twitter token set [here](https://github.com/kobarasukimaro/auto-pokemon-friendly-competition-notifier/blob/main/common-resources/README.md#register-with-the-parameter-store).

![Friendly Competition drawio](https://github.com/kobarasukimaro/auto-pokemon-friendly-competition-notifier/assets/17419944/7ba945c3-22e8-49c3-b695-04bcb7e4eb0c)

## Code Configuration


### If you want to change the content of the tweet
Please modify the section set to `tweet_contents` around line 37.
Please note that it only posts when it fits within 140 characters, as checked by Twitter regulations.

## CI/CD
### Deployment
When modifying the program or schedule and applying those changes, please use GitHub Actions.
To execute the workflow, select `Run workflow` from [Deploy general notice tweet](https://github.com/kobarasukimaro/auto-pokemon-friendly-competition-notifier/actions/workflows/deploy_general_notice_tweet.yml), and choose the branch you wish to deploy.

### Removal
If you wish to remove the general-notifier, please use GitHub Actions.
To execute the workflow, select `Run workflow` from [Remove general notice tweet](https://github.com/kobarasukimaro/auto-pokemon-friendly-competition-notifier/actions/workflows/remove_general_notice_tweet.yml), choose the branch you wish to deploy, and select `yes` for `remove ok?`.

---

# general-notifier について

## この機能の役割
定期的に仲間大会の情報以外の任意の内容についてツイートします。
現在設定しているのは以下のようなものです。

![スクリーンショット 2023-05-23 8 37 32](https://github.com/kobarasukimaro/auto-pokemon-friendly-competition-notifier/assets/17419944/9ff2a4f8-cec7-46cf-8c55-95e101a601b7)

## 仕組み
EventBridgeで定期的にLambdaを実行します。Lambdaの中では[こちら](https://github.com/kobarasukimaro/auto-pokemon-friendly-competition-notifier/blob/main/common-resources/README.md#register-with-the-parameter-store) で設定したTwitterのトークンを使用してツイートします。

![仲間大会 drawio](https://github.com/kobarasukimaro/auto-pokemon-friendly-competition-notifier/assets/17419944/7ba945c3-22e8-49c3-b695-04bcb7e4eb0c)

## コードの構成


### ツイートの内容を変えたい
37行目あたりの `tweet_contents` に設定している部分を修正してください。
なお、文字数チェックしててTwitter規程で140文字に収まる場合のみに投稿しています。

## CI/CD
### デプロイ
プログラムやスケジュールを修正し、それを反映する場合は GitHub Actions を使用してください。
[Deploy general notice tweet](https://github.com/kobarasukimaro/auto-pokemon-friendly-competition-notifier/actions/workflows/deploy_general_notice_tweet.yml)から `Run workflow` を選択し、デプロイ対象のブランチを選択してワークフローを実行してください。

### 削除
general-notifier を削除する場合は GitHub Actions を使用してください。
[Remove general notice tweet](https://github.com/kobarasukimaro/auto-pokemon-friendly-competition-notifier/actions/workflows/remove_general_notice_tweet.yml)から `Run workflow` を選択し、 デプロイ対象のブランチを選択して `remove ok?` で `yes` を選択してワークフローを実行してください。
