FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

COPY ./app /app

WORKDIR /app
RUN pip install beautifulsoup4
RUN pip install requests