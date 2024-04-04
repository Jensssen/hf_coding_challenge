FROM python:3.10.0-slim

WORKDIR /app

COPY ./src/ .

RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y vim

EXPOSE 8080

CMD ["python", "app.py"]
