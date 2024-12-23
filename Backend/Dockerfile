# Dependencies

FROM python:3.13
WORKDIR /app/
RUN pip install poetry
COPY poetry.lock pyproject.toml /app/
RUN poetry install --without dev

# Application

COPY . /app/
ENTRYPOINT [ "poetry" ]
CMD ["run", "python", "manage.py", "runserver", "0.0.0.0:8000"]