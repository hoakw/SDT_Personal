import time
import json
from kubernetes import client, config
from kubernetes.stream import stream


config.load_kube_config()

k8s_core = client.CoreV1Api()
k8s_app = client.AppsV1Api()

crd_api = client.CustomObjectsApi()

print(type(crd_api))

#node_respones = k8s_core.list_node(label_selector="node-role.kubernetes.io/master")
#master_ip = node_respones.items[0].status.addresses[0].address
#namespace = "fastapi"


gateway_body = {
    "apiVersion": "networking.istio.io/v1alpha3",
    "kind": "Gateway",
    "metadata": {
        "name": "jupyterlab-jlab",
        "namespace": "jlab"
    },
    "spec": {
        "servers" : [{
            "hosts": [
                "sdt.fastapi.com"
            ],
            "port": {
                "name": "http",
                "number": 80,
                "protocol": "HTTP"
            }
        }],
        "selector": {
            "istio": "ingressgateway"
        }
    }
}

virtual_svc_body = {
    "apiVersion": "networking.istio.io/v1alpha3",
    "kind": "VirtualService",
    "metadata": {
        "name": "jupyterlab-jlab",
        "namespace": "jlab"
    },
    "spec": {
        "hosts": ["sdt.fastapi.com"],
        "http" : [{
            "match": [{
                "uri": {
                    "prefix": "/notebook/jlab/jupyterlab/"
                }
            }],
            "route": [{
                "destination": {
                    "host": "jupyterlab.jlab.svc.cluster.local"
                }
            }]
        }],
        "gateways": ["jupyterlab-jlab"]
    }
}





# gw_res = crd_api.create_namespaced_custom_object(
#     group="networking.istio.io",
#     version="v1alpha3",
#     plural="gateways",
#     namespace="jlab",
#     body=gateway_body
# )

# vs_res = crd_api.create_namespaced_custom_object(
#     group="networking.istio.io",
#     version="v1alpha3",
#     plural="virtualservices",
#     namespace="jlab",
#     body=virtual_svc_body
# )

#res = crd_api.list_cluster_custom_object(group="networking.istio.io", version="v1alpha3", plural="gateways")
res = crd_api.list_namespaced_custom_object(group="networking.istio.io", version="v1alpha3", plural="gateways", namespace="sdt")
for gw_info in res['items']:
    print(gw_info['metadata']['name'])

# crd_api.delete_namespaced_custom_object(
#     group="networking.istio.io",
#     version="v1alpha3",
#     plural="gateways",
#     namespace="jlab",
#     name="jupyterlab-jlab"
# )

# crd_api.delete_namespaced_custom_object(
#     group="networking.istio.io",
#     version="v1alpha3",
#     plural="virtualservices",
#     namespace="jlab",
#     name="jupyterlab-jlab"
# )