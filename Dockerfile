FROM python:3.11-slim

WORKDIR /app

LABEL dev="aron"

COPY . .

ENTRYPOINT [ "python -m flask run" ]