#!/bin/bash

# Check if nvidia-smi is available
if command -v nvidia-smi > /dev/null 2>&1; then
    echo "nvidia-smi is available. Running docker-compose.gpu.yml"
    docker-compose -f docker-compose.yml -f docker-compose.gpu.yml up -d
else
    echo "nvidia-smi is not available. Running docker-compose.yml"
    docker-compose up -d
fi
