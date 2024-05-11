from lists3 import *
import os
from s3 import S3

apikey = os.environ.get("API_KEY")

thumbnails_bucket = "thumbnails"
s3_minia = S3(thumbnails_bucket)

s3_minia.upload_file("temp/input2.jpg")