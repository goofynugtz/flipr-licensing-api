FROM python:3-slim-buster
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /
ADD . /
RUN pip install --upgrade pip
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
COPY . /
# RUN apt-get update
# RUN apt-get -y install curl
# ENTRYPOINT [ "bash","./script.sh" ]
# HEALTHCHECK CMD curl --fail http://localhost:8000/api || exit 1
