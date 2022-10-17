import numpy as np
import pandas as pd
import streamlit as st
import requests
import json

import time


class Calculation():
    def __init__(self, url_info):
        self.url = f"http://{url_info}"


    def create_notebook(self, notebook_data: dict):
        #url = f"http://{svc_name}.{svc_namespace}.svc.cluster.local"
        method = "v1/notebooks/create"

        headers = {
            "Content-Type": "application/json"
        }

        params = {
            "namespace": notebook_data['namespace']
        }


        data = json.dumps({
            "notebook_name": notebook_data['name'],
            "namespace": notebook_data['namespace'],
            "image": notebook_data['image'],
            "label": notebook_data['name'],
            "cpu": notebook_data['cpu'],
            "mem": notebook_data['mem'],
            "gpu": 0,
            "password": notebook_data['password']
        })

        respeonse = requests.post(f"{self.url}/{method}/", headers=headers, data=data)
        print(respeonse.text, flush=True)

    def get_notebook_list(self, namespace: str):
        print("[SDT] Get List of notebook!!!")
        ### Get Deploy Info
        ## To DO
        ##  - 같은 notebook 이미지를 생성할 경우, Notebook ID는 어떻게 구별할 것 인가?
        ##  - labels의 값에는 꼭 name이 아니라 app 여러가지가 나올수가 있음... 어떻게 처리할 것인가?
        #url = f"http://{svc_name}.{svc_namespace}.svc.cluster.local"
        method = "v1/notebooks"

        headers = {
            "Content-Type": "application/json"
        }

        params = {
            "namespace": namespace
        }

        respeonse = requests.get(f"{self.url}/{method}/", headers=headers, params=params)
        print(respeonse.text, flush=True)
        print(type(respeonse.text), flush=True)

        return json.loads(respeonse.text)

    def delete_notebook(self, name: str, namespace: str):
        method = "v1/notebooks/delete{nodebook_id}"

        headers = {
            "Content-Type": "application/json"
        }

        params = {
            "notebook_name": name,
            "namespace": namespace
        }

        respeonse = requests.delete(f"{self.url}/{method}/", headers=headers, params=params)
        print(respeonse.text, flush=True)
