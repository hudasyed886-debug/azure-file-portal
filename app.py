from flask import Flask, render_template, request, redirect, url_for
import os
from azure.storage.blob import BlobServiceClient

app = Flask(__name__)

# Get connection string from environment variable
connection_string = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
container_name = os.getenv('AZURE_STORAGE_CONTAINER', 'uploads')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect('/')
    
    file = request.files['file']
    if file.filename == '':
        return redirect('/')
    
    # Upload to Azure Blob Storage
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=file.filename)
    blob_client.upload_blob(file)
    
    return 'File uploaded successfully! <a href="/">Go back</a>'

if __name__ == '__main__':
    app.run()