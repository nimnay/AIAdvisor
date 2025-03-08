import boto3
import json

def callAPI(student):
    kb_id = "IIPMMYP0DR"

    # Extract courses from the student object
    completed_courses = "\n".join([f"- {course}" for course in student.get("completed_courses", [])])
    current_courses = "\n".join([f"- {course}" for course in student.get("current_courses", [])])
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
                  f"4. Ensure the schedule is appropriate for my academic standing and does not include courses I’m not eligible to take.")

    hard_coded_prompt = ("You are a college advisor helping students plan their class schedules based on their current "
                         "progress. I will provide you with a list of courses I have already completed and a set of class offerings for the next semester. Your job is to create a schedule")

    response = retrieveAndGenerate(input_text, kb_id, hard_coded_prompt)
    print(response)

    if response:
        return response
    else:
        print("No response received from AWS Bedrock.")

def retrieveAndGenerate(input_text, kb_id, hard_coded_prompt):
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
        #"generationPrompt": hard_coded_prompt,
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


