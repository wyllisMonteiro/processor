FROM python:3.6-stretch

WORKDIR /app

ENV FLASK_APP api
ENV FLASK_RUN_HOST 0.0.0.0
ENV FLASK_ENV development

COPY requirements.txt requirements.txt
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install -r requirements.txt

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y

CMD ["flask", "run"]
