To start the server:
```bash
uv sync
```
After installing packages, start the lightweight server `uvicorn` via uv:
```bash
uv run uvicorn api:app --port 8001
```
You can check all the endpoints in the browser in Swagger UI on `http://localhost:8000/docs`

Database description:
1. age
2. sex
3. chest pain type (4 values)
4. resting blood pressure
5. serum cholestoral in mg/dl
6. fasting blood sugar > 120 mg/dl
7. resting electrocardiographic results (values 0,1,2)
8. maximum heart rate achieved
9. exercise induced angina
10. oldpeak = ST depression induced by exercise relative to rest
11. the slope of the peak exercise ST segment
12. number of major vessels (0-3) colored by flourosopy
13. thal: 0 = normal; 1 = fixed defect; 2 = reversable defect

Analysis examples:
https://www.kaggle.com/datasets/johnsmith88/heart-disease-dataset/code