# GitHub Copilot でアプリをゼロから作り、チーム開発を体験するハンズオン

このハンズオンでは、GitHub Copilot cloud agent と VS Code の GitHub Copilot を使って、Python のアプリをゼロから作ります。アプリのテーマは全員共通で「カフェ注文シミュレーター」です。プロンプトの書き方や追加する機能は自由に決めてかまいません。

前半は個人で、自分のリポジトリにアプリを作り、Pull Request（PR）を送ってマージするまでの流れと、GitHub Actions による静的解析を体験します。後半はチームを組み、Issue の作成、実装、Copilot によるレビュー、マージまでを一緒に進めます。

Git の操作（ブランチ作成、コミット、push、PR 作成など）は、原則として VS Code の GitHub Copilot に自然言語で依頼して行います。コマンドを覚える必要はありませんが、Copilot が実行しようとしているコマンドは必ず確認してから承認してください。

完成イメージは [example](../example/README.md) フォルダーにあります。ハンズオンではこのコードは使わず、自分でゼロから作ります。

## 必要な環境

[リポジトリ直下の README](../README.md) の事前セットアップを済ませてください。

- Visual Studio Code（最新の安定版）
- GitHub Copilot Chat 拡張機能、Python 拡張機能
- Python
- Git
- GitHub アカウント（private リポジトリを作成できること）
- GitHub Copilot のライセンス（cloud agent と Copilot code review が利用可能であること）

## 進め方

各章の手順を見ながら、ブラウザーの GitHub と VS Code の Copilot Chat を行き来して進めます。

1. [リポジトリを作成し、cloud agent でアプリの雛形を作る](handson-steps/1-create-repo-with-cloud-agent.md)
1. [VS Code の Copilot に慣れ、機能追加の PR を送ってマージする](handson-steps/2-add-feature-with-copilot.md)
1. [GitHub Actions で静的解析を行う](handson-steps/3-static-analysis-with-actions.md)
1. [チームを組み、アプリを解析して Issue を作る](handson-steps/4-team-setup-and-issues.md)
1. [Issue を実装し、Copilot のレビューを受けてマージする](handson-steps/5-implement-issue-and-review.md)
1. [GitHub と GitHub Copilot を使いこなすための Tips](handson-steps/6-tips-for-github-and-copilot.md)

講師向けの説明メモは [instructor-notes.md](instructor-notes.md) にまとめています。

## ゴール

- GitHub Copilot cloud agent にアプリの雛形を作らせ、その PR をレビューしてマージできる
- VS Code の Copilot Chat で、Ask、Plan、Agent を使い分けられる
- `#` によるコンテキスト指定とスラッシュコマンドを使い、コードやターミナルの情報を Copilot に解析させられる
- Git の操作を Copilot に依頼し、実行されるコマンドを確認してから承認できる
- 自分で PR を作成し、ブラウザーの GitHub でマージできる
- GitHub 公式アクションと OSS ツールだけを使い、SHA でバージョンを固定した Actions ワークフローを作れる
- private リポジトリにメンバーを招待し、Issue と PR を使ってチームで開発できる
- PR に Copilot をレビュアーとしてアサインし、レビュー結果と Actions のチェック結果を確認できる
- カスタムインストラクションや CODEOWNERS など、GitHub と Copilot をチームで使いこなすための仕組みを知る
