from fastapi import APIRouter, HTTPException
import boto3, os
from botocore.exceptions import ClientError

router = APIRouter(prefix="/storage", tags=["Storage"])

AWS_REGION = os.environ["AWS_REGION"]
BUCKET_NAME = os.environ["BUCKET_NAME"]

s3 = boto3.client("s3", region_name=AWS_REGION)

@router.post("/bucket")
def create_buckets():
    try:
        s3.create_bucket(
            Bucket=BUCKET_NAME,
            CreateBucketConfiguration={
                "LocationConstraint": AWS_REGION
            },
        )

        return {
            "message": "S3 bucket created successfully",
            "bucket": BUCKET_NAME,
            "region": AWS_REGION,
        }
    
    except ClientError as e:
        error_code = e.response["Error"]["Code"]

        raise HTTPException(
            status_code=500,
            detail=f"bucket creation error: {error_code}",
        )