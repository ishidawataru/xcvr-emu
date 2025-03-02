FROM python:3.13 AS builder

WORKDIR /app

RUN pip install --upgrade pip setuptools pip-tools build

COPY pyproject.toml /app/

RUN mkdir src && touch src/__init__.py

RUN pip-compile --verbose --strip-extras pyproject.toml

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

RUN python -m build

RUN pip install -e '.[dev]'

CMD ["xcvr-emud", "-c", "src/xcvr_emu/config.yaml"]

FROM python:3.13-slim AS runtime

ARG TARGETARCH

RUN if [ "$TARGETARCH" = "arm64" ]; then \
  apt-get update && apt-get install -y build-essential; \
  fi

RUN --mount=type=bind,from=builder,source=/app,target=/app \
  pip install --no-cache-dir /app/dist/*.whl

RUN --mount=type=bind,from=builder,source=/app,target=/app \
  cp /app/src/xcvr_emu/config.yaml .

CMD ["xcvr-emud", "-c", "config.yaml"]
