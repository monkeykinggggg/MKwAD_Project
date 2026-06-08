To start the server:
```bash
uv sync
```
After installing packages, start the lightweight server `uvicorn` via uv:
```bash
uv run uvicorn medical_api:app --port 8001
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

## To send analytics data to computational server make one of requests available:
### Request for mean, variance, std_dev calculations
```bash
GET /analyze/{metric}/{operation}
```
Where:
metric -> choose one from: ["mean", "variance", "std_dev"]

operation -> one of database columns:
```py
class PatientResultsReponse(BaseModel):
    age: int
    sex: int
    chest_pain: int
    resting_blood: int
    serum_cholesterol: int
    fasting_blood_sugar: int
    electrocardiography: int
    maximum_heart_rate: int
    angina: int
    oldpeak_ST: float
    slope_ST: float
    major_vessel_number: int
    thal: int
    target: int
```
And then the endpoint can be followed by filtering parameters, f.ex.:
```bash
?sex=1&resting_blood_min=120
```
Here we search between patient who are male (sex = 1) and their resting_blood parameter is minimum 120.

Anallogicaly, for the max values we would have `column_name_max` field in the parameters section of the query.

So for parameters we have options:
- `column_name` = specific_val (we filter for rows that have column_name== specific_val)
- `column_name_min` = specific_val (we filter for rows that have column_name>= specific_val)
- `column_name_max` = specific_val(we filter for rows that have column_name<= specific_val )

### Request for covariance calculations between two features
```bash
GET /covariance/{metric_x}/{metric_y}
```
Where:
metric_x, metric_y -> choose one from database columns

And then the endpoint can be followed by filtering parameters same as the analytical endpoint.