FROM python:3.10-slim-buster

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "app.py"]
