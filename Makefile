up:
	docker-compose up -d

makemigrate:
	docker-compose run --rm web python manage.py makemigrations

migrate:
	docker-compose run --rm web python manage.py migrate

super-user:
	docker-compose run --rm web python manage.py createsuperuser
