#===============================================================================
# Build container
#===============================================================================
FROM python:slim AS build

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app
COPY pyproject.toml .
COPY poetry.lock .

RUN python -m venv .env
RUN .env/bin/pip install poetry poetry-plugin-export
RUN .env/bin/poetry export --format=requirements.txt --output=requirements.txt

#===============================================================================
# App container
#===============================================================================
FROM python:slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
RUN mkdir -p openbook_server/_static.volume
RUN mkdir -p openbook_server/_media.volume

COPY --from=build /app/requirements.txt . 
RUN python -m venv .env
RUN .env/bin/pip install -r requirements.txt
RUN .env/bin/pip install psycopg

COPY . .
COPY _docker/openbook_server.entrypoint.sh openbook_server/entrypoint.sh
RUN chmod +x openbook_server/entrypoint.sh

# This copies to …/_static, according to settings.py
# start.sh then copies the files onto the volume …/_static.volume
RUN .env/bin/python openbok_server/manage.py collectstatic --noinput

VOLUME /app/openbook_server/_media.volume
VOLUME /app/openbook_server/_static.volume
EXPOSE 8000

WORKDIR /app/openbook_server
ENTRYPOINT ["./entrypoint.sh"]
