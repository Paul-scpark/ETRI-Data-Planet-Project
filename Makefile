run-server:
	python manage.py runserver

freeze:
	pip freeze > requirements.txt

install:
	pip install -r requirements.txt

db-dump:
	python manage.py runscript load_data