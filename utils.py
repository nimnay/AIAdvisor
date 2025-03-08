import boto3
import json
from botocore.exceptions import ClientError

def callAPI(promptData):
    client = boto3.client("bedrock-runtime", region_name="us-west-2")
    model_id = "arn:aws:bedrock:us-west-2:363793501045:inference-profile/us.meta.llama3-2-1b-instruct-v1:0"
    prompt = (f"Create a daily schedule for a college student named {promptData.name} that is a {promptData.grade} and "
              f"wants to take a nap between {promptData.time_constraints}")

    formatted_prompt = f"""
    <|begin_of_text|><|start_header_id|>user<|end_header_id|>
    {prompt}
    <|eot_id|>
    <|start_header_id|>assistant<|end_header_id|>
    """

    native_request = {
        "prompt": formatted_prompt,
        "max_gen_len": 512,
        "temperature": 1,
        "top_p": 0.1,
    }

    request = json.dumps(native_request).encode('utf-8')

    try:
        response = client.invoke_model(
            modelId=model_id,
            body=request,
            contentType="application/json",
            accept="application/json"
        )

        model_response = json.loads(response["body"].read())

        response_text = model_response["generation"]
        return response_text

    except ClientError as e:
        print(f"AWS ClientError: {e}")
    except Exception as e:
        print(f"General error: {e}")
        raise