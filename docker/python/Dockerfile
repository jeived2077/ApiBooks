FROM python:3.12-slim



RUN pip install --no-cache-dir --upgrade pip

COPY docker/python/requirements.txt /code/requirements.txt

WORKDIR /code

COPY ./src /code/src
RUN pip install --no-cache-dir -r /code/requirements.txt

ENV PYTHONPATH=/code/src
ENV DB_USER=postgres
ENV DB_PASSWORD=1234
ENV DB_HOST=db
ENV DB_PORT=5432
ENV DB_NAME=Reader_Database
ENV SECRET_KEY=super_secret_key
ENV REDIS_HOST=redis
ENV REDIS_PORT=6379
ENV REDIS_PASSWORD=
ENV REDIS_SSL=False
ENV REDIS_CERT_SEQL=None

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80", "--workers", "4"]                      