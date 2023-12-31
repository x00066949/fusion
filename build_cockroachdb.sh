#/bin/bash

minikube start  --cpus 4
helm repo add cockroachdb https://charts.cockroachdb.com/
helm repo update
helm install my-release --values kubernetes/cockroachdb/my-values.yaml cockroachdb/cockroachdb
kubectl create -f kubernetes/cockroachdb/client-secure.yaml

sleep 60

kubectl exec -it cockroachdb-client-secure -- ./cockroach sql --certs-dir=./cockroach-certs --host=my-release-cockroachdb-public