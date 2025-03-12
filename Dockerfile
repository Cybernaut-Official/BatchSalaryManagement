FROM python:3.10

# Allows docker to cache installed dependencies between builds
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

#RUN python manage.py makemigrations

#RUN python manage.py migrate


# Mounts the application code to the image
COPY . code

WORKDIR /code

RUN python manage.py makemigrations

RUN python manage.py migrate
EXPOSE 8000

# runs the production server
ENTRYPOINT ["python", "manage.py"]
CMD ["runserver", "0.0.0.0:8000"]