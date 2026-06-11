FROM --platform=linux/amd64 python:3.13-slim-trixie
COPY --from=ghcr.io/astral-sh/uv:0.11.1 /uv /uvx /bin/
WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync

COPY . .
EXPOSE 8501
ENV BACKEND_URL=http://medical-server:8001
CMD ["uv", "run", "streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
# tu build the image: docker build --platform linux/amd64 -t medical_backend .