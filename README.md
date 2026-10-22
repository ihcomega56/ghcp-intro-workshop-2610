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

