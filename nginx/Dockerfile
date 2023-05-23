FROM python:3-slim-buster
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
COPY ./ssl.sh ./ssl.sh
COPY ./ssl.conf ./default.conf.backup
RUN apt-get update
ENTRYPOINT [ "bash","./ssl.sh" ]