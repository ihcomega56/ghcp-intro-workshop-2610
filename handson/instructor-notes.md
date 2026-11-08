# 講師用メモ

受講者向け手順（[handson-steps](handson-steps/)）の各章で、講師が説明すべきポイント、デモの観点、つまずきやすい点をまとめます。見出しの番号と順番は受講者向けの章と同じです。

## 0. 開始前の確認とオープニング

対応する受講者向け資料: [handson/README.md](README.md)、[リポジトリ直下の README](../README.md)

### 事前に確認しておくこと

- 受講者のアカウントで次が使えること。Copilot Business / Enterprise の場合は、Organization または Enterprise のポリシーで有効化が必要です。
    - Copilot cloud agent（リポジトリ作成画面の **Prompt** 欄、Issue への Copilot のアサイン）
    - Copilot code review（PR の Reviewers に Copilot が表示されること）
    - VS Code の Copilot Chat（Ask / Plan / Agent）
- private リポジトリでは、cloud agent と GitHub Actions の実行に Actions の分数を消費します。cloud agent と Copilot code review は、premium request（AI クレジット）も消費します。受講者のプランで足りるか確認しておきます。
- 個人アカウントの private リポジトリでルールセット（第6章 G）を使うには、GitHub Pro などの有料プランが必要です。Free プランの受講者が多い場合は、講師のデモで見せるだけにします。
- 研修用の Organization を使う場合は、受講者がリポジトリを作成できること、外部のメンバーを招待できるかどうかを確認しておきます。

### 時間配分（参考）

全体で約2時間を想定した参考値です。受講者向けの資料には時間を記載していないので、進み具合を見て調整してください。

| 時間 | 章 | 内容 |
| ---- | ---- | ---- |
| 0:00 - 0:05 | 0 | オープニング |
| 0:05 - 0:20 | 1 | リポジトリ作成、cloud agent による雛形作成、VS Code のアップデート、clone |
| 0:20 - 0:50 | 2 | Copilot Chat の基本操作の練習、機能追加の PR とマージ |
| 0:50 - 1:05 | 3 | Actions で静的解析を行うワークフローの作成 |
| 1:05 - 1:20 | 4 | チーム編成、招待、アプリの解析、Issue の作成 |
| 1:20 - 1:45 | 5 | Issue の実装、Copilot のレビュー、マージ |
| 1:45 - 2:00 | 6 | Tips（講師デモ中心）、ふりかえり |

時間が足りないときの調整案:

- 第1章: cloud agent の作業待ちの間に、第2章の「Copilot Chat を開き、モードを確認する」までを先に説明しておく。
- 第2章: 機能追加は小さめのもの（例: デザイン変更）を推奨し、2つ目の PR は追加ワークに回す。
- 第3章: SHA のブラウザーでの照合は1つのアクションだけにする。
- 第5章: 個人で並行実装するとコンフリクトが起きやすいため、時間が厳しい場合はチームで1つの Issue をモブプロで実装する。
- 第6章: A（カスタムインストラクション）と G（CODEOWNERS とルールセット）を講師がデモし、残りは持ち帰りの課題にする。

### オープニングで説明すること

- 今日のゴールは「アプリを作ること」そのものより、**GitHub 上での開発の流れ（Issue → ブランチ → PR → レビュー → マージ）を、Copilot と一緒に回せるようになること**。
- Git のコマンドは覚えなくてよいが、Copilot が実行しようとしているコマンドは**必ず読んでから承認する**。「何をしようとしているか分からないコマンドは承認しない。分からなければ Copilot に聞く」を最初に強調します。
- 完成イメージは `example/` にあるが、ハンズオンでは使わない。
- Git の基本用語に不安がある受講者には [docs/intro-to-git.md](../docs/intro-to-git.md) を案内します。

## 1. リポジトリを作成し、cloud agent でアプリの雛形を作る

対応する受講者向け資料: [1-create-repo-with-cloud-agent.md](handson-steps/1-create-repo-with-cloud-agent.md)

### 説明すること

- **Copilot の3つの使い方**を整理しておくと、以降の章が理解しやすくなります。
    - VS Code などのエディター上の Copilot（第2章以降）: 手元で対話しながら作業する
    - Copilot cloud agent（この章、第5章の追加ワーク）: GitHub 上の環境で自律的に作業し、PR を作る。人はレビューに集中する
    - Copilot code review（第5章）: PR をレビューする
