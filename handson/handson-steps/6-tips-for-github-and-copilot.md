## この章でやること

GitHub と GitHub Copilot をチームでもっと使いこなすための設定ファイルを、リポジトリに適用して効果を体験します。各 Tips には、そのまま使える設定ファイルの例を載せています。興味のあるものから自由に選んで取り組んでください。チームで分担して取り組み、最後に何を適用したかを共有するのもおすすめです。

| Tips | 適用するファイル | 何がうれしいか |
| ---- | ---- | ---- |
| A | `.github/copilot-instructions.md` | プロジェクトのルールを毎回プロンプトに書かなくて済む |
| B | `.github/instructions/*.instructions.md` | 特定のファイルにだけ適用するルールを書ける |
| C | `AGENTS.md` | Copilot 以外の AI エージェントとも共通の指示を共有できる |
| D | `.github/prompts/*.prompt.md` | よく使うプロンプトをスラッシュコマンドとして呼び出せる |
| E | `.github/agents/*.agent.md` | レビュー専用など、役割を持ったエージェントを作れる |
| F | `.github/skills/*/SKILL.md` | 手順やスクリプトをまとめた「能力」を Copilot に持たせられる |
| G | `.github/CODEOWNERS` とルールセット | 変更内容に応じてレビュアーを自動で割り当て、マージの条件を決められる |
| H | PR テンプレート、Issue テンプレート | PR や Issue に書く内容をそろえられる |
| I | `.github/dependabot.yml` | 依存パッケージやアクションの SHA を自動で最新に保てる |

## 設定ファイルの適用のしかた

どの Tips も、次の流れで設定ファイルを適用します。

1. 第2章と同じように、作業用のブランチを作成します。
1. VS Code のエクスプローラーで、各 Tips に書かれたパスにファイルを作成します。フォルダーがない場合は、ファイル名に `.github/prompts/add-menu-item.prompt.md` のようにパスごと入力すると、フォルダーも一緒に作成されます。
1. 各 Tips の例をコピーして貼り付け、保存します。`<ユーザー名>` のような部分や、ファイル名・コマンドなど自分たちのアプリと違う部分は書き換えます。
1. Copilot Chat の設定ファイル（A〜F）は、保存した時点でローカルの Copilot Chat に反映されます。PR を作る前に効果を試してかまいません。
1. 第2章と同じように **コミット → PR → レビュー → マージ** の流れで、チームのリポジトリに反映します。GitHub 上の機能（cloud agent、Copilot code review、G〜I）は、`main` ブランチにマージされてから有効になります。

## 手順

### A. カスタムインストラクションを適用する

リポジトリ全体に適用されるルールを書いておくと、Copilot Chat、cloud agent、Copilot code review がそのルールに従います。

1. `.github/copilot-instructions.md` を作成し、次の内容を貼り付けます。

    ```markdown
    # カフェ注文シミュレーター

    Python と Streamlit で作る、カフェの注文を体験できる Web アプリです。外部 API やデータベースは使わず、ローカル PC だけで動作します。

    ## 技術スタック

    - Python 3
    - Streamlit（画面）
    - Ruff（静的解析）
    - pytest（テスト）

    ## よく使うコマンド

    - 依存パッケージのインストール: `pip install -r requirements.txt`
    - アプリの起動: `streamlit run app.py`
    - 静的解析: `ruff check .`
    - テスト: `pytest`

    コマンドは、仮想環境（`.venv`）を有効にしてから実行してください。

    ## コーディングのルール

    - 関数の引数と戻り値には型ヒントを付ける
    - 画面に表示する文言、ソースコードのコメントは日本語で書く
    - 金額は整数（円）で扱い、表示するときは `1,000 円` のように3桁区切りにする
    - 新しい依存パッケージを追加したら `requirements.txt` にも追記する

    ## コミュニケーション

    - 回答、コミットメッセージ、PR の説明は日本語で書く
    - コードを変更したら、静的解析とテストを実行して結果を報告する
    ```

1. 「コーディングのルール」に、チームで決めたいルールがあれば追記します。
1. **＋**（新しいチャット）でチャットを開き直し、`#codebase このアプリに新しい画面を追加する場合の手順を教えてください。` と送信します。
1. 回答の下にある **参照** に `copilot-instructions.md` が含まれていること、回答が日本語で、書いたコマンドやルールに沿っていることを確認します。

### B. 特定のファイルにだけ適用するインストラクションを適用する

`applyTo` に書いたパターンに一致するファイルを扱うときだけ、ルールが適用されます。

