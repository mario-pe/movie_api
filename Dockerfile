FROM python:3.6
ENV PYTHONUNBUFFERED 1
RUN mkdir /movies_service
WORKDIR /movies_service
ADD . /movies_service/
RUN pip install -r requirements-dev.txt