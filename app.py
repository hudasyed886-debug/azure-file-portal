import os
from flask import Flask, render_template, request, redirect, url_for
from azure.storage.blob import BlobServiceClient

app = Flask(__name__)

# Debug: Check environment variables
print("DEBUG: Starting Flask app...")
print("DEBUG: AZURE_STORAGE_CONNECTION_STRING exists?", "AZURE_STORAGE_CONNECTION_STRING" in os.environ)
print("DEBUG: AZURE_STORAGE_CONTAINER:", os.getenv('AZURE_STORAGE_CONTAINER'))

# Get connection string from environment variable
connection_string = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
container_name = os.getenv('AZURE_STORAGE_CONTAINER', 'uploads')

if not connection_string:
    print("ERROR: AZURE_STORAGE_CONNECTION_STRING is missing!")

@app.route('/')
def home():
    return "Azure Flask App is Running! Upload functionality will work once connection string is set."

@app.route('/upload', methods=['POST'])
def upload_file():
    if not connection_string:
        return "Azure Storage connection string is not configured."
    
    if 'file' not in request.files:
        return redirect('/')
    
    file = request.files['file']
    if file.filename == '':
        return redirect('/')
    
    # Upload to Azure Blob Storage
    try:
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=file.filename)
        blob_client.upload_blob(file)
        return 'File uploaded successfully! <a href="/">Go back</a>'
    except Exception as e:
        return f'Error: {str(e)}'

if __name__ == '__main__':
    app.run()
