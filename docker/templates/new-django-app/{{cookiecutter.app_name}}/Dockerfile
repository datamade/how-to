# Extend the base Python image
# See https://hub.docker.com/_/python for version options
# N.b., there are many options for Python images. We used the plain
# version number in the pilot. YMMV. See this post for a discussion of
# some options and their pros and cons:
# https://pythonspeed.com/articles/base-image-python-docker-images/
FROM python:3.11

# Give ourselves some credit
LABEL maintainer "DataMade <info@datamade.us>"

# Add the NodeSource PPA and install Node.js
# (see: https://github.com/nodesource/distributions/blob/master/README.md)
RUN apt-get update \
	&& apt-get install sudo \ 
	&& curl -fsSL https://deb.nodesource.com/setup_{{ cookiecutter.node_version }}.x | sudo -E bash - \
	&& sudo apt-get install -y nodejs


# Install any additional OS-level packages you need via apt-get. RUN statements
# add additional layers to your image, increasing its final size. Keep your
# image small by combining related commands into one RUN statement, e.g.,
#
# RUN apt-get update && \
#     apt-get install -y python-pip
#
# Read more on Dockerfile best practices at the source:
# https://docs.docker.com/develop/develop-images/dockerfile_best-practices
RUN apt-get install -y --no-install-recommends postgresql-client nodejs{% if cookiecutter.postgis == 'True' %} gdal-bin{% endif %}

# Inside the container, create an app directory and switch into it
RUN mkdir /app
WORKDIR /app

# Copy the requirements file into the app directory, and install them. Copy
# only the requirements file, so Docker can cache this build step. Otherwise,
# the requirements must be reinstalled every time you build the image after
# the app code changes. See this post for further discussion of strategies
# for building lean and efficient containers:
# https://blog.realkinetic.com/building-minimal-docker-containers-for-python-applications-37d0272c52f3
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install Node requirements
COPY ./package.json /app/package.json
RUN npm install

# Copy the contents of the current host directory (i.e., our app code) into
# the container.
COPY . /app

# Add a bogus env var for the Django secret key in order to allow us to run
# the 'collectstatic' management command
ENV DJANGO_SECRET_KEY 'foobar'

# Sets Debug to False to make sure that Django compressor can run.
# Unless overridden in docker-compose.yml or .env locally or config variables
# in Heroku, this sets the environment to production mode
ENV DJANGO_DEBUG 'False'

# Build static files into the container
RUN python manage.py collectstatic --noinput
RUN python manage.py compress
