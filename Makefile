run:
	python manage.py runserver

migrations:
	python manage.py makemigrations

migrate:
	python manage.py migrate

freeze:
	pip freeze > requirements.txt

install:
	pip install -r requirements.txt

dump:
	python manage.py runscript load_data