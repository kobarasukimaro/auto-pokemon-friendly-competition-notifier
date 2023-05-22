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
