FROM python:3.11 

WORKDIR /app

EXPOSE 5050

COPY pyproject.toml poetry.lock ./

RUN pip install poetry 
RUN poetry install --no-dev

COPY . ./

CMD ["poetry", "run", "python", "main.py"]