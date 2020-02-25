FROM python:3.7
MAINTAINER "DataMade <info@datamade.us>"

RUN pip install --no-cache-dir cookiecutter

COPY ./python /python
COPY ./django /django

CMD ["cookiecutter", "-f", "/python"]
