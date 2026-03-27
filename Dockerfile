FROM python:3.10
EXPOSE 8000
WORKDIR /app
COPY requirements.txt .
RUN  pip install  -r requirements.txt
COPY . .
CMD ["uvicorn", "app:app", "--host", "0.0.0.0"]