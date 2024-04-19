from minio import Minio
import os
from minio.error import S3Error

# Replace these with your AWS credentials and S3 bucket and file information
aws_access_key_id = 'oJTJnZIz0lJ8RblZMLbb'
aws_secret_access_key = 'nyAeRaWm1vo9mBBwgKqhLzP1Yjws7V5IpVrfKPEe'
host = "144.91.123.186:32771"
secure = False

class S3:
    access_key : str
    secret_key : str
    bucket_name : str
    host : str
    secure : bool
    client : Minio

    def __init__(self,bucket_name):
        self.access_key = aws_access_key_id
        self.secret_key = aws_secret_access_key
        self.bucket_name = bucket_name
        self.host = host
        self.secure = secure
        self.client = Minio(self.host,
            access_key=self.access_key,
            secret_key=self.secret_key,
            secure=self.secure
        )

    def download_file(self,file_key, local_file_path):
        try:
            with open(local_file_path, 'wb+') as file_data:
                # Get the object as a stream
                object_data = self.client.get_object(self.bucket_name, file_key)
                
                # Read from the object stream and write to the local file
                for data in object_data.stream(32 * 1024):  # Adjust buffer size as needed
                    file_data.write(data)
            
            print(f"File downloaded successfully to {local_file_path}")
        except Exception as e:
            print(f"Error downloading file: {e}")
            exit()

    def upload_file(self,file_key, file_s3_name):
        try:
            os.chdir("temp/")
            self.client.fput_object(
                    self.bucket_name, file_key, file_s3_name,
            )
            print(f"File uploaded successfully to S3 key: {file_key}")
            os.chdir("..")
        except Exception as e:
            print(f"Error uploading file: {e}")

    def remove_file(self,file_key):
        try:
            self.client.remove_object(self.bucket,file_key)
            print(f"File '{file_key}' deleted from bucket '{self.bucket}'")

        except S3Error as e:
            print(f"An error occurred: {e}")

# Uncomment the following lines to use the download and upload functions
# download_file(file_key, local_file_path)
# upload_file(file_key, local_file_path)
