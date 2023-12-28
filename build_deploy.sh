#/bin/bash

docker build --pull --no-cache -f docker/Dockerfile -t movies-data:latest app
docker tag movies-data:latest us-central1-docker.pkg.dev/sentinel-core/mov-api/movie-python:latest
docker push us-central1-docker.pkg.dev/sentinel-core/mov-api/movie-python
kubectl delete -f kubernetes/movies-api/deployment.yaml 
kubectl apply -f kubernetes/movies-api/deployment.yaml 
minikube service movie-data-service 