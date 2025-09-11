#!/bin/bash
echo "Creating Lambda deployment package..."
zip lambda.zip lambda_function.py

echo "Starting LocalStack..."
docker-compose up -d

echo "Waiting for LocalStack to be ready..."
sleep 10

echo "Initializing Terraform..."
docker-compose exec terraform terraform init

echo "Applying Terraform configuration..."
docker-compose exec terraform terraform apply -auto-approve

echo "Cloud simulation ready!"
echo "LocalStack Dashboard: http://localhost:3006"
echo "Services endpoint: http://localhost:4566"
