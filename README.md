# VS Code + GitHub Copilot ハンズオン環境セットアップ

このリポジトリは、VS Code と GitHub Copilot を使って、Python の小さな注文アプリを改修するハンズオン用スターターです。アプリは Streamlit で動作し、バックエンドやデータベースの構築は不要です。

## 事前にインストールするもの

### 1. GitHub アカウントと GitHub Copilot

- GitHub アカウントを用意し、ブラウザーからサインインできることを確認します。
- GitHub Copilot を利用できることを確認します。会社からライセンスが付与されている場合は、そのアカウントを使ってください。無料プランには利用上限があります。
- VS Code の Copilot アイコンからセットアップし、GitHub にサインインします。Copilot Chat が開き、質問に応答することを確認してください。

### 2. Visual Studio Code

- [Visual Studio Code](https://code.visualstudio.com/) の最新安定版をインストールします。
- 拡張機能で、発行元が Microsoft の **Python** をインストールします。
- GitHub Copilot の拡張機能は、VS Code の Copilot セットアップ画面の案内に従ってインストールします。
- TypeScript、Node.js、Vite 用の拡張機能は不要です。

### 3. Python

- [Python 3.11 または 3.12](https://www.python.org/downloads/) をインストールします。
- Windows ではインストーラーの **Add Python to PATH** を有効にします。
- VS Code のターミナルを開き、バージョンが表示されることを確認します。

  ```sh
  # Windows
  python --version

  # macOS / Linux
  python3 --version
  ```

### 4. Git

- [Git](https://git-scm.com/downloads) をインストールします。
- VS Code のターミナルで確認します。

  ```sh
  git --version
  ```

## リポジトリを取得する

VS Code で `F1`（macOS は `Cmd+Shift+P`）を押し、**Git: Clone** を選びます。次の URL を入力し、保存先を選択します。

```text
https://github.com/ihcomega56/ghcp-intro-workshop-2610.git
```

クローン後にフォルダーを開きます。ワークスペースの信頼確認が表示されたら、リポジトリの内容を確認してから許可してください。

## 仮想環境を作成する

VS Code でリポジトリのフォルダーを開き、**ターミナル → 新しいターミナル**を選びます。プロジェクトごとにパッケージを分けるため、仮想環境を作成します。

```sh
# Windows
python -m venv .venv

# macOS / Linux
python3 -m venv .venv
```

### 仮想環境を有効にする

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

有効になると、ターミナルのプロンプトに `(.venv)` が表示されます。PowerShell の実行ポリシーによって有効化がブロックされる場合は、ポリシーを変更せず、VS Code で `.venv` の Python を選択して、以降のコマンドをその Python から実行してください。

## VS Code で仮想環境を選択する

- `F1`（macOS は `Cmd+Shift+P`）を押します。
- **Python: Select Interpreter** を選びます。
- このリポジトリ内の `.venv` を選択します。
  - Windows: `.venv\Scripts\python.exe`
  - macOS / Linux: `.venv/bin/python`

## パッケージをインストールして起動する

仮想環境を有効にしたターミナルで、以下を実行します。

```sh
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

ブラウザーが自動で開かない場合は、ターミナルに表示される URL（通常は `http://localhost:8501`）を開いてください。アプリを終了するときは、ターミナルで `Ctrl+C` を押します。

## ハンズオンでの改修例

- メニューに商品を追加する
- 売り切れの商品を注文できないようにする
- 割引条件を追加する
- 注文確定後はカートを変更できないようにする
- 合計金額の計算を、画面表示の処理から分離する

Copilot の提案はそのまま採用せず、変更差分を確認し、アプリを動かして結果を確かめましょう。

## トラブルシューティング

- `python` が見つからない場合は、Python のインストールと PATH 設定を確認し、VS Code を再起動します。macOS / Linux では `python3` が使える場合があります。
- `streamlit` が見つからない場合は、VS Code で選択した Python が `.venv` のものか確認し、`python -m pip install -r requirements.txt` を再実行します。
- Copilot が応答しない場合は、VS Code の GitHub アカウントと Copilot の利用権限を確認します。

## Git のコミット名（任意）

このワークショップで Git のコミットを行う場合は、リポジトリのターミナルで名前とメールアドレスを設定します。以下の値を自分のものに置き換えてください。

```sh
git config user.name "自分の名前"
git config user.email "GitHubで使用するメールアドレス"
```

メールアドレスを公開したくない場合は、GitHub の **Settings → Emails** に表示される非公開用の `noreply` アドレスを利用できます。
