import requests
import json
import time


url = f"http://192.168.1.207:30569/v1/models/kserve-test:predict"

headers = {
    "Host": "kserve-test.mlflow.example.com"
}

data = json.dumps({
    "test" : "Test GOOD!!!"
})

respeonse = requests.post(url, headers=headers, data=data)

print(respeonse)


