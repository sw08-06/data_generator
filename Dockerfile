FROM python:3.12.3

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

ENV DATA_PATH=/app/data

CMD ["python3", "src/main.py"]
