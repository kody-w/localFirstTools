#!/bin/bash
echo "Starting Minikube..."
minikube start --driver=docker --cpus=2 --memory=4096

echo "Building Docker image..."
eval $(minikube docker-env)
docker build -t level3-k8s:latest .

echo "Deploying to Kubernetes..."
kubectl apply -f deployment.yaml

echo "Waiting for deployment..."
kubectl wait --for=condition=available --timeout=300s deployment/level3-app

echo "Getting service URL..."
minikube service level3-service --url
