from fastapi import FastAPI, Request
from kubernetes import client, config

#from app.api.api_v1.api import api_router
#from app.core.config import settings


tags_metadata = [
    {
        'name': 'notebook-fastapi',
        'description': 'Notebook creator'
    }
]

app = FastAPI(
    openapi_tags = tags_metadata,
    swagger_ui_parametes={"defaultModelsExpandDepth": -1}
)


#async def get_pod_list(*, request: Request):
# openapi_extra -> Description 프런트 개발자와 맞추기 위한 type spec 정의
@app.post("/create", openapi_extra = {
    "requestBody": {
        "content": {
            "application/json": {
                "schema": {
                    "type": "object",
                    "properties": {
                        "notebook_id": {
                            "description": "Name",
                            "type": "string"
                        },
                        "notebook_img": {
                            "descripition": "Notebook Image Name",
                            "type": "string"
                        },
                        "request_cpu": {
                            "descripition": "Request CPU Size",
                            "type": "float"
                        },
                        "request_mem": {
                            "description": "Request Memory Size",
                            "type": "float"
                        }
                    }
                }
            }
        }
    }
})
async def create_notebook(request: Request):
    contents = await request.json()
    notebook_id = contents.get('notebook_id')
    notebook_img = contents.get('notebook_img')
    notebook_cpu = contents.get('notebook_cpu')
    notebook_mem = contents.get('notebook_mem')
    print(f"Notebook ID : f{notebook_id}")
    print(f"Notebook Image : f{notebook_img}")
    print(f"Notebook CPU : f{notebook_cpu}")
    print(f"Notebook Memory : f{notebook_mem}")
    print(f"[SDT Notbeook Creating] Creating {notebook_id}... ")

    
    config.load_incluster_config()
    k8s_core = client.CoreV1Api()
    k8s_app = client.AppsV1Api()
    
    
        
    ### Define Varialbes
    ## Resource Variables
    deploy_apiversion = "apps/v1"
    deploy_kind = "Deployment"
    service_apiversion = "v1"
    service_kind = "Service"

    ## Object Variables
    name = "jupyterlab"
    namespace = "sdt"
    labels = {"name": "jupyterlab"}
    image = "jupyter/datascience-notebook:latest"
    password = "sdt"

    ## Network Variables
    port = 80
    target_port = 8888
    node_port = 32250
    protocol = "TCP"
    network_type = "http"
    service_type = "NodePort"

    ## Resource Variables
    cpu = 250
    mem = 500

    ### Manifest 
    ## Deployment
    deployment = client.V1Deployment(
        # apiVersion
        api_version = deploy_apiversion,
        # kind
        kind = deploy_kind,
        # metadata
        metadata = client.V1ObjectMeta(
            name=name,
            #namespace="sdt", 
            labels=labels
        ),
        # spec
        spec = client.V1DeploymentSpec(
            replicas = 1,
            selector = client.V1LabelSelector(match_labels = labels),
            template = client.V1PodTemplateSpec(
                metadata = client.V1ObjectMeta(labels = labels),
                spec = client.V1PodSpec(
                    containers = [ 
                        client.V1Container(
                            security_context = client.V1PodSecurityContext(run_as_user = 0, fs_group = 0),
                            name=name,
                            image=image,
                            ports = [client.V1ContainerPort(container_port = target_port)],
                            command = ["/bin/bash", "-c", f"start.sh jupyter lab --LabApp.token='{password}' --LabApp.ip='0.0.0.0' --LabApp.allow_root=True"],
                            resources = client.V1ResourceRequirements(requests = {"cpu": f"{cpu}m", "memory": f"{mem}Mi"}),
                        ),
                    ],
                    restart_policy = "Always"
                ),
            ),
        ),
    )

    ## Service
    service = client.V1Service(
        # apiVersion
        api_version = service_apiversion,
        # kind
        kind = service_kind,
        # metadata
        metadata = client.V1ObjectMeta(
            name = name, 
            #namespace = "sdt", 
            labels = labels,
        ),
        # spec
        spec = client.V1ServiceSpec(
            type = service_type,
            ports = [client.V1ServicePort(
                port = port, 
                target_port = target_port, 
                protocol = protocol, 
                name = network_type,
                node_port = node_port,
            )],
            selector = labels,    
        ),
    )

    ### Creating Deployment
    deploy_respones = k8s_app.create_namespaced_deployment(namespace = namespace, body = deployment)
    ### Creating Service
    service_respones = k8s_core.create_namespaced_service(namespace = namespace, body = service) 

    print(f"Respones : {deploy_respones}  / {service_respones}")

    ### Get Deploy Info
    pod_list = k8s_core.list_namespaced_pod(namespace=namespace)
    service_list = k8s_core.list_namespaced_service(namespace=namespace)
    for pod_info in pod_list.items:
        if name in pod_info.metadata.name:
            print(f"Pod Name : {pod_info.metadata.name} / Status : {pod_info.status.phase} / HostIP : {pod_info.status.host_ip}")
            pod_name = pod_info.metadata.name
            access_ip = pod_info.status.host_ip
    for service_info in service_list.items:
        if service_info.metadata.name == name:
            print(f"Service Name : {service_info.metadata.name} / Service Type : {service_info.spec.type} / Service Port : {service_info.spec.ports[0].node_port}")
            service_name = service_info.metadata.name
            access_port = service_info.spec.ports[0].node_port

    print(f"Address : {access_ip}:{access_port}")
    print(f"Password : {password}")


    return { "message":f"Notebook ID = {notebook_id} / Notebook Image = {notebook_img} / Notebook CPU = {notebook_cpu} / Notebook Memory = {notebook_mem}" }

@app.get("/list")
async def get_pod_list():
    config.load_incluster_config()
    v1 = client.CoreV1Api()

    ret = v1.list_pod_for_all_namespaces()
    pod_list = ""
    for i in ret.items:
         pod_list += f"{i.status.pod_ip} / {i.metadata.namespace} / {i.metadata.name} \n"
    
    return {"message":f"{pod_list}"}


#app.include_router(api_router, prefix=settings.API_V1_STR)