- cloud agent は GitHub Actions 上の一時的な環境で動き、作業内容は PR とセッションログ（**View session**）で確認できること。**PR を作るだけで、勝手に main にマージはしない**こと。
- **テーマを全員共通（カフェ注文シミュレーター）にしている理由**: 第4章でチームのリポジトリを選ぶときに、同じテーマでも作り方や機能がこれだけ違う、という比較ができるため。プロンプトの書き方や追加する機能は自由です。
- private リポジトリにする理由: 研修のコードを公開しないため。第4章で招待したメンバーだけがアクセスできることも体験します。
- cloud agentを使うとPRが作成されます。Ready for mergeのボタン操作が必要です。
- **Squash and merge** の意味: PR 内の複数のコミットを1つにまとめて main に取り込む。main の履歴がシンプルになる。ほかに **Create a merge commit**、**Rebase and merge** があることにも触れます。
- clone は、リモートリポジトリ（GitHub）の内容をローカルにコピーすること。clone はこの章だけ手入力し、以降の Git 操作は Copilot に依頼します。

### つまずきやすい点

- **Prompt 欄が表示されない**: cloud agent が使えないプラン、またはポリシーで無効になっている。代替として、README 付きでリポジトリを作成し、リポジトリの **Agents** タブ（または github.com/copilot の agents）から同じプロンプトで依頼してもらいます。それも難しい場合は、`example/` の内容を参考に講師が用意したファイルを使います。
- **cloud agent の作業が終わらない**: 数分〜10分程度かかることがある。その間に VS Code のアップデートを進めてもらい、**View session** でログを見る時間にします。
- **clone で認証エラー**: VS Code の統合ターミナルでは、VS Code の GitHub 認証が使われます（設定 `git.terminalAuthentication`）。Windows では Git Credential Manager のブラウザー認証が開くこともあります。private リポジトリなので、別アカウントでサインインしていると 404 / 認証エラーになります。
- **`git config user.name` が空**: リポジトリ直下の README の手順は、このリポジトリ内でのみ有効な設定（`--global` なし）なので、新しいリポジトリでは再設定が必要です。
- macOS で VS Code のアップデートが表示されない場合は、メニューの **Code → 更新の確認** から確認できます。

## 2. VS Code の Copilot に慣れ、機能追加の PR を送ってマージする

対応する受講者向け資料: [2-add-feature-with-copilot.md](handson-steps/2-add-feature-with-copilot.md)

### 説明すること

- **Ask / Plan / Agent の違い**: Ask はファイルを変更しない、Plan は計画だけを作る、Agent は編集とコマンド実行まで行う。「まず Ask で理解、Plan で計画、Agent で実装」の流れを推奨します。
- **モデルの選択**: モデルによって速度、得意なこと、消費するリクエスト（AI クレジット）が違う。迷ったら **Auto** でよい。
- **ハーネス**: チャットのタイトルに表示される **Copilot** / **Local** などは、エージェントを動かす実行基盤の違い。`/init`、`/create-agent`、`/create-skill` などは **Local** のエージェントセッションで使えるコマンドで、環境によっては候補に出ないことがある（第6章で使う）。候補に出ない場合は自然言語で依頼すればよいと伝えます。
- **`@workspace` などのチャット参加者は非推奨**になっていること。古い記事で見かけたら、`#codebase` などの `#` 参照で代替できます。
- **`#` でよく使うもの**（入力欄で `#` を入力すると候補が出ます）
    - `#codebase`: ワークスペース全体から関連するコードを探す
    - `#<ファイル名>`、`#<フォルダー名>`: 特定のファイルやフォルダーを渡す
    - `#selection`: エディターで選択している範囲
    - `#terminalLastCommand`: 直前にターミナルで実行したコマンドと出力
    - `#terminalSelection`: ターミナルで選択している範囲
    - `#changes`: ソース管理上の変更（差分）
    - `#problems`: 問題パネルのエラーや警告
    - `#fetch`: Web ページの内容を取得する
    - `#githubRepo`: 別の GitHub リポジトリを検索する