1. `.github/instructions/tests.instructions.md` を作成し、次の内容を貼り付けます。

    ```markdown
    ---
    description: "テストコードを書くときのルール"
    applyTo: "**/test_*.py,**/*_test.py"
    ---

    # テストコードのルール

    - テストは pytest で書く。unittest は使わない
    - テストファイルは `tests/` フォルダーに `test_<対象のモジュール名>.py` という名前で置く
    - テスト関数の名前は `test_` で始め、何を確認しているかが分かるようにする
    - テスト関数には、何を確認しているかを日本語の docstring で1行書く
    - 1つのテスト関数では、1つの振る舞いだけを確認する
    - 正常系だけでなく、境界値（0 個、空のカートなど）と異常系のテストも書く
    - Streamlit の画面ではなく、計算やデータ処理の関数をテストする
    ```

1. `applyTo` の値を見て、どのファイルに適用されるかを Copilot に説明してもらいます。
1. **＋**（新しいチャット）でチャットを開き直し、`カートの合計金額を計算する処理のテストを書いてください。` と送信します。作成されたテストが、書いたルール（日本語の docstring、境界値のテストなど）に沿っていることを確認します。

### C. AGENTS.md を適用する

`AGENTS.md` は、Copilot だけでなくほかの AI エージェントも読み込む共通の指示ファイルです。

1. リポジトリのルートに `AGENTS.md` を作成し、次の内容を貼り付けます。

    ````markdown
    # AGENTS.md

    ## プロジェクトの概要

    Python と Streamlit で作る「カフェ注文シミュレーター」です。アプリ本体は `app.py` です。

    ## セットアップ

    ```sh
    # Windows（PowerShell）
    python -m venv .venv
    .venv\Scripts\Activate.ps1
    pip install -r requirements.txt

    # macOS
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    ```

    ## 起動

    ```sh
    streamlit run app.py
    ```

    ## 静的解析とテスト

    変更を加えたら、次のコマンドがすべて成功することを確認してください。

    ```sh
    ruff check .
    pytest
    ```

    ## ブランチと PR のルール

    - `main` ブランチに直接コミットしない。作業用のブランチを作成する
    - ブランチ名は `feature/<内容>`、`fix/<内容>` のようにする
    - PR の説明には、関連する Issue の番号と動作確認の内容を書く
    - コミットメッセージと PR の説明は日本語で書く
    ````

1. Copilot Chat で `copilot-instructions.md と AGENTS.md の違いと使い分けを教えてください。` と質問してみます。

`AGENTS.md` を Copilot Chat に読み込ませるには、VS Code の設定 `chat.useAgentsMdFile` が有効になっている必要があります（既定で有効）。

### D. プロンプトファイルでスラッシュコマンドを使う

1. `.github/prompts/add-menu-item.prompt.md` を作成し、次の内容を貼り付けます。

    ```markdown
    ---
    description: "メニューに新しい商品を追加する"
    agent: agent
    ---

    カフェ注文シミュレーターのメニューに、新しい商品を追加してください。

    - 商品名: ${input:name:商品名（例: 抹茶ラテ）}
    - 価格: ${input:price:価格（円）}

    次の手順で作業してください。

    1. #codebase からメニューを定義している場所を探す
    2. 既存の商品と同じ書き方で、新しい商品を追加する
    3. `ruff check .` を実行し、指摘があれば修正する
    4. テストがある場合は `pytest` を実行し、結果を報告する
    5. 変更したファイルと、変更内容を日本語で簡潔に説明する
    ```

1. **＋**（新しいチャット）でチャットを開き直し、入力欄に `/add-menu-item` と入力して送信します。
1. 商品名と価格を聞かれたら答えます。`/add-menu-item name=抹茶ラテ price=480` のように、最初から値を渡すこともできます。
1. Copilot がプロンプトファイルの手順に従って、商品の追加と静的解析を行うことを確認します。

### E. カスタムエージェントを使う

1. `.github/agents/reviewer.agent.md` を作成し、次の内容を貼り付けます。

    ```markdown
    ---
    description: "コードの変更をレビューする専用のエージェント。ファイルの編集やコマンドの実行はしない"
    tools: ['read', 'search']
    ---

    あなたは、このリポジトリのコードレビューを担当するレビュアーです。

    ## ルール

    - ファイルの編集やコマンドの実行は行わず、読み取りと検索だけを行う
    - 修正案は、コードブロックで提示するだけにとどめる
    - 回答は日本語で書く

    ## レビューの観点

    1. バグ: 計算の誤り、想定外の入力（空のカート、0 個など）での不具合
    2. セキュリティ: 入力値の検証漏れ、秘密情報のハードコード
    3. テスト不足: 変更に対してテストが足りているか
    4. 読みやすさ: 名前の付け方、関数の長さ、重複したコード

    ## 出力の形式

    指摘ごとに、次の形式で書いてください。

    - **重要度**: 高・中・低
    - **場所**: ファイル名と行
    - **内容**: 何が問題か
    - **修正案**: どう直すとよいか

    指摘がない場合は、良かった点を1〜2個挙げてください。
    ```

