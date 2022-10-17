import os
import time
import datetime
from bs4 import BeautifulSoup
#from kubernetes import client, config
#from kfserving import KFServingClient


class GetAuthkey():
    def __init__(self, node_ip="192.168.100.186", node_port="30890"):
        self.node_ip = node_ip
        self.node_port = node_port


    def strTodict(self, req_data):
        soup = BeautifulSoup(req_data, 'html.parser')
        result_dict = {}
        links = soup.find_all('a') # 모든 a 태그 추출

        cell_line = []
        for i in links:
            href = i.attrs['href']
            cell_line.append(href)
        
        
        print(f"[Debug] {cell_line}")
        arr_val = cell_line[0].split("&") 
        for values in arr_val:
            arr_data = values.split("=")
            keys = arr_data[0]
            vals = arr_data[1]
            if keys not in result_dict:
                result_dict[keys] = vals

        return result_dict

    def get_authKey(self, str_data):
        lines = str_data.split("\n")
        for line in lines:
            if "authservice_session" in line:
                word = line.split(";")
                vals = word[0].split("=")
                return vals[1]
        return ""

    def get_key(self):
        # 1) 
        """
        config.load_kube_config()

        v1 = client.CoreV1Api()
        ret = v1.list_namespaced_service("istio-system", watch=False)
        #ret = v1.list_service_for_all_namespaces(watch=False)
        for i in ret.items:
            if i.metadata.name == "istio-ingressgateway":
                print(f"{i.spec.cluster_ip}")
                target_cluster_ip = i.spec.cluster_ip
        """
        url_home = f"http://{self.node_ip}:{self.node_port}"
        #1.
        result = os.popen(f"curl {url_home}").read()
        result_dict = self.strTodict(result)

        print(f"[Number 1] state_key={result_dict['state']}", flush=True)
        state_key = result_dict['state']


        #2.
        url_name = f'"{url_home}/dex/auth?client_id=kubeflow-oidc-authservice&redirect_uri=%2Flogin%2Foidc&response_type=code&scope=profile+email+groups+openid&amp;state={state_key}"'
        result = os.popen(f"curl {url_name}").read()
        result_dict = self.strTodict(result)

        req_key = result_dict["/dex/auth/local?req"]

        print(f"[Number 2] req_key={req_key}", flush=True)

        #3
        url_name = f"'{url_home}/dex/auth/local?req={req_key}' -H 'Content-Type: application/x-www-form-urlencoded' --data 'login=user%40mobiis.com&password=MLteam0719$$'"

        result = os.popen(f"curl {url_name}")
        print(f"[Number 3-1] login_result = {result}", flush=True)

        time.sleep(0.5)
        url_name = f'"{url_home}/dex/approval?req={req_key}"'
        result = os.popen(f"curl {url_name}").read()
        print(f"[Number 3-2] get id token result ={result}", flush=True)
        result_dict = self.strTodict(result)
        state_key = result_dict["state"]
        code_key = result_dict["/login/oidc?code"]


        url_name = f'"{url_home}/login/oidc?code={code_key}&amp&amp;state={state_key}"'
        result = os.popen(f"curl -v -i {url_name}").read()
        auth_key = self.get_authKey(result)
        
        now_time = datetime.datetime.now()

        return auth_key, now_time

        """
        h_header = {
            "Cookie": f"authservice_session={auth_key}", 
            "Host": "kfserving-custom-model.user.example.com",
        }

        url_name = "http://192.168.100.184:30890/v1/models/kfserving-custom-model:predict"

        h_data = {
            'gene': 'ASD',
            'sequence': 'FGASTSTASD',
            'case': '1'
        }
        result = requests.post(url_name, headers=h_header, data=json.dumps(h_data)).json()
        print(result)
        #result_df = pd.DataFrame(result)
        """