from fastapi import APIRouter, HTTPException, UploadFile, File, Form, HTTPException
import boto3, os, uuid
from botocore.exceptions import ClientError
from db import models

router = APIRouter(prefix="/storage", tags=["Storage"])

AWS_REGION = os.environ["AWS_REGION"]
BUCKET_NAME = os.environ["BUCKET_NAME"]

s3 = boto3.client("s3", region_name=AWS_REGION)


@router.post("/buckets")
def create_buckets(payload: models.BucketCreate):
    bucket_name = payload.bucket_name or BUCKET_NAME

    try:
        s3.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={"LocationConstraint": AWS_REGION},
        )

        return {
            "message": "S3 bucket created successfully",
            "bucket": bucket_name,
            "region": AWS_REGION,
        }

    except ClientError as e:
        error_code = e.response["Error"]["Code"]

        raise HTTPException(
            status_code=500,
            detail=f"bucket creation error: {error_code}",
        )


@router.post("/images")
def upload_images(
    file: UploadFile = File(...),
    bucket_name: str = Form(...),
):
    allowed_types = {
        "image/jpeg": ".jpg",
        "image/png": ".png",
        "image/webp": ".webp",
    }

    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail="Only JPEG, PNG, and WebP images are allowed.",
        )

    image_key = f"{uuid.uuid4()}{allowed_types[file.content_type]}"

    try:
        s3.upload_fileobj(
            file.file,
            bucket_name,
            image_key,
            ExtraArgs={"ContentType": file.content_type},
        )
        return {"image_key": image_key}

    except ClientError:
        raise HTTPException(
            status_code=500,
            detail="Failed to upload image to S3",
        )

    finally:
        file.close()
