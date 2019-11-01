FROM python:3.7-alpine
ENV VIRTUAL_ENV=/app/.venv
ENV PYTHONPATH=/app/.venv/lib/python3.7/site-packages/
EXPOSE 8080
WORKDIR /app
ENTRYPOINT ["python", "-c", "import sys; from importlib import import_module; sys.argv = ['server']; import_module('pull_request_service.server').main()"]
COPY . /app
