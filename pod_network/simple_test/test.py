import requests
import json
import time
import pandas as pd

svc_name = "fastapi-db-test"
svc_namespace = "sdt"
#url = f"http://{svc_name}.{svc_namespace}.svc.cluster.local"
url = f"http://192.168.1.200:30487"
#url = f"http://192.168.1.207:8000"
#method = "v1/notebooks"
method = "v1/notebooks/delete{notebook_id}"
headers = {
    "Content-Type": "application/json"
}

params = {
    "notebook_name": "test1",
    "namespace": "sdt"
}


data = json.dumps({
    "notebook_name": "jupyter",
    "namespace": "sdt",
    "image": "jupyter/datascience-notebook:latest",
    "label": "notebooks",
    "cpu": 100,
    "mem": 250,
    "gpu": 0,
    "password": "string",
    "target_port": 8888
})

while True:
    print(f"URL = {url}/{method}")
    respeonse = requests.delete(f"{url}/{method}/", headers=headers, params=params)
    #respeonse = requests.get(f"{url}/{method}/", headers=headers, params=params)
    #respeonse = requests.post(f"{url}/{method}/", headers=headers, data=data)

    print(respeonse.text)
    #result = json.loads(respeonse.text)
    #print(result)
    #print(pd.DataFrame(result))

    time.sleep(5)


