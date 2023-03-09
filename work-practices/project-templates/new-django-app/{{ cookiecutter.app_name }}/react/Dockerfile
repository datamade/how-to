# Root Dockerfile for all DataMade apps
FROM python:3.11

LABEL maintainer "DataMade <info@datamade.us>"

# Install any additional OS-level packages you need via apt-get. RUN statements
# add additional layers to your image, increasing its final size. Keep your
# image small by combining related commands into one RUN statement, e.g.,
#
# RUN apt-get update && \
#     apt-get install -y python-pip
#
# Read more on Dockerfile best practices at the source:
# https://docs.docker.com/develop/develop-images/dockerfile_best-practices
RUN apt-get install -y --no-install-recommends \
	postgresql-client nodejs{% if cookiecutter.postgis == 'True' %}\
	gdal-bin{% endif %}

RUN curl -sL https://deb.nodesource.com/setup_18.x | bash -

RUN mkdir /app
WORKDIR /app

COPY ./package.json ./package-lock.json* /app/
RUN npm install

COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

ENV DJANGO_SECRET_KEY 'foobar'
ENV DJANGO_DEBUG 'False'
RUN python manage.py collectstatic --noinput &&
	python manage.py compress
