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
name = "fastapi-pod-crud"
namespace = "fastapi-system"
labels = {"name": "nginx"}
image = "nginx"

## Network Variables
port = 80
target_port = 8888
node_port = 31241
protocol = "TCP"
network_type = "http"
service_type = "NodePort"

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
        name="nginx-deployment",
        namespace="default", 
        labels= {"app": "nginx"}
    ),
    spec = client.V1DeploymentSpec(
        replicas = 3,
        selector = client.V1LabelSelector(match_labels = {"app": "nginx"}),
        template = client.V1PodTemplateSpec(
            metadata = client.V1ObjectMeta(labels = {"app": "nginx"}),
            spec = client.V1PodSpec(
                containers = [ 
                    client.V1Container(
                        name="nginx",
                        image="nginx",
                        ports = [client.V1ContainerPort(container_port = 80)],
                        resources = client.V1ResourceRequirements(requests = {
                            "cpu": "250m", 
                            "memory": "500Mi"
                        }),
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
        name = "nginx-service", 
        namespace = "default", 
    ),
    spec = client.V1ServiceSpec(
        ports = [client.V1ServicePort(
            port = 8080, 
            target_port = 80, 
            protocol = "TCP", 
            name = "nginx-service",
        )],
        selector = {"app": "nginx"},    
    ),
)

### Creating Deployment
#deploy_respones = k8s_app.create_namespaced_deployment(namespace = "default", body = deployment)
### Creating Service
#service_respones = k8s_core.create_namespaced_service(namespace = "default", body = service) 

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
#deploy_delete = k8s_app.delete_namespaced_deployment(name = name, namespace = namespace)
# print(f"Delete Deployment : {deploy_delete.status}")
# ### Delete Service
#svc_delete = k8s_core.delete_namespaced_service(name = "nginx-service", namespace = namespace)
# print(f"Delete Service : {svc_delete}")


# pod_list = k8s_core.list_namespaced_pod(namespace = "default")
# for pod_info in pod_list.items:
#     print(f"Pod Name : {pod_info.metadata.name}")
