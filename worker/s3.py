from minio import Minio
import os
from minio.error import S3Error
from dotenv import load_dotenv
load_dotenv()

# Replace these with your AWS credentials and S3 bucket and file information
S3_ACCESS_KEY = os.environ.get("S3_KEY_ID")
S3_SECRET_KEY = os.environ.get("S3_SECRET_KEY")
S3_HOST = os.environ.get("S3_HOST")
S3_SECURE = os.environ.get("S3_SECURE")

class S3:
    def __init__(self, bucket_name):
        self.bucket_name = bucket_name
        self.access_key = S3_ACCESS_KEY
        self.secret_key = S3_SECRET_KEY
        self.host = S3_HOST
        self.secure = S3_SECURE
        
        # Initialize Minio client
        self.client = Minio(
            self.host,
            access_key=self.access_key,
            secret_key=self.secret_key,
            secure=self.secure
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

    def upload_file(self, local_file_path, file_key):
        try:
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
