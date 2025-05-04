from azure.storage.blob import BlobServiceClient

def upload_to_azure(connection_string, container_name, file_path, blob_name):
    blob_service = BlobServiceClient.from_connection_string(connection_string)
    container_client = blob_service.get_container_client(container_name)
    with open(file_path, "rb") as data:
        container_client.upload_blob(name=blob_name, data=data)
    print(f"Uploaded {file_path} to Azure Blob Storage as {blob_name}")
