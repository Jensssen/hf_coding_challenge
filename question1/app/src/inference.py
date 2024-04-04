import os
from typing import List, Dict

import boto3
from dotenv import load_dotenv
from sagemaker.predictor import retrieve_default
from sagemaker.session import Session

load_dotenv()

SAGEMAKER_ENDPOINT = os.environ.get("SAGEMAKER_ENDPOINT")
REGION = os.environ.get("REGION")

predictor = retrieve_default(SAGEMAKER_ENDPOINT,
                             sagemaker_session=Session(boto3.Session(region_name=REGION)))


def query_model(query: str) -> List[Dict[str, str]]:
    payload = {
        "inputs": f"<s>[INST] {query} [/INST]",
        "parameters": {
            "max_new_tokens": 256,
            "do_sample": True
        }
    }

    return predictor.predict(payload)
