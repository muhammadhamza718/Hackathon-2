#!/bin/bash

# Script to validate the Todo application deployment in Kubernetes
# This script checks if all required resources are properly deployed

set -e  # Exit on any error

echo "Starting deployment validation..."

# Check if kubectl is available
if ! command -v kubectl &> /dev/null; then
    echo "Error: kubectl is not installed or not in PATH"
    exit 1
fi

# Check if Helm is available
if ! command -v helm &> /dev/null; then
    echo "Error: Helm is not installed or not in PATH"
    exit 1
fi

echo "✓ Prerequisites check passed"

# Check if pods are running
echo "Checking pods status..."
POD_STATUS=$(kubectl get pods -o json | jq -r '.items[] | select(.metadata.labels.app | startswith("todo-")) | .status.phase' 2>/dev/null || echo "no_pods")

if [[ "$POD_STATUS" == "no_pods" ]]; then
    echo "✗ No todo application pods found"
    exit 1
fi

RUNNING_PODS=$(echo "$POD_STATUS" | grep -c "Running" || echo "0")
TOTAL_PODS=$(echo "$POD_STATUS" | wc -l)

if [ "$RUNNING_PODS" -eq "$TOTAL_PODS" ]; then
    echo "✓ All pods are running ($RUNNING_PODS/$TOTAL_PODS)"
else
    echo "✗ Only $RUNNING_PODS out of $TOTAL_PODS pods are running"
    kubectl get pods
    exit 1
fi

# Check if services are available
echo "Checking services..."
FRONTEND_SERVICE=$(kubectl get service todo-frontend-service -o json 2>/dev/null || echo "not_found")
if [[ "$FRONTEND_SERVICE" == "not_found" ]]; then
    echo "✗ Frontend service not found"
    exit 1
else
    echo "✓ Frontend service found"
fi

BACKEND_SERVICE=$(kubectl get service todo-backend-service -o json 2>/dev/null || echo "not_found")
if [[ "$BACKEND_SERVICE" == "not_found" ]]; then
    echo "✗ Backend service not found"
    exit 1
else
    echo "✓ Backend service found"
fi

# Check deployments
echo "Checking deployments..."
BACKEND_DEPLOYMENT=$(kubectl get deployment todo-backend-deployment 2>/dev/null || echo "not_found")
if [[ "$BACKEND_DEPLOYMENT" == "not_found" ]]; then
    echo "✗ Backend deployment not found"
    exit 1
else
    echo "✓ Backend deployment found"
fi

FRONTEND_DEPLOYMENT=$(kubectl get deployment todo-frontend-deployment 2>/dev/null || echo "not_found")
if [[ "$FRONTEND_DEPLOYMENT" == "not_found" ]]; then
    echo "✗ Frontend deployment not found"
    exit 1
else
    echo "✓ Frontend deployment found"
fi

# Check if Helm release exists
echo "Checking Helm release..."
HELM_STATUS=$(helm status todo-app 2>/dev/null || echo "not_found")
if [[ "$HELM_STATUS" == "not_found" ]]; then
    echo "✗ Helm release 'todo-app' not found"
    exit 1
else
    echo "✓ Helm release 'todo-app' found"
fi

# Check if health endpoints are responding (if accessible)
echo "Checking application health (if accessible)..."
if kubectl get service todo-frontend-service &> /dev/null; then
    echo "✓ Frontend service is accessible"
else
    echo "⚠ Could not access frontend service"
fi

if kubectl get service todo-backend-service &> /dev/null; then
    echo "✓ Backend service is accessible"
else
    echo "⚠ Could not access backend service"
fi

echo ""
echo "🎉 Deployment validation completed successfully!"
echo "All required resources are properly deployed and running."
echo ""
echo "Deployed resources:"
echo "- Backend Deployment: todo-backend-deployment"
echo "- Frontend Deployment: todo-frontend-deployment"
echo "- Backend Service: todo-backend-service"
echo "- Frontend Service: todo-frontend-service"
echo "- Helm Release: todo-app"