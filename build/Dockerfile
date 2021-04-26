FROM python:3.6.10-alpine3.11

WORKDIR /app

ENV FLASK_APP flaskr
ENV FLASK_RUN_HOST 0.0.0.0
ENV FLASK_ENV development

RUN apk add --no-cache gcc musl-dev linux-headers

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

CMD ["flask", "run"]
