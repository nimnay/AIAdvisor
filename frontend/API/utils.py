import boto3
import json

from botocore.exceptions import ClientError

# Calls the API connected to scheduling knowledge base
# Parameter: student- contains the students name and previously taken courses
def callAPI(student):
    kb_id = "IIPMMYP0DR"

    # Prompt to input into LLM
    input_text = (f"I am currently planning my class schedule for the next semester. Here is a list of courses I have "
                  f"already completed. Use this to create a list of classes I should take next semester:\n\n"
                  f"**Completed Courses: {student.get("completed_courses")}\n\n"
                  f"**Task:** Based on the courses I have already completed, "
                  f"create a class schedule for me. Please make sure to:\n"
                  f"1. Recommend only those courses for which I meet the prerequisites.\n"
                  f"2. Ensure no recommended courses have overlapping class times.\n"
                  f"3. Align your recommendations with my current academic progress and graduation year.\n"
                  f"4. Ensure the schedule is appropriate for my academic standing and does not include courses I’m not eligible to take.\n"
                  f"5. Ensure that your recommended scheduled is between 15 and 18 credits\n"
                  f"6. If a course has prerequisites, only recommend it if I have already completed the prerequisites.\n"
                  f"7. Include class times and dates"
                  )

    # Call to API
    response = retrieveAndGenerate(input_text, kb_id)
    return response

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
        },
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

# Call to Llama 3.2 3B to help with output formatting
def createList(response):
    client = boto3.client("bedrock-runtime", region_name="us-west-2")
    model_id = "arn:aws:bedrock:us-west-2:363793501045:inference-profile/us.meta.llama3-2-1b-instruct-v1:0"
    prompt = f"Create a list from this data providing the class numbers and class times with each class's data on a separate line: {response}"
    formatted_prompt = f"""
    <|begin_of_text|><|start_header_id|>user<|end_header_id|>
    {prompt}
    <|eot_id|>
    <|start_header_id|>assistant<|end_header_id|>
    """

    native_request = {
        "prompt": formatted_prompt,
        "max_gen_len": 512,
        "temperature": 0.1,
        "top_p": 1,
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