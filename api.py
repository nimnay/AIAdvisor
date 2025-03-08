import json
import boto3
from botocore.exceptions import ClientError


def createList(response):
    promptData = (f"Based on the courses you have completed or are currently enrolled in (CPSC 1010, CPSC 1020, CPSC 2120, POSC 1010), and the available course offerings provided, here is a recommended class schedule for the next semester that meets the prerequisites and does not have overlapping class times: "
                  f"CPSC 3220 - Introduction to Operating Systems, Section 1 (MWF 2:30 PM - 3:20 PM)"
                  f"CPSC 3600 - Network Programming, Section 1 (MWF 9:05 AM - 9:55 AM)"
                  f"CPSC 3520 - Programming Systems, Section 1 (TTh 1:30 PM - 2:45 PM)"
                  f"This schedule aligns with your current academic progress, as you have completed the prerequisite courses CPSC 1010, CPSC 1020, and CPSC 2120 (Data Structures) required for these upper-level computer science courses. The courses are appropriate for your academic standing, assuming you are a junior or senior computer science major. Please note that I have not included any courses you are not eligible to take based on the provided information.")

    client = boto3.client("bedrock-runtime", region_name="us-west-2")
    model_id = "arn:aws:bedrock:us-west-2:363793501045:inference-profile/us.meta.llama3-2-1b-instruct-v1:0"
    prompt = f"Create a list from this data providing the class numbers class times with each class's data on a separate line: {response}"
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
        print(response_text)
        #return response_text

    except ClientError as e:
        print(f"AWS ClientError: {e}")
    except Exception as e:
        print(f"General error: {e}")
        raise