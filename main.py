import boto3
import json
from botocore.exceptions import ClientError

client = boto3.client("bedrock-runtime", region_name="us-west-2")
model_id = "arn:aws:bedrock:us-west-2:363793501045:inference-profile/us.meta.llama3-2-1b-instruct-v1:0"
prompt = "Tell me a joke"

formatted_prompt = f"""
<|begin_of_text|><|start_header_id|>user<|end_header_id|>
{prompt}
<|eot_id|>
<|start_header_id|>assistant<|end_header_id|>
"""

native_request = {
    "prompt": formatted_prompt,
    "max_gen_len": 512,
    "temperature": 0.5,
}

# Convert the request to JSON and then to bytes
request = json.dumps(native_request).encode('utf-8')  # Convert to bytes

try:
    model_response = None
    response = None
    # Invoke the model with the request
    response = client.invoke_model(
        modelId=model_id,
        body=request,
        contentType="application/json",  # Specify content type
        accept="application/json"  # Specify accept type
    )

    # Decode the response body
    model_response = json.loads(response["body"].read())

    # Extract and print the response text
    response_text = model_response["generation"]
    print(response_text)

except ClientError as e:
    print(f"AWS ClientError: {e}")
except Exception as e:
    print(f"General error: {e}")
    raise  # Re-raise the exception to see the full traceback