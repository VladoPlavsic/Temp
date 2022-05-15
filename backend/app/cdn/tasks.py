import os
from fastapi import FastAPI
import boto3
from botocore.client import Config
from app.core.config import AWS_SECRET_KEY_ID, AWS_SECRET_ACCESS_KEY, CDN_ENDPOINT_URL, BOTO3_CONNECTION_TIMEOUT, BOTO3_CONNECTION_MAX_ATTEMPTS
import logging

logger = logging.getLogger(__name__)

async def connect_to_cdn(app: FastAPI) -> None:
    try:
        config = Config(connect_timeout=BOTO3_CONNECTION_TIMEOUT, retries={'max_attempts': BOTO3_CONNECTION_MAX_ATTEMPTS})

        client = boto3.client(
            service_name='s3',
            endpoint_url=CDN_ENDPOINT_URL,
            aws_access_key_id=AWS_SECRET_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            aws_session_token=None,
            region_name=None,
            config=config,
            )

        app.state._cdn_client = client

    except Exception as e:
        logger.warn("--- s3 CONNECTION ERROR ---")
        logger.warn(e)
        logger.warn("--- s3 CONNECTION ERROR ---")
