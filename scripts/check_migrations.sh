#!/bin/bash

CONTAINER_NAME="project_name-dc01"

# Check if the Django container is running
if docker ps --filter "name=${CONTAINER_NAME}" --filter "status=running" | grep -q "${CONTAINER_NAME}"; then
    # If running, execute the check
    docker exec "${CONTAINER_NAME}" python manage.py makemigrations --check --dry-run
else
    # Otherwise, print a warning and exit
    echo "WARNING: Django container not running. Skipping migrations check."
    exit 0
fi