1. チャットのエージェントの選択メニューを開き、**reviewer** が表示されることを確認します。
1. 何かファイルを変更してから、**reviewer** を選び、`#changes 今の変更をレビューしてください。` と送信します。
1. 指摘が重要度付きの形式で返ってくること、ファイルが編集されないことを確認します。

`tools` に書けるツール名は、VS Code のバージョンによって異なることがあります。ファイルを開いたときに警告が表示された場合は、Copilot に修正方法を聞いてみてください。

### F. スキルを使う

スキルは、フォルダー名と frontmatter の `name` を一致させる必要があります。Copilot は `description` を見て、いつこのスキルを使うかを判断します。

1. `.github/skills/run-checks/SKILL.md` を作成し、次の内容を貼り付けます。

    ```markdown
    ---
    name: run-checks
    description: "コードを変更したあとに、Ruff による静的解析と pytest によるテストを実行して結果を報告する。「チェックして」「テストして」「動作確認して」と頼まれたとき、またはコードの変更が終わったときに使う"
    ---

    # 静的解析とテストの実行

    次の手順で、変更したコードをチェックしてください。

    ## 手順

    1. 仮想環境（`.venv`）が有効になっているか確認する。有効になっていなければ、有効にしてから続ける
    2. `ruff check .` を実行する
    3. `pytest` を実行する。テストファイルがない、または pytest がインストールされていない場合は「未実行」として扱う
    4. 失敗したものがあれば、原因を説明する。修正はユーザーに確認してから行う

    ## 報告の形式

    | 項目 | 結果 | 詳細 |
    | ---- | ---- | ---- |
    | 静的解析（Ruff） | 成功・失敗・未実行 | 指摘の件数や内容 |
    | テスト（pytest） | 成功・失敗・未実行 | 成功・失敗したテストの数 |
    ```

1. **＋**（新しいチャット）でチャットを開き直し、`/run-checks` と送信するか、`変更内容をチェックしてください` と依頼します。
1. スキルが使われ、表の形式で結果が報告されることを確認します。

### G. CODEOWNERS とルールセットでレビューのルールを決める

1. `.github/CODEOWNERS` を作成し、次の内容を貼り付けます。`<ユーザー名>` は、チームメンバーの GitHub ユーザー名に置き換えます。

    ```text
    # 後に書いたルールが優先されます

    # すべてのファイルは、チームメンバー全員がコードオーナー
    *           @<ユーザー名1> @<ユーザー名2> @<ユーザー名3>

    # .github/ 配下の設定ファイルは、オーナーがコードオーナー
    /.github/   @<オーナーのユーザー名>
    ```

1. PR を作成してマージします。
1. 以降、新しい PR を作成すると、**Reviewers** にコードオーナーが自動で追加されることを確認します。
1. オーナーは、ブラウザーでリポジトリの **Settings → Rules → Rulesets** を開き、**New ruleset → New branch ruleset** をクリックします。
1. 次のとおり設定し、**Create** をクリックします。
    - **Ruleset Name**: `main`
    - **Enforcement status**: **Active**
    - **Target branches**: **Add target → Include default branch**
    - **Require a pull request before merging** にチェックを入れ、**Required approvals** を `1` にし、**Require review from Code Owners** にチェックを入れる
    - **Automatically request Copilot code review** にチェックを入れる
    - **Require status checks to pass** にチェックを入れ、**Add checks** から第3章で作成した静的解析のジョブを追加する
1. 新しく PR を作成し、Copilot のレビューが自動で依頼されること、Approve とチェックの成功がないとマージできないことを確認します。

private リポジトリでルールセットを使うには、GitHub Pro、GitHub Team などの有料プランが必要です。ルールセットの画面が使えない場合は、CODEOWNERS による自動のレビュアー割り当てだけを確認してください。

### H. PR テンプレートと Issue テンプレートを適用する

1. `.github/pull_request_template.md` を作成し、次の内容を貼り付けます。

    ```markdown
    ## 概要

    <!-- この PR で何をしたかを1〜2行で書いてください -->

    ## 関連 Issue

    <!-- 例: Closes #12 -->

    ## 変更内容

    -

    ## 動作確認

    - [ ] `streamlit run app.py` でアプリが起動し、変更した画面が期待どおりに動く
    - [ ] `ruff check .` が成功する
    - [ ] `pytest` が成功する（テストがある場合）

    ## レビューしてほしい点

    <!-- 特に見てほしい箇所や、迷った点を書いてください -->
    ```

