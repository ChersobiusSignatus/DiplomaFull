import os
import boto3

# Load AWS credentials from environment variables
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")

# Initialize S3 client
s3_client = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION
)

# Test image data (replace with a real image file)
image_path = "test_image.jpg"
if not os.path.exists(image_path):
    with open(image_path, "wb") as f:
        f.write(b"\xFF\xD8\xFF")  # Creates a small JPEG file

try:
    # Upload image to S3
    s3_client.upload_file(image_path, S3_BUCKET_NAME, "test_upload.jpg")
    print(f"✅ Successfully uploaded '{image_path}' to AWS S3!")

    # Verify uploaded files
    response = s3_client.list_objects_v2(Bucket=S3_BUCKET_NAME)
    files = [obj["Key"] for obj in response.get("Contents", [])]
    print("📂 Files in bucket:", files)

except Exception as e:
    print(f"❌ Upload failed: {e}")
