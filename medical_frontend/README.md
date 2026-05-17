# medical_frontend

Frontend projektu MedSecure FHE zbudowany w Streamlit.

## Uruchomienie

Najpierw uruchom backend w katalogu [medical_backend](../medical_backend):

```bash
uv sync
uv run uvicorn api:app --reload
```

Następnie w tym katalogu uruchom frontend w osobnym terminalu w katalogu [medical_frontend](../medical_frontend):

```bash
uv sync
streamlit run app.py
```

## Uwagi

- Aplikacja frontendowa łączy się z backendem pod adresem `http://localhost:8000`.
- Panel Streamlit zwykle otwiera się pod `http://localhost:8501`.