- **スラッシュコマンドの例**: `/explain`、`/fix`、`/tests`、`/doc`（インラインチャット）、`/new`、`/plan`、`/clear`、`/compact`（長い会話を圧縮）、`/help`、`/models`。プロンプトファイルやスキルも `/<名前>` で呼べる（第6章）。
- **VS Code のショートカット・コマンドの例**
    - Copilot Chat を開く: `Ctrl + Alt + I`（macOS: `⌃ + ⌘ + I`）
    - 新しいチャット: チャット上部の **＋** ボタン、または `/clear`
    - エディター / ターミナルのインラインチャット: `Ctrl + I`（macOS: `⌘ + I`）
    - インライン提案の採用 / 却下: `Tab` / `Esc`
    - コマンドパレット: `Ctrl + Shift + P`（macOS: `⌘ + ⇧ + P`）。`Chat: Open Customizations`、`Python: Select Interpreter`、`Git: Clone`、`Developer: Reload Window` などをデモで見せます。
    - ターミナルを開く: `` Ctrl + ` ``
- **仮想環境（venv）を説明させる意図**: Copilot が「説明役」としても使えることを体験させる。プロジェクトごとにパッケージを分けることで、ほかのプロジェクトや PC 全体の Python 環境を汚さないこと、`requirements.txt` で同じ環境を再現できることを補足します。
- **差分の確認（Keep / Undo）とチェックポイント**: Agent の変更は自動保存されることがあるので、差分を見てから **保持** する習慣をつけてもらいます。問題があればチェックポイントから元に戻せます。
- **コマンドの承認**: 承認画面にコマンドがそのまま表示される。特に `git push --force`、`git reset --hard`、`rm` などの破壊的なコマンドは承認しないよう伝えます。「Allow all」系の設定は便利だが研修中は使わない。
- **サンプルプロンプトの意図**: 「複雑にして」「ファイルを分けて」とは書いていないが、「データはプログラムと分けて管理」「別画面を用意」「設定で変更できる」「テストを書く」といった**仕様**を伝えた結果、`pages/`、データファイル、設定ファイル、テストなどに自然に分かれる。良いプロンプトは「作り方」より「満たしたい仕様と確認方法」を書く、という点を説明します。
- PR を Copilot に作らせるには、GitHub を操作するツール（Copilot ハーネスに組み込みの GitHub ツール、または GitHub MCP サーバー）が必要です。使えない場合のフォールバックとして、push 後にブラウザーに表示される **Compare & pull request** を案内しています。PR 説明欄の Copilot アイコンで説明文を生成できることもデモします。

### つまずきやすい点

- **Windows で `Activate.ps1` が実行できない**: 実行ポリシーが原因。`Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` を実行するか、Copilot に聞いてもらう（それ自体が練習になる）。
- **`python` と `python3` の違い**: Windows は `python`、macOS は `python3` が基本。
- **仮想環境が有効になっていない**: プロンプトの先頭に `(.venv)` が出ているか確認。VS Code の右下に表示される Python インタープリターが `.venv` になっているかも確認します。
- **`.venv` がコミットされそうになる**: `.gitignore` に `.venv` がない場合に起こる。プロンプトで確認を依頼しているが、`git add` の対象をよく見るよう伝えます。
- **ポート 8501 が使用中**: 以前起動したアプリが残っている。ターミナルで `Ctrl + C` するか、Streamlit が自動で別ポート（8502 など）を使うので、表示された URL を開きます。

## 3. GitHub Actions で静的解析を行う

対応する受講者向け資料: [3-static-analysis-with-actions.md](handson-steps/3-static-analysis-with-actions.md)

### 説明すること

- **GitHub Actions とは**: リポジトリへの push や PR などのイベントをきっかけに、決められた処理を自動で実行する仕組み。`.github/workflows/` の YAML で定義する。
- **静的解析とは**: プログラムを実行せずにコードを解析し、バグの可能性や書き方の問題を見つけること。Ruff は Rust 製の高速な Python 向け linter / formatter（OSS）。
- **サードパーティのアクションを使わない理由**: アクションはリポジトリのコードやトークンにアクセスできる。中身を確認していないアクションを使うと、サプライチェーン攻撃のリスクがある。
- **SHA で固定する理由**: タグ（`v7`）は後から別のコミットを指すように付け替えられる。SHA はコミットそのものを指すので、知らないうちに中身が変わることがない。行末にバージョンのコメントを書くのは、人が読んで分かるようにするため。Dependabot はこのコメントも含めて更新してくれる（第6章 I）。
- **Copilot に SHA を推測させない**: AI は SHA のような値をもっともらしく「作って」しまうことがある。プロンプトで `git ls-remote` などで実際に取得させ、さらにブラウザーで照合する、という**検証の習慣**を強調します。
- `permissions: contents: read` は、ワークフローに渡されるトークンの権限を最小にする設定（最小権限の原則）。
- **Settings → Actions → General** で、許可するアクションを制限したり、SHA での固定を必須にしたりできる（追加ワーク）。Organization / Enterprise 単位でも設定できます。

### 参考: 講師用の完成例

2026年11月8日時点の最新リリースの SHA です。受講者の環境で生成されたものと見比べる用途にとどめ、受講者には配布しません。実施日に `git ls-remote https://github.com/actions/checkout refs/tags/<タグ>` などで最新の値を確認してください。

