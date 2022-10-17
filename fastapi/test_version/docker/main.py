from fastapi import FastAPI
from kubernetes import client, config

app = FastAPI()

@app.get("/")
async def get_pod():
    print("[SDT] GET Pod Info")
    
    ### 외부에서 접근할때, config 파일이 있어야함
    #config.load_kube_config()
    
    ### Pod 내부에서 접근할 때
    config.load_incluster_config()
    v1 = client.CoreV1Api()

    ret = v1.list_pod_for_all_namespaces()
    for i in ret.items:
        print(f"[SDT] {i.status.pod_ip} / {i.metadata.namespace} / {i.metadata.name}")
    return {"message":f"Pod Name = {i.metadata.name}"}

