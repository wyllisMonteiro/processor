FROM python:3.6-stretch

WORKDIR /app

ENV FLASK_APP flaskr
ENV FLASK_RUN_HOST 0.0.0.0
ENV FLASK_ENV prod

COPY requirements.txt requirements.txt
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["flask", "run"]
