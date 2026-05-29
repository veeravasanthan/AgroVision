import requests
import os

url = "http://127.0.0.1:5000/disease-predict"
files = {'file': ('test_apple.jpg', b'fake image data', 'image/jpeg')}

try:
    response = requests.post(url, files=files)
    print(f"Status Code: {response.status_code}")
    if "Diagnosis:" in response.text:
        print("Success: Diagnosis found in response.")
    else:
        print("Failure: Diagnosis NOT found in response.")
        # print(response.text[:500])
except Exception as e:
    print(f"Error: {e}")
