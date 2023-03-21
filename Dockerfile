FROM python:3.9-slim

RUN apt-get update && apt-get install -y sqlite3

WORKDIR /app

RUN pip install --upgrade pip  
RUN pip install PyYAML==6.0

COPY ./app .

RUN chmod g+w /app
RUN chmod g+w /app/db.sqlite3
RUN chmod g+w /app/domains.yml

CMD ["python", "main.py"]
