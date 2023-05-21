# 仲間大会自動ツイートシステムの準備
## 必要なアカウントを作成する
- [AWS](https://aws.amazon.com/jp/free)
- [GitHub](https://github.co.jp/) 
- [GCP](https://cloud.google.com/?hl=ja)
- [Twitter](https://twitter.com/i/flow/signup)

## Twitter Developer Portal で app を作成する
**この作業は Twitter で行ってください。**<br>
プログラムからツイートを自動的に投稿するために Twitter Developer Portal で Consumer key と Access Token を発行します。
方法については[こちら](https://programming-zero.net/twitter-api-process/)を参考にしてください。

以下の4つの情報を発行できたらメモしてください。
- Consumer Key
- Consumer Key Secret
- Access Token
- Access Token Secret

## Google　スプレッドシートに仲間大会用のスプレッドシートを作成する
[こちら](https://docs.google.com/spreadsheets/d/1u0VbnryJ2T2Zp571SxhDbJM2c63VquqHMRcU5EpiWn8/edit?usp=sharing)のスプレッドシートのコピーを推奨します。
このスプレッドシートの中で必要なシートは、名前が `YYYYMM` 形式のシートとなります。また、シートの各列の入力内容については `入力ルール` シートをご参照ください。
`YYYYMM` 形式のシート以外はマスター情報や集計情報のシートとなります。

### シートIDの確認
プログラム上でスプレッドシートを参照する際にシートIDを使用しているため、 `Google　スプレッドシートに仲間大会用のスプレッドシートを作成する` で作成したスプレッドシートのIDを確認します。
スプレッドシートのURLの形式は `https://docs.google.com/spreadsheets/d/スプレッドシートID/edit` となっているため、 `スプレッドシートID` 部分を抽出してメモしてください。

## 仲間大会スプレッドシートにプログラムからアクセスできるようにする
### Google Sheets API の有効化とサービスアカウントキーの保存
**この作業は GCP で行ってください。**<br>
Google Sheets API を有効にして `Google　スプレッドシートに仲間大会用のスプレッドシートを作成する` で作成したスプレッドシートに設定を行います。
方法は[こちら](https://note.com/npaka/n/nd522e980d995)を参考にしてください。
Google Sheets API を有効にする上で作成した `「サービスアカウントキー」（JSONファイル）` は後ほど使用するのでローカルに保存しておいてください。

## AWS の設定
**この作業は AWS で行ってください。**
### IAMユーザーのアクセスキー作成
アプリケーションなどのデプロイを行うためにアクセスキーを使用しているためIAMユーザーのアクセスキーを作成してください。方法は[こちら](https://docs.aws.amazon.com/ja_jp/IAM/latest/UserGuide/id_credentials_access-keys.html)を参考にしてください。
> **Warning**
> ルートユーザーのアクセスキーも作成可能ですが推奨はしません。

アクセスキーを作成したら、アクセスキーとアクセストークンをメモしてください。
また、ユーザーの権限はあまり検証していないのでポリシーはAdministratorやPowerUserなど強めの権限を使用してください。

### パラメーターストアの登録
アプリケーションで使用する外に漏れるとまずい情報をパラメーターストアに登録します。登録方法は[こちら](https://docs.aws.amazon.com/ja_jp/systems-manager/latest/userguide/parameter-create-console.html)を参考にしてください。
以下の情報をパラメーターストアに登録してください。尚、全て **安全な文字列** で登録し、KMSキーはAWS標準のものを使用してください。
|  キー名  |  値  |
| ---- | ---- |
| `/competition-notifier/twitter/consumer-key`  |  `Twitter Developer Portal で app を作成する` で登録した `Consumer Key`  |
| `/competition-notifier/twitter/consumer-secrets`  |  `Twitter Developer Portal で app を作成する` で登録した `Consumer Key Secret`  |
| `/competition-notifier/twitter/access-token`  |  `Twitter Developer Portal で app を作成する` で登録した `Access Token`  |
| `/competition-notifier/twitter/consumer-access-token-secrets`  |  `Twitter Developer Portal で app を作成する` で登録した `Access Token Secret`  |
| `/competition-notifier/google/spread-sheet-key`  |  `Google　スプレッドシートに仲間大会用のスプレッドシートを作成する` で確認した `スプレッドシートID`  |
| `/competition-notifier/google/gcp-key`  |  `仲間大会スプレッドシートにプログラムからアクセスできるようにする` で作成した `「サービスアカウントキー」（JSONファイル）` の内容  |

## GitHub リポジトリの準備
**この作業は GitHub で行ってください。**<br>
ご自身のGitHubアカウント上でこの仕組みをデプロイできるようにこのリポジトリをforkしてください。
cloneして別リポジトリとして作成する形でも構いません。

### デプロイ準備
この仕組みをGitHub Actions から AWS上にデプロイします。そのため GitHub Actions から AWS の操作を行えるように [GitHub Actions のシークレット](https://docs.github.com/ja/actions/security-guides/encrypted-secrets)に `AWS の設定` で作成したアクセスキーとアクセストークンを登録します。
以下の名前で登録してください。

|  キー名  |  値  |
| ---- | ---- |
| `AWS_ACCESS_KEY_ID`  |  `AWS の設定` で作成したアクセスキー  |
| `AWS_SECRET_ACCESS_KEY`  |   `AWS の設定` で作成したシークレットキー  |