1. `.github/ISSUE_TEMPLATE/feature.yml` を作成し、次の内容を貼り付けます。

    ```yaml
    name: 機能追加
    description: 新しい機能や改善のアイデアを提案します
    title: "[機能追加] "
    labels: ["enhancement"]
    body:
      - type: textarea
        id: summary
        attributes:
          label: 追加したい機能
          description: どのような機能を追加したいかを書いてください
        validations:
          required: true
      - type: textarea
        id: reason
        attributes:
          label: 理由
          description: なぜその機能が必要か、誰がうれしいかを書いてください
      - type: textarea
        id: acceptance
        attributes:
          label: 完了の条件
          description: どうなったら完了とするかを箇条書きで書いてください
          placeholder: |
            - メニューに抹茶ラテが表示される
            - カートに追加すると合計金額に反映される
    ```

1. `.github/ISSUE_TEMPLATE/bug.yml` を作成し、次の内容を貼り付けます。

    ```yaml
    name: バグ報告
    description: アプリの不具合を報告します
    title: "[バグ] "
    labels: ["bug"]
    body:
      - type: textarea
        id: steps
        attributes:
          label: 再現手順
          description: 不具合が起きるまでの操作を順番に書いてください
          placeholder: |
            1. コーヒーをカートに追加する
            2. 注文を確定する
        validations:
          required: true
      - type: textarea
        id: expected
        attributes:
          label: 期待する動作
        validations:
          required: true
      - type: textarea
        id: actual
        attributes:
          label: 実際の動作
          description: エラーメッセージがあれば貼り付けてください
        validations:
          required: true
      - type: dropdown
        id: os
        attributes:
          label: OS
          options:
            - Windows
            - macOS
            - その他
    ```

1. マージ後、ブラウザーで **Issues → New issue** をクリックし、テンプレートを選べるようになっていることを確認します。
1. 新しく PR を作成し、説明欄にテンプレートの内容が自動で入力されることを確認します。

### I. Dependabot で依存関係を最新に保つ

1. `.github/dependabot.yml` を作成し、次の内容を貼り付けます。

    ```yaml
    version: 2
    updates:
      # GitHub Actions のアクション（SHA で固定したものも含む）
      - package-ecosystem: "github-actions"
        directory: "/"
        schedule:
          interval: "weekly"

      # requirements.txt に書いた pip のパッケージ
      - package-ecosystem: "pip"
        directory: "/"
        schedule:
          interval: "weekly"
    ```

1. マージ後、ブラウザーで **Insights → Dependency graph → Dependabot** を開き、設定が読み込まれていることを確認します。アクションを SHA で固定していても、Dependabot が新しいバージョンの SHA に更新する PR を作成してくれます。

## プロンプト例

- カスタムインストラクション、プロンプトファイル、カスタムエージェント、スキルの違いと使い分けを表にしてください。
- `#codebase` このリポジトリのカスタムインストラクションに追記したほうがよいルールを提案してください。
- CODEOWNERS とルールセットを組み合わせると、どのようなことができますか？
- Copilot code review の指摘をチームのルールに合わせるには、どうすればよいですか？
- このリポジトリで、ほかに自動化できそうな作業はありますか？

## 余裕がある方向けの追加ワーク

1. `Ctrl + Shift + P`（macOS は `⌘ + ⇧ + P`）でコマンドパレットを開き、**Chat: Open Customizations** を実行して、適用したカスタマイズの一覧を確認します。
1. 次の機能も調べて、試してみます。
    - GitHub Copilot CLI: ターミナルから Copilot に作業を依頼する
    - MCP サーバー: Copilot から外部のツールやサービスを使えるようにする
    - Copilot のメモリー: 会話をまたいで覚えておいてほしいことを Copilot に記憶させる
    - フック: Copilot の作業の特定のタイミングで、決まったコマンドを必ず実行させる
    - Secret scanning の push protection: パスワードやトークンを誤って push するのを防ぐ
1. 例の設定ファイルを、チームのルールに合わせて Copilot と一緒に書き換えてみます。
1. 個人のリポジトリに戻り、ここで適用したカスタマイズを自分のリポジトリにも取り入れます。

## ふりかえり

1. チームごとに、作ったアプリと、適用したカスタマイズを1〜2分で共有します。
1. Copilot に任せてうまくいったこと、うまくいかなかったことを話し合います。
1. Copilot の提案を採用する前に、どのような観点で確認すべきかをチームでまとめます。