```yaml
name: Lint

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

permissions:
  contents: read

jobs:
  ruff:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1
        with:
          persist-credentials: false
      - uses: actions/setup-python@6d4fd22b20465ccc0f7354476588e8df7c9ca0e0 # v7.1.0
        with:
          python-version: "3.x"
      - name: Install Ruff
        run: pip install ruff
      - name: Run Ruff
        run: ruff check --output-format=github .
```

- `--output-format=github` を付けると、PR の **Files changed** に指摘が注釈として表示されます。
- 再現性を重視する場合は `pip install ruff==<バージョン>` のようにバージョンも固定するとよい、と補足できます。

### つまずきやすい点

- **SHA が存在しない / ワークフローが `Unable to resolve action` で失敗する**: Copilot が SHA を推測で書いた可能性が高い。ブラウザーでの照合手順をやり直してもらいます。
- **ワークフローが実行されない**: ファイルの場所が `.github/workflows/` 直下でない、拡張子が `.yml` / `.yaml` でない、`on:` のブランチ名が `main` でない、など。
- **ローカルで `ruff` が見つからない**: 仮想環境が有効になっていない。

## 4. チームを組み、アプリを解析して Issue を作る

対応する受講者向け資料: [4-team-setup-and-issues.md](handson-steps/4-team-setup-and-issues.md)

### 説明すること

- **Collaborator の権限**: 個人アカウントの private リポジトリに招待された Collaborator は、書き込み権限を持つ（Settings の変更などはオーナーのみ）。Organization のリポジトリでは、Read / Triage / Write / Maintain / Admin などのロールで細かく制御できる。
- **他人のコードを読むときに Copilot が役立つ**: 同じお題でも、各自のアプリの構成は違っているはず。`#codebase` と Mermaid 図で、短時間で全体像をつかむ体験をしてもらいます。
- **Issue の書き方**: 「背景」「やりたいこと」「完了条件」を書くと、人にも AI にも伝わりやすい。完了条件をチェックリストにすると、PR のレビュー観点にもなる。Issue の大きさは「1つの PR で完結する」程度が目安。
- **Issue は cloud agent への依頼書にもなる**: よく書かれた Issue は、そのまま Copilot にアサインして実装させられる（第5章の追加ワーク）。
- Copilot が Issue を作成するには GitHub を操作するツールが必要です。Copilot ハーネスには GitHub のツールが組み込まれていることが多いですが、使えない場合はコマンドパレットの **MCP: Add Server** から GitHub MCP サーバー（`https://api.githubcopilot.com/mcp/`）を追加する方法をデモするか、ブラウザーで作成するフォールバックを案内します。
- github.com 上の Copilot Chat（画面右上の Copilot アイコン）でも、リポジトリについて質問したり Issue の下書きを作ったりできることを紹介します。

### つまずきやすい点

- **招待メールが届かない**: `https://github.com/<オーナー>/<リポジトリ>/invitations` を直接開いてもらう。GitHub の通知（ベルのアイコン）にも表示されます。
- **自分のリポジトリと同じフォルダー名で clone できない**: 手順どおり、clone 先のフォルダー名（`team-app`）を指定してもらいます。
- **Issue が重複して作られる**: Copilot に同じ依頼を2回送った場合など。不要なものは **Close issue** で閉じます。

