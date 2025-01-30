# Pythonイメージを指定
FROM python:3.11

# 作業ディレクトリを設定
WORKDIR /app

# 必要なライブラリをインストール
COPY pyproject.toml .
RUN pip install --no-cache-dir flask flask-sqlalchemy psycopg2-binary

# アプリケーションコードをコピー
COPY . .

# Flaskアプリを起動
CMD ["python", "main.py"]
