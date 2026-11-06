# VS Code + GitHub Copilot ハンズオン環境セットアップ

このリポジトリは、VS Code と GitHub Copilot を使って、Python の小さな注文アプリを改修するハンズオン用スターターです。アプリは Streamlit で動作し、バックエンドやデータベースの構築は不要です。

## 事前セットアップ

### 1. Visual Studio Code

- [Visual Studio Code](https://code.visualstudio.com/) の最新安定版をインストールします。
- 次の拡張機能をインストールします。
    - 発行元が Microsoft の **Python**
    - 発行元が Microsoft の **GitHub Copilot Chat**

<img width="1512" height="982" alt="Screenshot 2026-10-22 at 9 19 19" src="https://github.com/user-attachments/assets/625a8b1f-733f-4630-ab5c-f632ea821b38" />

### 2. GitHub アカウントと GitHub Copilot

- GitHub アカウントを用意し、ブラウザーから[github.com](https://github.com/)にサインインできることを確認します。
- GitHub Copilot を利用できることを確認します。
- VS Code の Copilot アイコンからセットアップし、GitHub にサインインします。Copilot Chat が開き、質問に応答することを確認してください。

<img width="1512" height="982" alt="Screenshot 2026-10-22 at 9 09 18" src="https://github.com/user-attachments/assets/d29a5310-71be-4042-bb08-4a0e635d821e" />

<img width="1512" height="982" alt="Screenshot 2026-10-22 at 9 14 17" src="https://github.com/user-attachments/assets/ec27c76f-b396-4043-84c0-cb0b7329e1e4" />

### 3. Python

- [Python 3.15](https://www.python.org/downloads/) をインストールします。
- Windows ではインストーラーの **Add Python to PATH** を有効にします。
- VS Code のターミナルを開き、バージョンが表示されることを確認します。

  ```sh
  # Windows
  python --version

  # macOS / Linux
  python3 --version
  ```
<img width="1512" height="982" alt="Screenshot 2026-10-22 at 9 38 33" src="https://github.com/user-attachments/assets/fd79b273-1684-4af6-a0d2-a10a17d41ff4" />

### 4. Git

- [Git](https://git-scm.com/downloads) をインストールします。
- VS Code のターミナルで確認します。

  ```sh
  git --version
  ```

#### Git のコミット設定

- VS Code のターミナルで次のコマンドを実行します。
    - "GitHubのアカウント名"、"GitHubで使用するメールアドレス" は実際の値に置き換えてください。
    - 値はダブルクオーテーションで囲んでください。例： `git config user.name "ihcomega56"`
    - メールアドレスを公開したくない場合は、GitHub の **Settings → Emails** に表示される非公開用の `noreply` アドレスを利用できます。

```sh
git config user.name "GitHubのアカウント名"
git config user.email "GitHubで使用するメールアドレス"
```

<img width="1491" height="854" alt="Screenshot 2026-10-22 at 9 47 50" src="https://github.com/user-attachments/assets/e05959a5-5bbb-400a-b455-de1911527f21" />

## ワークショップ当日の準備

以下はワークショップ当日に行います。事前にリポジトリの取得やアプリの起動を済ませる必要はありません。

### リポジトリをForkして取得する

このリポジトリを開き、GitHub の **Fork** ボタンから自分のアカウントにForkします。自分のForkをVS Codeでクローンしてください。

- VS Code で `F1`（macOS は `Cmd+Shift+P`）を押し、**Git: Clone** を選びます。
- 自分のForkのURL（`https://github.com/自分のGitHubアカウント名/ghcp-intro-workshop-2610.git`）を入力し、保存先を選びます。
- クローン後にフォルダーを開きます。ワークスペースの信頼確認が表示されたら、リポジトリの内容を確認してから許可してください。
- HTTPSでGitHubにサインインして操作します。手動でPATを作成したり、SSH鍵を設定したりする必要はありません。認証を求められたら、VS Codeの案内に従ってブラウザーでGitHubにサインインします。

### 仮想環境を作成する

VS Code で **ターミナル → 新しいターミナル**を選び、リポジトリのフォルダー内で仮想環境を作ります。

```sh
# Windows
python -m venv .venv

# macOS / Linux
python3 -m venv .venv
```

#### 仮想環境を有効にする

```powershell
# Windows PowerShell
.venv\Scripts\Activate.ps1
```

```bat
:: Windows コマンドプロンプト
.venv\Scripts\activate.bat
```

```sh
# macOS / Linux
source .venv/bin/activate
```

有効になると、ターミナルのプロンプトに `(.venv)` が表示されます。PowerShell の実行ポリシーで有効化がブロックされる場合は、ポリシーを変更せず、次のコマンドでは `.venv\Scripts\python.exe` を `python` の代わりに使えます。

#### VS Code で仮想環境を選択する

- `F1`（macOS は `Cmd+Shift+P`）を押します。
- **Python: Select Interpreter** を選び、このリポジトリの `.venv` を選択します。
  - Windows: `.venv\Scripts\python.exe`
  - macOS / Linux: `.venv/bin/python`

### パッケージをインストールしてアプリを起動する

仮想環境を有効にしたターミナルで、以下を実行します。

```sh
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

ブラウザーが自動で開かない場合は、ターミナルに表示されるURL（通常は `http://localhost:8501`）を開きます。アプリを終了するときは、ターミナルで `Ctrl+C` を押してください。

### ブランチをPushしてPull Requestを作成する

- VS Code の左下にあるブランチ名をクリックし、**Create New Branch** を選びます。作業内容が分かるブランチ名を入力します。
- 変更後、ソース管理ビューで差分を確認し、コミットします。
- **Publish Branch** を選び、自分のForkへブランチをPushします。初回はブラウザーでGitHubへのサインインを求められる場合があります。
- GitHubで自分のForkを開き、**Compare & pull request** を選びます。元のワークショップリポジトリの `main` ブランチ宛てにPull Requestを作成します。

### 改修のお題の例

- メニューに商品を追加する
- 売り切れの商品を注文できないようにする
- 割引条件を追加する
- 注文確定後はカートを変更できないようにする
- 合計金額の計算を、画面表示の処理から分離する

Copilot の提案はそのまま採用せず、変更差分を確認し、アプリを動かして結果を確かめましょう。
