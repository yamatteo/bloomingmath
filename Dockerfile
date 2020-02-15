FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

COPY requirements.txt .
COPY .env.production .env
COPY ./app /app
COPY ./dist /dist

RUN pip install -r requirements.txt
