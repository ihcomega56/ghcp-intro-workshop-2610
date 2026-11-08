# サンプルアプリ: カフェ注文シミュレーター

ハンズオンで作るアプリのイメージをつかむための完成例です。ハンズオン本編では、このフォルダーのコードは使わず、GitHub Copilot と一緒にアプリをゼロから作ります。

Python と [Streamlit](https://streamlit.io/) で動作し、バックエンドやデータベースは使いません。

## 実行手順

VS Code でこのリポジトリを開き、メニューの **ターミナル → 新しいターミナル** でターミナルを開いてから、次のコマンドを順に実行します。

### Windows（PowerShell）

```powershell
cd example
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

`Activate.ps1` の実行がポリシーで拒否された場合は、次のコマンドを実行してから再度有効化します。

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

### macOS / Linux

```sh
cd example
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

ブラウザーで `http://localhost:8501` が開き、アプリが表示されます。終了するときは、ターミナルで `Ctrl + C` を押します。
