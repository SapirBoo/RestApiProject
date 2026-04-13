FROM python:3.10
WORKDIR /app
COPY requirements.txt .
RUN  pip install --no-cache-dir --upgrade -r requirements.txt
RUN apt-get update && apt-get install -y postgresql-client

COPY . .
RUN chmod +x docker-entrypoint.sh

CMD ["./docker-entrypoint.sh"]