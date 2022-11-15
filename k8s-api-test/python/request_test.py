import requests
import json



url = "http://3.39.12.67:30467/sites"
#url = "http://3.39.12.67:30467/oauth/token"
#url = "http://3.39.12.67:30467/customers/76U4-BE7I-Z3Z1/users"
#url = "http://192.168.1.216/customers/1H9X-EJNN-7YIP/users"
#url = "http://3.39.12.67:30467/v1/notebooks"

origins = "http://192.168.1.207:32208"

headers = {
    #"Content-Type": "application/x-www-form-urlencoded"
    "Content-Type": "application/json"
}

params = {
    "grant_type": "password",
    "username": "junesu@sdt.inc",
    "password": "Sdt251327!",
    "customerCode": "76U4-BE7I-Z3Z1"
}


params = {
    "namespace": "sklim"
}

# params = {
#     "notebookName": "test5",
#     "namespace": "sdt"
# }


# data = json.dumps({
#     "notebookName": "test2",
#     "namespace": "sklim",
#     "image": "jupyter/datascience-notebook:latest",
#     "cpu": 100,
#     "mem": 250,
#     "volumeName": "workspace1"
# })

# data = json.dumps({
#     "volumeName": "workspace2",
#     "namespace": "sklim"
# })


data = json.dumps({
    "email": "junesu@sdt.inc",
    "password": "Sdt251327!"
})

# data = json.dumps({
#   "code": "SITE-B2C",
#   "name": "b2c",
#   "customerCode": "ZWBC-UZGZ-3GMU"
# })

#print(f"URL = {url}/{method}")
#respeonse = requests.get(f"{url}/{method}/", headers=headers, params=params)
#respeonse = requests.get(f"{url}", headers=headers, params=params)
#respeonse = requests.post(f"{url}", headers=headers, data=data)
#respeonse = requests.post(f"{url}", headers=headers, params=params)
respeonse = requests.get(f"{url}", headers=headers)

print(respeonse.text, flush=True)

