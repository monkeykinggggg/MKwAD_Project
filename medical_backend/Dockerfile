FROM --platform=linux/amd64 python:3.12-slim-trixie
COPY --from=ghcr.io/astral-sh/uv:0.11.1 /uv /uvx /bin/
WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv --version
RUN uv sync

COPY . .
EXPOSE 8001
ENV COMPUTATIONAL_URL=http://computational-server:8002
CMD ["uv", "run", "uvicorn", "medical_api:app", "--port=8001","--host=0.0.0.0"]
# tu build the image: docker build --platform linux/amd64 -t medical_backend .