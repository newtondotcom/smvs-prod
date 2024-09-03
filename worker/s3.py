from minio import Minio
import os
from lists3 import *
from minio.error import S3Error
from dotenv import load_dotenv
load_dotenv()

class S3:
    def __init__(self, s3name):
        bucket = get_s3(s3name)
        self.host = bucket['endpoint'].strip()
        self.port = bucket['port']
        self.secure = bucket['ssl']
        self.access_key = bucket['access_key'].strip()
        self.secret_key = bucket['secret_key'].strip()
        self.bucket_name = bucket['bucket'].strip()
        
        # Initialize Minio client
        self.client = Minio(
            self.host + ":" + str(self.port),
            access_key=self.access_key,
            secret_key=self.secret_key,
            secure=self.secure,
            region='us-east-1'
        )

    def download_file(self, file_key, local_file_path):
        try:
            # Ensure the local directory exists
            os.makedirs(os.path.dirname(local_file_path), exist_ok=True)

            # Download object to local file
            self.client.fget_object(self.bucket_name, file_key, local_file_path)
            print(f"File downloaded successfully to {local_file_path}")
        except Exception as e:
            print(f"Error downloading file: {e}")

    def upload_file(self, file_key):
        try:        
            local_file_path = file_key
            # Upload local file to the bucket without storing in a temp folder
            # Remove the 'temp/' prefix from the file_key
            file_key = file_key.replace('temp/', '')
            # Upload local file to the bucket
            self.client.fput_object(self.bucket_name, file_key, local_file_path)
            return self.host + "/" + self.bucket_name + "/" + file_key
            print(f"File uploaded successfully to S3 key: {file_key}")
        except Exception as e:
            print(f"Error uploading file: {e}")

    def remove_file(self, file_key):
        try:
            # Remove object from the bucket
            self.client.remove_object(self.bucket_name, file_key)
            print(f"File '{file_key}' deleted from bucket '{self.bucket_name}'")
        except S3Error as e:
            print(f"An error occurred: {e}")

# Uncomment the following lines to use the download and upload functions
# download_file(file_key, local_file_path)
# upload_file(file_key, local_file_path)
