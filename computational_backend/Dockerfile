# use official Python image as the base image
FROM --platform=linux/amd64 python:3.12-slim-trixie
# download uv from Astral's GitHub Container Registry and copy the uv binary to the image
COPY --from=ghcr.io/astral-sh/uv:0.11.1 /uv /uvx /bin/
WORKDIR /app
# copy the requirements file to the image and install the dependencies using uv
COPY pyproject.toml uv.lock ./
# install the dependencies using uv
RUN uv --version
RUN uv sync
# copying the rest of the application code to the container
COPY . .
# exposing the port so it is accessible outside the container on localhost in our computer
EXPOSE 8002
# command to run the application when the container starts
RUN uv run python -m unittest -v
CMD ["uv", "run", "uvicorn", "computational_api:app", "--port=8002","--host=0.0.0.0"]  
# exporting on the localhost

# tu build the image: docker build --platform linux/amd64 -t computational_backend .