while ! nc -z db 5432; do sleep 5; done;
  echo "postgres available"

  python manage.py makemigrations 
  python manage.py makemigrations app
  python manage.py migrate
  python manage.py runserver 0.0.0.0:8000
  ;