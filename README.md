Установка зависимостей:
pip install -r requirements.txt

База Данных:
PostgreSQL
python3 manage.py loaddata women.json

Фото:
https://drive.google.com/drive/folders/1B_aeqDkN9Szlj2jNSAxHfeeTbVlUde_W?usp=drive_link

Миграции:
python3 manage.py makemigrations
python3 manage.py migrate

python3 manage.py runserver