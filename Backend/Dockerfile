# Dependencies

FROM python:3.13
WORKDIR /app/
RUN pip install --no-cache-dir poetry
COPY poetry.lock pyproject.toml /app/
RUN poetry install --without dev

# Application

COPY . /app/
ENTRYPOINT [ "poetry" ]
CMD ["run", "fastapi", "main.py", "--port", "80"]