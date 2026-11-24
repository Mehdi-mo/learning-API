import requests

student = {"hours_studied": 10, "attendance": 80}
response = requests.post('http://127.0.0.1:8000/predict', json = student)

print(response.json())