FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt setup.py ./
COPY app app/

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install -e .[test]
RUN apt-get update && apt-get install -y netcat-openbsd

COPY docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

ENV FLASK_APP=server.py
ENV FLASK_ENV=development
ENV PYTHONPATH=/app

EXPOSE 5000

ENTRYPOINT ["docker-entrypoint.sh"]