## 5. Issue を実装し、Copilot のレビューを受けてマージする

対応する受講者向け資料: [5-implement-issue-and-review.md](handson-steps/5-implement-issue-and-review.md)

### 説明すること

- **ブランチ名に Issue 番号を入れる理由**: どの Issue の作業かが分かる。PR の説明に `Closes #<番号>` を書くと、マージ時に Issue が自動で閉じる（`Fixes`、`Resolves` も可）。
- **Copilot code review**
    - PR の **Reviewers** から Copilot をリクエストすると、通常は数十秒〜数分でレビューが届く。
    - **レビューに使うモデルや推論レベル（reasoning effort）を選べる**。推論レベルを上げると、より深く検討した指摘が得られる一方、時間とリクエストの消費が増える。小さな PR は標準、ロジックが複雑な PR は高めにする、といった使い分けを紹介します。
    - Copilot のレビューは「Approve」や「Request changes」ではなく、常に **Comment** として届く。マージの判断は人が行う。
    - 指摘は鵜呑みにせず、妥当かどうかを人が判断する。対応しない場合は理由を返信して Resolve する。
    - `.github/copilot-instructions.md` や `.github/instructions/*.instructions.md` の内容がレビューにも反映される（第6章 A、B）。
    - ルールセットで、すべての PR に Copilot のレビューを自動で依頼できる（第6章 G）。
    - **Fix with Copilot** で、レビュー指摘の修正を cloud agent に任せられる。
- **Actions のチェック**: PR を作成したときと、push するたびに実行される。チェックが失敗したまま main にマージしないことを、ルールセットで強制できる（第6章 G）。
- **人のレビュー**: **Comment** / **Approve** / **Request changes** の違い。行へのコメント、suggestion（修正案）の書き方をデモします。
- **コンフリクト（受講者向けの資料には記載していないので、口頭で必ず言及する）**: 第5章で複数人が並行して PR を出すと、同じファイルの同じ箇所を変更してコンフリクトが起きることがある。PR に「This branch has conflicts that must be resolved」と表示される。今回は対応手順まではやらないが、「起きうること」「Copilot に両方の変更の意図を説明させてから解消させる方法がある」「PR 画面の **Update branch** で main を取り込める」ことを伝えます。実際に起きた受講者がいた場合は、講師がフォローします。
- **ペアプロ・モブプロで Copilot を使うコツ**: ドライバー（操作する人）とナビゲーター（プロンプトや確認観点を考える人）に分かれる。プロンプトをチームで考えると、良いプロンプトの書き方が共有されやすい。

### つまずきやすい点

- **Reviewers に Copilot が出てこない**: ライセンスやポリシーで Copilot code review が有効になっていない。講師の画面でデモします。
- **Copilot が PR のレビューコメントを読めない**: GitHub を操作するツールがない場合。コメントをコピーしてチャットに貼り付けてもらいます。
- **マージできない**: チェックが失敗している、コンフリクトがある、（ルールセットがある場合）Approve が足りない、など。PR 下部のメッセージを読んでもらいます。
- **Issue を Copilot にアサインできない**: cloud agent が使えないプラン、またはポリシーで無効になっている。

## 6. GitHub と GitHub Copilot を使いこなすための Tips

対応する受講者向け資料: [6-tips-for-github-and-copilot.md](handson-steps/6-tips-for-github-and-copilot.md)

### 説明すること

- **カスタマイズの全体像**（どれも「毎回プロンプトに書いていたことを、ファイルに書いて共有する」仕組み）

    | 種類 | 場所 | いつ使われるか |
    | ---- | ---- | ---- |
    | カスタムインストラクション | `.github/copilot-instructions.md` | 常に自動で適用。Chat、cloud agent、code review で使われる |
    | パス別インストラクション | `.github/instructions/*.instructions.md` | `applyTo` に一致するファイルを扱うときに自動で適用 |
    | AGENTS.md | リポジトリのルートなど | Copilot を含む複数の AI エージェントで共通の指示 |
    | プロンプトファイル | `.github/prompts/*.prompt.md` | `/<名前>` で呼び出したとき |
    | カスタムエージェント | `.github/agents/*.agent.md` | エージェントの選択メニューで選んだとき。使えるツールを制限できる |
    | スキル | `.github/skills/<名前>/SKILL.md` | 内容に関連する依頼のときに自動で、または `/<名前>` で。スクリプトなどを同梱できる |
    | フック | `.github/hooks/` など | エージェントの作業の決まったタイミングで、コマンドを確実に実行する |
    | MCP サーバー | `.vscode/mcp.json` など | 外部のツールやサービスを Copilot から使う |

