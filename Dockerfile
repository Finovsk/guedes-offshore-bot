FROM python:3.7.6-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

ENTRYPOINT ["python","main.py"]