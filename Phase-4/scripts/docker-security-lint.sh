#!/bin/bash

# Docker Security Linting Script
# This script performs basic security checks on Dockerfiles

set -e

echo "Starting Docker security linting..."

# Check if dockerfile_lint is installed, if not use basic checks
if command -v dockerfile_lint &> /dev/null; then
    echo "Using dockerfile_lint for security checks..."

    # Run dockerfile_lint on backend Dockerfile
    echo "Checking backend/Dockerfile..."
    dockerfile_lint -f backend/Dockerfile

    # Run dockerfile_lint on frontend Dockerfile
    echo "Checking frontend/Dockerfile..."
    dockerfile_lint -f frontend/Dockerfile
else
    echo "dockerfile_lint not found, performing basic security checks..."

    # Basic security checks for backend Dockerfile
    echo "Checking backend/Dockerfile for common security issues..."

    # Check if running as root (RUN useradd or USER root issues)
    if grep -E "USER\s+root" backend/Dockerfile; then
        echo "⚠️  Warning: Backend Dockerfile may run as root"
    else
        echo "✓ Backend Dockerfile does not run as root"
    fi

    # Check for non-root user creation
    if grep -E "useradd|adduser" backend/Dockerfile; then
        echo "✓ Backend Dockerfile creates non-root user"
    else
        echo "⚠️  Warning: Backend Dockerfile may not create non-root user"
    fi

    # Check for apt-get clean
    if grep -E "apt-get.*clean" backend/Dockerfile; then
        echo "✓ Backend Dockerfile cleans package cache"
    else
        echo "⚠️  Warning: Backend Dockerfile may not clean package cache"
    fi

    # Basic security checks for frontend Dockerfile
    echo "Checking frontend/Dockerfile for common security issues..."

    # Check if running as root
    if grep -E "USER\s+root" frontend/Dockerfile; then
        echo "⚠️  Warning: Frontend Dockerfile may run as root"
    else
        echo "✓ Frontend Dockerfile does not run as root"
    fi

    # Check for non-root user creation
    if grep -E "adduser|addgroup" frontend/Dockerfile; then
        echo "✓ Frontend Dockerfile creates non-root user"
    else
        echo "⚠️  Warning: Frontend Dockerfile may not create non-root user"
    fi

    # Check for npm cache clean
    if grep -E "npm cache clean" frontend/Dockerfile; then
        echo "✓ Frontend Dockerfile cleans npm cache"
    else
        echo "⚠️  Warning: Frontend Dockerfile may not clean npm cache"
    fi
fi

# Additional security best practices checks
echo "Checking for additional security best practices..."

# Check .dockerignore files exist
if [ -f "backend/.dockerignore" ] && [ -f "frontend/.dockerignore" ]; then
    echo "✓ .dockerignore files exist for both applications"
else
    echo "⚠️  Warning: .dockerignore files may be missing"
fi

# Check for multi-stage builds
if grep -E "FROM.*as.*builder" backend/Dockerfile; then
    echo "✓ Backend Dockerfile uses multi-stage build"
else
    echo "⚠️  Warning: Backend Dockerfile may not use multi-stage build"
fi

if grep -E "FROM.*as.*builder" frontend/Dockerfile; then
    echo "✓ Frontend Dockerfile uses multi-stage build"
else
    echo "⚠️  Warning: Frontend Dockerfile may not use multi-stage build"
fi

echo ""
echo "Docker security linting completed!"
echo "Note: For more comprehensive security scanning, consider using tools like:"
echo "- docker run --rm -v \$(pwd):/root/ -w /root/ projectatomic/dockerfile-lint dockerfile_lint -f backend/Dockerfile"
echo "- docker run --rm -v /var/run/docker.sock:/var/run/docker.sock -v \$(pwd):/data:ro docker/dockerfile:latest FROM backend/Dockerfile"
echo "- Hadolint: hadolint backend/Dockerfile"