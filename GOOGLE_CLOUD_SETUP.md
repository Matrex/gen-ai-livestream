# Google Cloud Credentials Setup

## Background
The RAG (Retrieval-Augmented Generation) application requires Google Cloud credentials to access Vertex AI services.

## Setup Methods

### 1. Using gcloud CLI (Recommended)
```bash
# Install Google Cloud SDK
curl https://sdk.cloud.google.com | bash

# Authenticate
gcloud auth application-default login

# Set your project (replace with your project ID)
gcloud config set project sascha-playground-doit
```

### 2. Service Account Method
1. Create a service account in Google Cloud Console
2. Download the JSON key file
3. Set the environment variable:
```bash
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/service-account-key.json"
```

### 3. Environment Variables
If you know your project details, set these environment variables:
```bash
export GOOGLE_CLOUD_PROJECT=sascha-playground-doit
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account-key.json
```

## Troubleshooting
- Ensure you have the necessary permissions in the Google Cloud project
- Verify the service account has the correct IAM roles
- Check that the credentials file is accessible and not corrupted

## Resources
- [Google Cloud Authentication Documentation](https://cloud.google.com/docs/authentication/external/set-up-adc)
- [Vertex AI Documentation](https://cloud.google.com/vertex-ai/docs/start/client-libraries)

## Note
The RAG Corpus ID used is: 
`projects/sascha-playground-doit/locations/us-central1/ragCorpora/569705352862367744`
