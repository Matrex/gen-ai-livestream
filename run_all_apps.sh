#!/bin/bash

# Function to run a Streamlit app in the background
run_streamlit_app() {
    local app_path=$1
    local port=$2
    echo "Starting Streamlit app: $app_path on port $port"
    cd "$(dirname "$app_path")"
    
    # Special handling for RAG UI to provide credential guidance
    if [[ "$app_path" == *"rag-api/ui/app.py"* ]]; then
        echo "⚠️ WARNING: Google Cloud credentials are required for the RAG UI"
        echo "Please refer to GOOGLE_CLOUD_SETUP.md for setup instructions"
    fi
    
    streamlit run --server.port "$port" "$(basename "$app_path")" &
    cd - > /dev/null
}

# List of Streamlit apps with their respective ports
declare -A apps=(
    ["rag-api/ui/app.py"]=8501
    ["document-processing/ui/app.py"]=8502
    ["use-cases/artist-matching/app.py"]=8503
    ["use-cases/product-taxonomy/app.py"]=8504
    ["secure/prompt-guard/ui/app.py"]=8505
    ["code-assistant/analyze/service/app.py"]=8506
)

# Run all apps
for app_path in "${!apps[@]}"; do
    run_streamlit_app "$app_path" "${apps[$app_path]}"
done

# Wait for all background processes
wait

echo "All Streamlit apps have been launched."
echo "Note: Some apps may require additional configuration or credentials."
