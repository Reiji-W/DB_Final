# Python�C���[�W���w��
FROM python:3.11

# ��ƃf�B���N�g����ݒ�
WORKDIR /app

# �K�v�ȃ��C�u�������C���X�g�[��
COPY pyproject.toml .
RUN pip install --no-cache-dir flask flask-sqlalchemy psycopg2-binary

# �A�v���P�[�V�����R�[�h���R�s�[
COPY . .

# Flask�A�v�����N��
CMD ["python", "main.py"]
