FROM python:3.8
RUN mkdir /usr/src/app
WORKDIR /usr/src/app
COPY requirements.txt .
RUN pip install -r requirements.txt
ENV PYTHONUNBUFFERED 1
COPY LanguageDetection.py /usr/src/app