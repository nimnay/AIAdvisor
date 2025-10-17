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
    import json
    import logging
    from typing import Any, Dict, List, Optional

    import boto3
    from botocore.exceptions import ClientError

    LOGGER = logging.getLogger(__name__)
    LOGGER.addHandler(logging.NullHandler())

    # Constants
    DEFAULT_REGION = "us-west-2"
    KNOWLEDGE_BASE_ID = "IIPMMYP0DR"
    RETRIEVE_MODEL_ARN = (
        "arn:aws:bedrock:us-west-2::foundation-model/anthropic.claude-3-sonnet-20240229-v1:0"
    )
    FORMAT_MODEL_ID = (
        "arn:aws:bedrock:us-west-2:363793501045:inference-profile/us.meta.llama3-2-1b-instruct-v1:0"
    )


    def call_api(student: Dict[str, Any]) -> Optional[List[str]]:
        """Create a prompt from a student profile, retrieve an answer from Bedrock, and return a parsed list.

        Args:
            student: dictionary with optional keys: 'completed_courses', 'current_courses', 'time_constraints', etc.

        Returns:
            A list of class recommendations (one per line) or None on failure.
        """
        completed = student.get("completed_courses", []) or []
        current = student.get("current_courses", []) or []
        time_constraints = student.get("time_constraints")

        completed_text = "\n".join(f"- {c}" for c in completed) if completed else "None"
        current_text = "\n".join(f"- {c}" for c in current) if current else "None"

        input_text = (
            "I am currently planning my class schedule for the next semester. "
            "Here is a list of courses I have already completed or am currently enrolled in. "
            "Use this to determine which courses I am eligible to take:\n\n"
            f"**Completed Courses:**\n{completed_text}\n\n"
            f"**Currently Enrolled Courses:**\n{current_text}\n\n"
            f"**Time Constraints:** {time_constraints or 'None'}\n\n"
            "**Class Offerings for the Next Semester:** [Provide the list of available courses in JSON format]\n\n"
            "**Task:** Based on the courses I have already completed and the available class offerings for the next semester, "
            "create a class schedule for me. Please make sure to:\n"
            "1. Recommend only those courses for which I meet the prerequisites.\n"
            "2. Ensure no recommended courses have overlapping class times.\n"
            "3. Align your recommendations with my current academic progress and graduation year.\n"
            "4. Ensure the schedule is appropriate for my academic standing and does not include courses I’m not eligible to take.\n"
            "5. Ensure that your recommended scheduled is at least 12 credits, use the credit information for each class and aim for 16-18 while staying within the requirements.\n"
            "6. If a course has prerequisites, only recommend it if I have already completed or am currently enrolled in those prerequisites.\n"
            "7. Do not recommend any course that requires a prerequisite I have not taken or am not currently enrolled in."
        )

        response_text = retrieve_and_generate(input_text, KNOWLEDGE_BASE_ID)
        if not response_text:
            LOGGER.error("No response from retrieve_and_generate")
            return None

        LOGGER.debug("Raw retrieve_and_generate response: %s", response_text)

        parsed = create_list(response_text)
        return parsed


    def retrieve_and_generate(input_text: str, kb_id: str, region: str = DEFAULT_REGION) -> Optional[str]:
        """Call Bedrock Agent Runtime retrieve_and_generate API and return the generated text.

        This function wraps boto3 client calls and handles simple errors.
        """
        client = boto3.client("bedrock-agent-runtime", region_name=region)

        payload = {
            "input": {"text": input_text},
            "retrieveAndGenerateConfiguration": {
                "type": "KNOWLEDGE_BASE",
                "knowledgeBaseConfiguration": {"knowledgeBaseId": kb_id, "modelArn": RETRIEVE_MODEL_ARN},
            },
        }

        try:
            resp = client.retrieve_and_generate(**payload)
            # Navigate expected response structure conservatively
            output = resp.get("output") or {}
            text = output.get("text")
            return text

        except ClientError as e:
            LOGGER.exception("AWS ClientError in retrieve_and_generate: %s", e)
            return None
        except Exception as e:
            LOGGER.exception("Unexpected error in retrieve_and_generate: %s", e)
            return None


    def create_list(response: str, region: str = DEFAULT_REGION) -> Optional[List[str]]:
        """Send the response to a formatting model and return a list of strings (one per class).

        The function expects 'response' to be text and will ask a Bedrock formatting model to return a simple list.
        """
        if not response:
            return None

        client = boto3.client("bedrock-runtime", region_name=region)

        prompt = (
            "Create a list from this data providing the class numbers and class times with each class's data on a separate line: "
            f"{response}"
        )

        formatted_prompt = (
            "<|begin_of_text|><|start_header_id|>user<|end_header_id|>\n"
            f"{prompt}\n"
            "<|eot_id|>\n"
            "<|start_header_id|>assistant<|end_header_id|>"
        )

        native_request = {"prompt": formatted_prompt, "max_gen_len": 512, "temperature": 1, "top_p": 0.1}

        try:
            body = json.dumps(native_request).encode("utf-8")
            resp = client.invoke_model(modelId=FORMAT_MODEL_ID, body=body, contentType="application/json", accept="application/json")

            # resp["body"] may be a streaming object; handle common patterns
            raw = resp.get("body")
            if hasattr(raw, "read"):
                raw = raw.read()
            if isinstance(raw, (bytes, bytearray)):
                raw = raw.decode("utf-8")

            model_response = json.loads(raw)
            # try common keys for generated text
            gen = model_response.get("generation") or model_response.get("output") or model_response.get("text")

            if isinstance(gen, list):
                lines = [str(item).strip() for item in gen if str(item).strip()]
            else:
                # fall back to splitting on newlines
                gen_text = str(gen)
                lines = [ln.strip() for ln in gen_text.splitlines() if ln.strip()]

            return lines

        except ClientError as e:
            LOGGER.exception("AWS ClientError in create_list: %s", e)
            return None
        except Exception as e:
            LOGGER.exception("Unexpected error in create_list: %s", e)
            return None
