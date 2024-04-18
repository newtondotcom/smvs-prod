from minio import Minio
import os
from minio.error import S3Error

# Replace these with your AWS credentials and S3 bucket and file information
aws_access_key_id = 'oJTJnZIz0lJ8RblZMLbb'
aws_secret_access_key = 'nyAeRaWm1vo9mBBwgKqhLzP1Yjws7V5IpVrfKPEe'

class S3:
    access_key : str
    secret_key : str
    bucket_name : str

    def __init__(self, access_key, secret_key, bucket_name):
        self.access_key = access_key
        self.secret_key = secret_key
        self.bucket_name = bucket_name

    def download_file(file_key, local_file_path, bucket_name):
        try:
            client = Minio("144.91.123.186:32771",
                access_key=aws_access_key_id,
                secret_key=aws_secret_access_key,
                secure=False
            )
            
            with open(local_file_path, 'wb+') as file_data:
                # Get the object as a stream
                object_data = client.get_object(bucket_name, file_key)
                
                # Read from the object stream and write to the local file
                for data in object_data.stream(32 * 1024):  # Adjust buffer size as needed
                    file_data.write(data)
            
            print(f"File downloaded successfully to {local_file_path}")
        except Exception as e:
            print(f"Error downloading file: {e}")
            exit()

    def upload_file(file_key, file_s3_name,bucket_name):
        try:
            os.chdir("temp/")
            client = Minio("144.91.123.186:32771",
                    access_key=aws_access_key_id,
                    secret_key=aws_secret_access_key,
                    secure=False
            )
            client.fput_object(
                    bucket_name, file_key, file_s3_name,
            )
            print(f"File uploaded successfully to S3 key: {file_key}")
            os.chdir("..")
        except Exception as e:
            print(f"Error uploading file: {e}")

    def remove_file(bucket,file_key):
        try:
            client = Minio("144.91.123.186:32771",
                    access_key=aws_access_key_id,
                    secret_key=aws_secret_access_key,
                    secure=False
            )
            client.remove_object(bucket,file_key)
            print(f"File '{file_key}' deleted from bucket '{bucket}'")

        except S3Error as e:
            print(f"An error occurred: {e}")

# Uncomment the following lines to use the download and upload functions
# download_file(file_key, local_file_path)
# upload_file(file_key, local_file_path)
