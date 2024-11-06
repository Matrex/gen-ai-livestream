#!/bin/bash

# Generative AI Livestream Project Setup Script

set -e

# Ensure Python 3.9+ is available
python3 --version
if [ $? -ne 0 ]; then
    echo "Python 3.9+ is required. Please install it first."
    exit 1
fi

# Create a virtual environment
python3 -m venv genai_env
source genai_env/bin/activate

# Function to install requirements for a specific directory
install_requirements() {
    local dir="$1"
    if [ -f "$dir/requirements.txt" ]; then
        echo "Installing requirements for $dir"
        pip install -r "$dir/requirements.txt"
    fi
}

# Install requirements for key services
services=(
    "rag-api/ui"
    "rag-api/confluence"
    "document-processing/ui"
    "document-processing/cloud-run-service"
    "code-assistant/analyze/service"
    "podcast-automation"
    "secure/prompt-guard/ui"
    "secure/prompt-guard/guard-service"
    "use-cases/artist-matching"
    "use-cases/product-taxonomy"
    "slack/bot"
)

for service in "${services[@]}"; do
    install_requirements "$service"
done

# Copy .env.sample files to .env if .env doesn't exist
find . -name ".env.sample" | while read -r env_sample; do
    env_file=$(dirname "$env_sample")/.env
    if [ ! -f "$env_file" ]; then
        cp "$env_sample" "$env_file"
        echo "Created $env_file from sample"
    fi
done

echo "Setup complete! Activate the virtual environment with 'source genai_env/bin/activate'"