- **インストラクションは短く具体的に**: 長すぎるとコンテキストを圧迫し、守られにくくなる。コードを読めば分かることより、「AI が推測できないルール」（テストのコマンド、禁止事項、命名規則など）を書く。
- **スキルとインストラクションの違い**: インストラクションは常に読み込まれるルール、スキルは必要なときだけ読み込まれる手順書（スクリプトや例も含められる）。スキルは Agent Skills というオープンな標準で、Copilot CLI など ほかのツールでも使える。
- **`/init`、`/create-agent`、`/create-skill`、`/create-prompt`、`/create-instructions`** で、それぞれのひな形を Copilot に作らせられる（Local のエージェントセッションで利用可能）。コマンドパレットの **Chat: Open Customizations** で、作成したカスタマイズを一覧・管理できる。
- **CODEOWNERS**: ファイルのパターンごとに、レビューを担当する人やチームを決める。PR を作ると自動でレビュアーに追加される。ルールセットの **Require review from Code Owners** と組み合わせると、コードオーナーの Approve がないとマージできなくなる。CODEOWNERS 自体を `.github/` に置き、変更をオーナーに限定するのが定番。
- **ルールセット**: main への直接 push の禁止、PR の必須化、Approve の数、ステータスチェックの必須化、Copilot の自動レビュー、署名付きコミットの必須化などを設定できる。従来のブランチ保護ルールより柔軟で、Organization 単位で一括適用もできる。
- **PR / Issue テンプレート**: 書く内容をそろえるだけでなく、AI にとっても読みやすい情報になる。Issue フォーム（YAML）を使うと入力項目を必須にできる。
- **Dependabot**: `github-actions` を対象にすると、SHA で固定したアクションも新しいバージョンの SHA に更新する PR を作ってくれる。第3章の「SHA で固定すると更新が大変では？」という疑問への答えになる。
- **その他に紹介できる機能**
    - GitHub Copilot CLI: ターミナルで Copilot に作業を依頼できる。
    - VS Code の Agents ウィンドウ: 複数のエージェントのセッションを並行して管理できる。
    - Copilot のメモリー: 会話をまたいで覚えておいてほしいことを記憶させる。
    - Secret scanning と push protection: パスワードやトークンを誤って push するのを防ぐ。
    - Code scanning（CodeQL）: GitHub 公式の静的解析によるセキュリティチェック。
    - GitHub Projects: Issue や PR をカンバンで管理する。
    - Copilot coding agent 用の環境設定（`.github/workflows/copilot-setup-steps.yml`）: cloud agent の作業環境に、あらかじめツールや依存パッケージを入れておける。

### つまずきやすい点

- **`/init` などが候補に出ない**: ハーネスが Local でない、または VS Code のバージョンが古い。自然言語で依頼すれば同じものを作れます。
- **カスタマイズが効いていないように見える**: チャットを開き直していない、ファイルの場所や拡張子が違う、`applyTo` のパターンが一致していない、など。回答の **参照** に表示されるファイルを確認してもらいます。
- **ルールセットの画面が表示されない / 設定が効かない**: 個人アカウントの Free プランの private リポジトリでは利用できません。
- **CODEOWNERS のユーザーが無効と表示される**: 書き込み権限のないユーザーや、存在しないユーザー名を指定している。リポジトリの **Code** タブで CODEOWNERS ファイルを開くと、エラーが表示されます。

## まとめ・ふりかえりで伝えること

- Copilot は「書く」だけでなく、**読む（解析）、説明する、計画する、レビューする、Git や GitHub を操作する**ところまで手伝ってくれる。
- 一方で、**最終的な判断と責任は人にある**。コマンドの承認、差分の確認、SHA の照合、レビュー指摘の取捨選択は、人が行う。
- チームで使うときは、**ルールをファイル（インストラクション、CODEOWNERS、ルールセット、テンプレート）にして共有する**と、人も AI も同じルールで動ける。
