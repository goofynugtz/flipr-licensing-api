FROM python:3-slim-buster
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /app
ADD . /app
RUN pip install --upgrade pip
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt
COPY . /app
# RUN apt-get update
# RUN apt-get -y install curl
# RUN apt-get -y install awscli
RUN ls
RUN echo "\n\n"
RUN ls /app
# RUN python manage.py makemigrations --no-input
# RUN python manage.py migrate --no-input --run-syncdb
ENTRYPOINT [ "bash","./script.sh" ]
# HEALTHCHECK CMD curl --fail http://localhost:8000/api || exit 1
