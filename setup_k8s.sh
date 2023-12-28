#/bin/bash

kubectl create secret generic db-login --from-literal=db_user=$DB_USER --from-literal=db_password=$DB_PASSWORD
kubectl apply -f kubernetes/movies-api/deployment.yaml 
sleep 45
minikube service movie-data-service 
