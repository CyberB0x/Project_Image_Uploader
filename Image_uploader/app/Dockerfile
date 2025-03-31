FROM python:3.12-alpine

LABEL authors="Arslon"

WORKDIR /app

COPY ./requirements.txt .

RUN apk add --no-cache jpeg-dev zlib-dev \
    && pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "app.py"]
