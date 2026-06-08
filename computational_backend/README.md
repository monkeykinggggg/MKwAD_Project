Follow these steps to run the computational server:
```bash
uv sync
uv run uvicorn computational_api:app --port 8002
# paste to run tests:
uv run python -m unittest -v
```
Open the Swagger API test environment in browser on ``