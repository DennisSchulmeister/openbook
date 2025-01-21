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
RUN mkdir -p openbook/_static.volume
RUN mkdir -p openbook/_media.volume

COPY --from=build /app/requirements.txt . 
RUN python -m venv .env
RUN .env/bin/pip install -r requirements.txt
RUN .env/bin/pip install psycopg

COPY . .
COPY _docker/openbook.entrypoint.sh openbook/entrypoint.sh
RUN chmod +x openbook/entrypoint.sh

# This copies to …/_static, according to settings.py
# start.sh then copies the files onto the volume …/_static.volume
RUN .env/bin/python openbook/manage.py collectstatic --noinput

VOLUME /app/openbook/_media.volume
VOLUME /app/openbook/_static.volume
EXPOSE 8000

WORKDIR /app/openbook
ENTRYPOINT ["./entrypoint.sh"]
