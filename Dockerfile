FROM vitalbeats/poetry:1.1.4

WORKDIR /app
COPY . /app
RUN poetry install

EXPOSE 8080
ENTRYPOINT ["poetry", "run", "server"]
