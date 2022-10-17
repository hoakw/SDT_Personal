import requests




url = "http://192.168.1.207:30487/v1/notebooks"

headers = {
    "Content-Type": "application/json"
}

params = {
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

print(f"URL = {url}/{method}")
#respeonse = requests.get(f"{url}/{method}/", headers=headers, params=params)
#respeonse = requests.get(f"{url}/{method}/", headers=headers, params=params)
respeonse = requests.post(f"{url}/{method}/", headers=headers, data=data)

print(respeonse.text, flush=True)
