
# 部活管理システム

このプロジェクトは、Flaskを使用した部活管理システムです。ウェブインターフェースを通じて部活やメンバーを管理することができます。バックエンド開発には`Flask`と`Flask-SQLAlchemy`を使用しています。

## 主な機能
- 部活の登録
- 新入生の登録と部活への割り当て
- 部活とメンバーの一覧表示
- APIを使用したCRUD操作

---

## 前提条件
- Python 3.11以上
- 仮想環境ツール（venv、`uv`、または`Rye`）

---

## セットアップ手順

### `uv` を使用したセットアップ

#### Mac
1. **`uv` のインストール**:
   ```bash
   pip install uv
   ```

2. **新しい仮想環境の作成**:
   ```bash
   uv sync
   ```

4. **プロジェクトの実行**:
   ```bash
   uv run python main.py
   ```

#### Windows
1. **`uv` のインストール**:
   ```cmd
   pip install uv
   ```

2. **新しい仮想環境の作成**:
   ```cmd
   uv sync
   ```

4. **プロジェクトの実行**:
   ```cmd
   uv run python main.py
   ```

---

### `Rye` を使用したセットアップ

#### Mac
1. **Rye のインストール**:
   ```bash
   curl -sSf https://rye-up.com/get | bash
   ```

2. **新しいプロジェクト環境の作成**:
   ```bash
   rye sync
   ```

3. **依存関係の追加**:
   ```bash
   rye add flask flask-sqlalchemy
   ```

4. **プロジェクトの実行**:
   ```bash
   rye run python main.py
   ```

#### Windows
1. **Rye のインストール**:
   ```cmd
   curl -sSf https://rye-up.com/get | powershell
   ```

2. **新しいプロジェクト環境の作成**:
   ```cmd
   rye sync
   ```

3. **依存関係の追加**:
   ```cmd
   rye add flask flask-sqlalchemy
   ```

4. **プロジェクトの実行**:
   ```cmd
   rye run python main.py
   ```

---

### `pip` を使用したセットアップ

#### Mac
1. **仮想環境の作成**:
   ```bash
   python3 -m venv .venv
   ```

2. **仮想環境の有効化**:
   ```bash
   source .venv/bin/activate
   ```

3. **依存関係のインストール**:
   ```bash
   pip install flask flask-sqlalchemy
   ```

4. **プロジェクトの実行**:
   ```bash
   python main.py
   ```

#### Windows
1. **仮想環境の作成**:
   ```cmd
   python -m venv .venv
   ```

2. **仮想環境の有効化**:
   ```cmd
   .venv\Scripts\activate
   ```

3. **依存関係のインストール**:
   ```cmd
   pip install flask flask-sqlalchemy
   ```

4. **プロジェクトの実行**:
   ```cmd
   python main.py
   ```

---

## プロジェクトファイル
- `main.py`: Flaskアプリケーションのメインファイル。
- `templates/index.html`: ウェブインターフェース用のHTMLテンプレート。
- `club_management.db`: SQLiteデータベースファイル（実行時に生成されます）。
- `README.md`: このファイル。

---

## APIエンドポイント

### 部活関連
1. **部活の登録 (POST)**:
   - エンドポイント: `/clubs`
   - リクエストボディ:
     ```json
     {
       "club_name": "サッカークラブ",
       "description": "サッカー愛好家のためのクラブ。",
       "capacity": 20
     }
     ```

2. **全ての部活の取得 (GET)**:
   - エンドポイント: `/clubs`

### メンバー関連
1. **新入生の登録 (POST)**:
   - エンドポイント: `/members`
   - リクエストボディ:
     ```json
     {
       "name": "田中太郎",
       "grade": 1,
       "club_id": 1,
       "contact": "tanaka@example.com"
     }
     ```

2. **全てのメンバーの取得 (GET)**:
   - エンドポイント: `/members`

---

## 注意事項
- データベースを同期するには、以下のURLにアクセスしてください:
  ```
  http://127.0.0.1:5000/sync
  ```
- Python 3.11以上が必要です。
