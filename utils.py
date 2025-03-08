import boto3
import json

def callAPI():
    kb_id = "IIPMMYP0DR"
    input_text = "list the available advanced systems paths."
    response = retrieveAndGenerate(input_text, kb_id)

    if response:
        return response
    else:
        print("No response received from AWS Bedrock.")

def retrieveAndGenerate(input_text, kb_id):
    session_id = None
    model_id = "anthropic.claude-3-sonnet-20240229-v1:0"
    region_id = "us-west-2"

    # Initialize AWS Bedrock Agent Runtime client
    bedrock_agent_client = boto3.client("bedrock-agent-runtime", region_name=region_id)

    request_payload = {
        "input": {"text": input_text},
        "retrieveAndGenerateConfiguration": {
            "type": "KNOWLEDGE_BASE",
            "knowledgeBaseConfiguration": {
                "knowledgeBaseId": kb_id,
                "modelArn": "arn:aws:bedrock:us-west-2::foundation-model/anthropic.claude-3-sonnet-20240229-v1:0"
            }
        }
    }

    if session_id:
        request_payload["sessionId"] = session_id

    try:
        response = bedrock_agent_client.retrieve_and_generate(**request_payload)

        generated_text = response["output"]["text"]
        return generated_text

    except Exception as e:
        print(f"Error retrieving and generating response: {e}")
        return None


