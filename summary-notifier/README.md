# About summary-notifier

## The role of this feature
This feature periodically tweets a list of friendly competitions, complete with images. There are two types: once a day about the competitions being held that day, and on Mondays and Thursdays about the most upcoming competitions. The content is as follows:

![Screenshot 2023-05-20 20 02 33](https://github.com/kobarasukimaro/auto-pokemon-friendly-competition-notifier/assets/17419944/b6b338e1-f682-4fce-ad98-be543aa9bde6)

## Mechanism
It regularly executes Lambda via EventBridge. Inside the Lambda, it tweets using the Twitter token set [here](https://github.com/kobarasukimaro/auto-pokemon-friendly-competition-notifier/blob/main/common-resources/README.md#register-with-the-parameter-store). Information about the friendly competitions is obtained from a Google Spreadsheet.

Here is something I brought over from a previous note:
![image](https://github.com/kobarasukimaro/auto-pokemon-friendly-competition-notifier/assets/17419944/67654962-0537-4dfd-8c56-9c0447fe2285)

## Code Configuration

## CI/CD
### Deployment
When modifying the program or schedule and applying those changes, please use GitHub Actions.
To execute the workflow, select `Run workflow` from [Deploy summary notice tweet](https://github.com/kobarasukimaro/auto-pokemon-friendly-competition-notifier/actions/workflows/deploy_summary_notice_tweet.yml), and choose the branch you wish to deploy.

### Removal
If you wish to remove the summary-notifier, please use GitHub Actions.
To execute the workflow, select `Run workflow` from [Remove summary notice tweet](https://github.com/kobarasukimaro/auto-pokemon-friendly-competition-notifier/actions/workflows/remove_summary_notice_tweet.yml), choose the branch you wish to deploy, and select `yes` for `remove ok?`.


---

# summary-notifier について

## この機能の役割
定期的に仲間大会一覧を画像付きですツイートします。
1日1回その日行われる大会について、月曜と木曜に直近で開かれる大会についての2種類あります。
以下のような内容です。

![スクリーンショット 2023-05-20 20 02 33](https://github.com/kobarasukimaro/auto-pokemon-friendly-competition-notifier/assets/17419944/b6b338e1-f682-4fce-ad98-be543aa9bde6)




## 仕組み
EventBridgeで定期的にLambdaを実行します。Lambdaの中では[こちら](https://github.com/kobarasukimaro/auto-pokemon-friendly-competition-notifier/blob/main/common-resources/README.md#register-with-the-parameter-store) で設定したTwitterのトークンを使用してツイートします。
仲間大会の情報はGoogleスプレッドシートから取得します。

以前noteに貼ったものを持ってきました

![image](https://github.com/kobarasukimaro/auto-pokemon-friendly-competition-notifier/assets/17419944/67654962-0537-4dfd-8c56-9c0447fe2285)


## コードの構成

## CI/CD
### デプロイ
プログラムやスケジュールを修正し、それを反映する場合は GitHub Actions を使用してください。
[Deploy summary notice tweet](https://github.com/kobarasukimaro/auto-pokemon-friendly-competition-notifier/actions/workflows/deploy_summary_notice_tweet.yml)から `Run workflow` を選択し、デプロイ対象のブランチを選択してワークフローを実行してください。

### 削除
competition-notifier を削除する場合は GitHub Actions を使用してください。
[Remove summary notice tweet](https://github.com/kobarasukimaro/auto-pokemon-friendly-competition-notifier/actions/workflows/remove_summary_notice_tweet.yml)から `Run workflow` を選択し、 デプロイ対象のブランチを選択して `remove ok?` で `yes` を選択してワークフローを実行してください。
