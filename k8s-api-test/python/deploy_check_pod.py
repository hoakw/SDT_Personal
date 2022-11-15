import time
from kubernetes import client, config
from kubernetes.stream import stream


config.load_kube_config()

k8s_core = client.CoreV1Api()
k8s_app = client.AppsV1Api()

### Define Varialbes
## Resource Variables
deploy_apiversion = "apps/v1"
deploy_kind = "Deployment"
service_apiversion = "v1"
service_kind = "Service"

## Object Variables
#name = "nginx-deployment"
name = "test-pvc"
namespace = "sdt"
labels = {"name": "test-pvc"}
image = "jupyter/datascience-notebook:latest"
notebook_home = "/home"

## Network Variables
port = 80
target_port = 8888
node_port = 31241
protocol = "TCP"
network_type = "http"
service_type = "NodePort"

#volume spec
vol_name = "workspace1"
vol_path = "/home/pvc-test"
pvc_name = "workspace1"

## Resource Variables
cpu = 250
mem = 500

## Resource Check
deploy_list = k8s_app.list_namespaced_deployment(namespace = namespace)
for deploy_info in deploy_list.items:
    print(f"deployment Name : {deploy_info.metadata.name}")
    if deploy_info.metadata.name == name:
        print("[Return] Already Deployment!!")

### Manifest 
## Deployment
deployment = client.V1Deployment(
    api_version = "apps/v1",
    kind = "Deployment",
    metadata = client.V1ObjectMeta(
        name=name,
        namespace=namespace, 
        labels= labels
    ),
    spec = client.V1DeploymentSpec(
        replicas = 1,
        selector = client.V1LabelSelector(match_labels = labels),
        template = client.V1PodTemplateSpec(
            metadata = client.V1ObjectMeta(labels = labels),
            spec = client.V1PodSpec(
                containers = [ 
                    client.V1Container(
                        name=name,
                        image=image,
                        ports = [client.V1ContainerPort(container_port = 8888)],
                        command = ["/bin/bash", "-c", f"jupyter lab --notebook-dir={notebook_home} --LabApp.token='' --LabApp.ip='0.0.0.0' --LabApp.allow_root=True --LabApp.allow_root=True"],
                        resources = client.V1ResourceRequirements(requests = {
                            "cpu": "250m", 
                            "memory": "500Mi"
                        })
                    ),
                ],
            ),
        ),
    ),
)

## Service
service = client.V1Service(
    api_version = "v1",
    kind = "Service",
    metadata = client.V1ObjectMeta(
        name = name, 
        namespace = namespace, 
    ),
    spec = client.V1ServiceSpec(
        ports = [client.V1ServicePort(
            port = port, 
            target_port = target_port, 
            protocol = "TCP", 
            name = name,
        )],
        type="NodePort",
        selector = labels,    
    ),
)

### Creating Deployment
deploy_respones = k8s_app.create_namespaced_deployment(namespace = namespace, body = deployment)
#print(deploy_respones.metadata.creation_timestamp)
### Creating Service
service_respones = k8s_core.create_namespaced_service(namespace = namespace, body = service) 

# ### Get Deploy Info
# ## To DO
# ##  - 같은 notebook 이미지를 생성할 경우, Notebook ID는 어떻게 구별할 것 인가?
# time_num = 0
# while True:
#     pod_list = k8s_core.list_namespaced_pod(namespace = namespace)
#     for pod_info in pod_list.items:
#         if name in pod_info.metadata.name:
#             print(f"Pod Name : {pod_info.metadata.name} / Status : {pod_info.status.phase} / HostIP : {pod_info.status.host_ip}")
#             pod_name = pod_info.metadata.name
#             access_ip = pod_info.status.host_ip
#             pod_status = pod_info.status.phase

#     if pod_status == "Running" or time_num == 30:
#         break
    
#     print(f"Pod Name : {pod_info.metadata.name} is {pod_info.status.phase}")
#     time.sleep(3)
#     time_num += 3

# ### Get Service Info
# service_list = k8s_core.list_namespaced_service(namespace = namespace)
# for service_info in service_list.items:
#     if service_info.metadata.name == name:
#         print(f"Service Name : {service_info.metadata.name} / Service Type : {service_info.spec.type} / Service Port : {service_info.spec.ports[0].node_port}")
#         service_name = service_info.metadata.name
#         access_port = service_info.spec.ports[0].node_port

# print(f"Address : {access_ip}:{access_port}")
# print(f"Password : {password}")


# ### Delete Deployment
deploy_delete = k8s_app.delete_namespaced_deployment(name = name, namespace = namespace)
# ### Delete Service
svc_delete = k8s_core.delete_namespaced_service(name = name, namespace = namespace)
print(f"Delete Deployment : {svc_delete.status}")
#print(f"Delete Service : {svc_delete}")


# pod_list = k8s_core.list_namespaced_pod(namespace = "sdt")
# for pod_info in pod_list.items:
#     if pod_info.spec.volumes[0].persistent_volume_claim is not None:
#         print(f"Pod Name : {pod_info.spec.volumes[0].persistent_volume_claim.claim_name}")
