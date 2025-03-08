import boto3
import json

from botocore.exceptions import ClientError


def callAPI(student):
    kb_id = "IIPMMYP0DR"

    # Extract courses from the student object
    completed_courses = "\n".join([f"- {course}" for course in student.get("completed_courses", [])])
    current_courses = "\n".join([f"- {course}" for course in student.get("current_courses", [])])
    'time_constraints = student.get("time_constraints", "None")  # Default to "None" if empty'


    input_text = (f"I am currently planning my class schedule for the next semester. Here is a list of courses I have "
                  f"already completed or am currently enrolled in. Use this to determine which courses I am eligible to take:\n\n"
                  f"**Completed Courses:**\n{completed_courses if completed_courses else 'None'}\n\n"
                  f"**Currently Enrolled Courses:**\n{current_courses if current_courses else 'None'}\n\n"
                  f"**Class Offerings for the Next Semester:** [Provide the list of available courses in JSON format]\n\n"
                  f"**Task:** Based on the courses I have already completed and the available class offerings for the next semester, "
                  f"create a class schedule for me. Please make sure to:\n"
                  f"1. Recommend only those courses for which I meet the prerequisites.\n"
                  f"2. Ensure no recommended courses have overlapping class times.\n"
                  f"3. Align your recommendations with my current academic progress and graduation year.\n"
                  f"4. Ensure the schedule is appropriate for my academic standing and does not include courses I’m not eligible to take."
                  f"5. Ensure that your recommended scheduled is at least 12 credits, use the credit information for each class and aim for 16-18 while staying within the requirements."
                  f"6. If a course has prerequisites, only recommend it if I have already completed or am currently enrolled in those prerequisites."
                  f"7. Do not recommend any course that requires a prerequisite I have not taken or am not currently enrolled in."

                  )


    response = retrieveAndGenerate(input_text, kb_id)
    print(response)
    answer = createList(response)

    if answer:
        return answer
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