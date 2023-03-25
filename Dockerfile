FROM python:3.11-slim

WORKDIR /code
COPY . /code
ENV BLOG_DB_URL="postgresql://postgres:postgres@localhost:5432/blog"

RUN pip install --no-compile --upgrade pip \
    && pip install --no-compile poetry \
    && poetry config virtualenvs.create false \
    && poetry config cache-dir /tmp/.cache/pypoetry \
    && poetry install --no-interaction --no-ansi \
    && pip uninstall --yes poetry \
    && rm -rf /tmp/.cache/pypoetry \
    && rm -rf /tmp/bytecode

CMD ["gunicorn --chdir application app:app"]
