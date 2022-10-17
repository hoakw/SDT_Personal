#/bin/bash

kubectl delete -f ./manifest/role_binding.yaml
kubectl delete -f ./manifest/sa.yaml
kubectl delete -f ./manifest/status_deployment.yaml
