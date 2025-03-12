FROM python:3.10

# Allows Docker to cache installed dependencies between builds
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Mounts the application code to the image
COPY . /code

WORKDIR /code

# Run database migrations
RUN python manage.py makemigrations
RUN python manage.py migrate

# Create a superuser automatically
ARG SUPERUSER_USERNAME=admin
ARG SUPERUSER_EMAIL=admin@gmail.com
ARG SUPERUSER_PASSWORD=admin

RUN python manage.py shell <<EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='$SUPERUSER_USERNAME').exists():
    User.objects.create_superuser('$SUPERUSER_USERNAME', '$SUPERUSER_EMAIL', '$SUPERUSER_PASSWORD')
EOF

EXPOSE 8000

# Runs the production server
ENTRYPOINT ["python", "manage.py"]
CMD ["runserver", "0.0.0.0:8000"]