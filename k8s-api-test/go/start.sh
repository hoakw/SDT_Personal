#/bin/bash

kubectl apply -f ./manifest/role_binding.yaml
kubectl apply -f ./manifest/sa.yaml
kubectl apply -f ./manifest/status_deployment.yaml
