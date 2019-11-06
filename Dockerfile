FROM python:3.7

RUN pip3 install poetry
RUN poetry config settings.virtualenvs.create false

WORKDIR /app
COPY . /app
RUN poetry install

EXPOSE 8080
ENTRYPOINT ["poetry", "run", "server"]
