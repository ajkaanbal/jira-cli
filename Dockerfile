FROM python:3.6-alpine

MAINTAINER ajkaanbal@gmail.com

WORKDIR /srv/app

COPY . .

RUN apk add bash && pip install -r requirements.txt

CMD ["python", "jira.py"]

