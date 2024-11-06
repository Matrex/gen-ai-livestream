# Generative AI Livestream - All Applications

## Overview
This project contains multiple Streamlit applications across different AI and machine learning domains.

## Applications

1. **RAG (Retrieval-Augmented Generation) UI**
   - Port: 8501
   - Path: `rag-api/ui/app.py`

2. **Document Processing UI**
   - Port: 8502
   - Path: `document-processing/ui/app.py`

3. **Artist Matching UI**
   - Port: 8503
   - Path: `use-cases/artist-matching/app.py`

4. **Product Taxonomy UI**
   - Port: 8504
   - Path: `use-cases/product-taxonomy/app.py`

5. **Prompt Guard UI**
   - Port: 8505
   - Path: `secure/prompt-guard/ui/app.py`

6. **Code Assistant UI**
   - Port: 8506
   - Path: `code-assistant/analyze/service/app.py`

## Prerequisites
- Python 3.9+
- Virtual environment activated
- All dependencies installed via `setup.sh`

## Running Applications

### Single Command to Run All Apps
```bash
./run_all_apps.sh
```

### Accessing Applications
After running the script, access the UIs at:
- RAG UI: http://localhost:8501
- Document Processing UI: http://localhost:8502
- Artist Matching UI: http://localhost:8503
- Product Taxonomy UI: http://localhost:8504
- Prompt Guard UI: http://localhost:8505
- Code Assistant UI: http://localhost:8506

## Notes
- Some applications may require API keys or additional configuration
- Check individual `.env.sample` files in each service directory
- You may need to set up specific credentials for Google Cloud or other services

## Troubleshooting
- Ensure virtual environment is activated
- Check that all dependencies are installed
- Verify network ports are available
