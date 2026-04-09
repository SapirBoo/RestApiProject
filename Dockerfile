FROM python:3.10
WORKDIR /app
COPY requirements.txt .
RUN  pip install --no-cache-dir --upgrade -r requirements.txt
RUN apt-get update && apt-get install -y postgresql-client

COPY . .

#CMD ["gunicorn", "-k",  "uvicorn.workers.UvicornWorker","app:app", "--bind", "0.0.0.0:8000","--workers", "2", "--timeout", "60",  "--access-logfile", "-","--error-logfile", "-"]
RUN chmod +x docker-entrypoint.sh

CMD ["./docker-entrypoint.sh"]