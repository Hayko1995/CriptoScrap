while ! nc -z db 5432; do sleep 3; done;
  echo "postgres available"

  echo "Attempting to apply migrations"
  python manage.py migrate

  echo "Attempting to create superuser"
  

  echo "Attempting to start server"
  python manage.py makemigrations 
  python manage.py makemigrations app
  python manage.py migrate
  python manage.py runserver 0.0.0.0:8000
  ;