# Preparing for the Friendly Competition Automatic Tweet System
## Create necessary accounts
- [AWS](https://aws.amazon.com/free)
- [GitHub](https://github.com/) 
- [GCP](https://cloud.google.com/)
- [Twitter](https://twitter.com/i/flow/signup)

## Create an app on Twitter Developer Portal
**Perform this step on Twitter.**<br>
To automatically post tweets from a program, you will issue a Consumer key and Access Token on the Twitter Developer Portal. Please refer to [this guide](https://programming-zero.net/twitter-api-process/) for instructions.

Please note the following four pieces of information once they are issued:
- Consumer Key
- Consumer Key Secret
- Access Token
- Access Token Secret

## Create a Google Spreadsheet for the Friendly Competition
It is recommended to make a copy of [this spreadsheet](https://docs.google.com/spreadsheets/d/1u0VbnryJ2T2Zp571SxhDbJM2c63VquqHMRcU5EpiWn8/edit?usp=sharing). The necessary sheets in this spreadsheet are those named in the `YYYYMM` format. For the contents of each column in the sheet, please refer to the `Input Rules` sheet. Sheets in formats other than `YYYYMM` contain master information and aggregation information.

### Check the sheet ID
Since the sheet ID is used to reference the spreadsheet in the program, check the ID of the spreadsheet you created in `Create a Google Spreadsheet for the Friendly Competition`. The URL format of the spreadsheet is `https://docs.google.com/spreadsheets/d/SpreadsheetID/edit`, so please extract the `SpreadsheetID` part and note it.

## Make the Friendly Competition Spreadsheet Accessible from the Program
### Enable Google Sheets API and save service account key
**Perform this step on GCP.**<br>
Enable the Google Sheets API and set up the spreadsheet you created in `Create a Google Spreadsheet for the Friendly Competition`. Please refer to [this guide](https://note.com/npaka/n/nd522e980d995) for instructions. Please save the `service account key` (JSON file) created in the process of enabling the Google Sheets API as it will be used later.

## AWS Setup
**Perform this step on AWS.**
### Create IAM User Access Key
You need to create an access key for the IAM user because the access key is used to deploy applications and other tasks. Please refer to [this guide](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html) for instructions.
> **Warning**
> It's possible to create access keys for root users but it's not recommended.

After creating the access key, note the access key and access token. The permissions for the user haven't been thoroughly tested, so use a policy with stronger permissions like Administrator or PowerUser.

### Register with the Parameter Store
Register information that would be harmful if leaked outside the application in the Parameter Store. Please refer to [this guide](https://docs.aws.amazon.com/systems-manager/latest/userguide/parameter-create-console.html) for registration methods. Please register the following information in the Parameter Store. Note that all should be registered as **Secure String** and use the standard AWS KMS key.
|  Key Name  |  Value  |
| ---- | ---- |
| `/competition-notifier/twitter/consumer-key`  |  `Consumer Key` registered in `Create an app on Twitter Developer Portal`  |
| `/competition-notifier/twitter/consumer-secrets`  |  `Consumer Key Secret` registered in `Create an app on Twitter Developer Portal`  |
| `/competition-notifier/twitter/access-token` |  `Access Token` registered in `Create an app on Twitter Developer Portal`  |
| `/competition-notifier/twitter/consumer-access-token-secrets`  |  `Access Token Secret` registered in `Create an app on Twitter Developer Portal`  |
| `/competition-notifier/google/spread-sheet-key`  |  `SpreadsheetID` checked in `Create a Google Spreadsheet for the Friendly Competition`  |
| `/competition-notifier/google/gcp-key`  |  Contents of `service account key` (JSON file) created in `Make the Friendly Competition Spreadsheet Accessible from the Program`  |

## Prepare GitHub Repository and Run GitHub Actions
**Perform this step on GitHub.**<br>
Fork this repository on your own GitHub account so that you can deploy this system. You can also clone it and create it as a separate repository.

### Prepare for deployment
Deploy this system from GitHub Actions to AWS. Therefore, register the access key and access token created in `AWS Setup` in the [GitHub Actions secrets](https://docs.github.com/actions/security-guides/encrypted-secrets) to allow GitHub Actions to operate AWS.
Register with the following names:

|  Key Name  |  Value  |
| ---- | ---- |
| `AWS_ACCESS_KEY_ID`  |  Access Key created in `AWS Setup`  |
| `AWS_SECRET_ACCESS_KEY`  |  Secret Key created in `AWS Setup`  |

### Run GitHub Actions
Execute GitHub Actions to create common resources. Select `Deploy CloudFormation` from the `Actions` of the repository and run it from `Run workflow`.

If it executes successfully, you're ready to deploy the application!

---

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

## GitHub リポジトリの準備と GitHub Actions の実行
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

### GitHub Actions 実行
GitHub Actions を実行して共通リソースの作成を行ってください。
リポジトリの `Actions` から `Deploy CloudFormation` を選択し、 `Run workflow` から実行してください。

正常に実行が完了すればアプリケーションのデプロイ準備OKです！
