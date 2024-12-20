FROM python:3.11 AS builder

WORKDIR /app

RUN pip install --upgrade pip setuptools pip-tools build

COPY pyproject.toml /app/

RUN mkdir src && touch src/__init__.py

RUN pip-compile --verbose --strip-extras pyproject.toml

RUN pip install  --no-cache-dir -r requirements.txt

COPY . /app

RUN python -m build

FROM python:3.11-slim AS runtime

RUN --mount=type=bind,from=builder,source=/app,target=/app \
  pip install --no-cache-dir /app/dist/*.whl

CMD ["xcvr-emud"]
