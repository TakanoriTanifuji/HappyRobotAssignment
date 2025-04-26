FROM python:3.12-slim

COPY requirements.txt /

RUN pip install --upgrade pip

RUN pip install -r /requirements.txt

COPY . /app

WORKDIR /app

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "wsgi:app"]