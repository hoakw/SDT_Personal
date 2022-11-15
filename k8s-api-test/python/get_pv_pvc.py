import time
from kubernetes import client, config
from kubernetes.stream import stream


config.load_kube_config()

k8s_core = client.CoreV1Api()
k8s_app = client.AppsV1Api()

#node_respones = k8s_core.list_node(label_selector="node-role.kubernetes.io/master")
#master_ip = node_respones.items[0].status.addresses[0].address
name = "workspace3"
namespace = "sdt"
labels = {"name": "workspace3"}
pv_path = "/mnt/workspace3"

pv_body = client.V1PersistentVolume(
    api_version = "v1",
    kind = "PersistentVolume",
    metadata = client.V1ObjectMeta(
        name = name,
        labels = labels
    ),
    spec = client.V1PersistentVolumeSpec(
        storage_class_name = "manual",
        access_modes = ["ReadWriteMany"],
        capacity = {
            "storage" : "10Gi"
        },
        host_path = client.V1HostPathVolumeSource(
            path = pv_path
        )
    )
)

pvc_body = client.V1PersistentVolumeClaim(
    api_version = "v1",
    kind = "PersistentVolumeClaim",
    metadata = client.V1ObjectMeta(
        name = name,
        labels = labels
    ),
    spec = client.V1PersistentVolumeClaimSpec(
        storage_class_name = "manual",
        access_modes = ["ReadWriteMany"],
        selector = client.V1LabelSelector(match_labels = labels),
        resources = client.V1ResourceRequirements(
            requests = {
                "storage": "10Gi"
            }
        )
    )
)


pv_respone = k8s_core.create_persistent_volume(body=pv_body)
pvc_respone = k8s_core.create_namespaced_persistent_volume_claim(namespace=namespace, body=pvc_body)


pv_list = k8s_core.list_persistent_volume()
pvc_list = k8s_core.list_namespaced_persistent_volume_claim(namespace = namespace)

for pv_info in pv_list.items:
    print(pv_info.metadata.name) 
for pvc_info in pvc_list.items:
    print(pvc_info.metadata.name)

# ns_respones = k8s_core.list_namespace()
# ns_list = []
# for ns_info in ns_respones.items:
#     ns_list.append(ns_info.metadata.name)
# if "test" not in ns_list:
#     ns_body = client.V1Namespace(
#         #api_version = "v1",
#         #kind = "Namespace",
#         metadata = client.V1ObjectMeta(
#             name="test"
#         )
#     )
#     k8s_core.create_namespace(body=ns_body)

# for pod_info in pod_list.items:
#     pod_label = pod_info.metadata.labels["name"]
#     pod_ns = pod_info.metadata.namespace
#     print(f"[Pod] Label Name = {pod_label}")
#     print(f"[Pod] Namespace = {pod_ns}")
#     svc_info = k8s_core.read_namespaced_service(name = pod_label, namespace = pod_ns)
#     svc_name = svc_info.metadata.name
#     svc_ns = svc_info.metadata.namespace

#     svc_port = svc_info.spec.ports[0].node_port
#     print(f"[Service] Name = {svc_name}")
#     print(f"[Service] Namespace = {svc_ns}")
#     print(f"[Service] Internal Address <DNS> = {svc_name}.{svc_ns}.cluster.local")
#     print(f"[Service] External Address = {master_ip}:{svc_port}")

# try:
#     pod_exist = k8s_app.read_namespaced_deployment(name = "fastapi-db-stest", namespace = "fastapi")
# except ApiException as e:
#     print("Not Found")

# print(pod_exist)