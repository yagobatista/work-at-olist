release: python src/manage.py migrate --noinput
web: gunicorn --chdir src/ project.wsgi --log-file -