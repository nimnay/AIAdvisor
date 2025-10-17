"""Utility functions for AI Advisor - AWS Bedrock integration."""

import json
import logging
from typing import Any, Dict, List, Optional

import boto3
from botocore.exceptions import ClientError

from src.config import (
    AWS_REGION,
    FORMAT_MODEL_ID,
    KNOWLEDGE_BASE_ID,
    MAX_GENERATION_LENGTH,
    RETRIEVE_MODEL_ARN,
    TARGET_MAX_CREDITS,
    TARGET_MIN_CREDITS,
    TEMPERATURE,
    TOP_P,
)

# Configure logging
logger = logging.getLogger(__name__)


def call_api(student: Dict[str, Any]) -> Optional[List[str]]:
    """
    Generate class schedule recommendations for a student.

    Args:
        student: Dictionary containing student information with keys:
            - completed_courses: List of completed course codes
            - current_courses: List of currently enrolled course codes
            - time_constraints: Optional time slot constraints

    Returns:
        List of recommended classes with scheduling info, or None on failure
    """
    completed = student.get("completed_courses", []) or []
    current = student.get("current_courses", []) or []
    time_constraints = student.get("time_constraints")

    # Format course lists for prompt
    completed_text = "\n".join(f"- {c}" for c in completed) if completed else "None"
    current_text = "\n".join(f"- {c}" for c in current) if current else "None"

    # Build comprehensive prompt
    input_text = _build_schedule_prompt(
        completed_text, current_text, time_constraints
    )

    # Get recommendation from Bedrock
    response_text = retrieve_and_generate(input_text, KNOWLEDGE_BASE_ID)
    if not response_text:
        logger.error("No response from retrieve_and_generate")
        return None

    logger.debug("Raw Bedrock response: %s", response_text)

    # Format response into structured list
    parsed = create_list(response_text)
    return parsed


def _build_schedule_prompt(
    completed_text: str,
    current_text: str,
    time_constraints: Optional[str],
) -> str:
    """Build the scheduling prompt for Bedrock."""
    return (
        "I am currently planning my class schedule for the next semester. "
        "Here is a list of courses I have already completed or am currently enrolled in. "
        "Use this to determine which courses I am eligible to take:\n\n"
        f"**Completed Courses:**\n{completed_text}\n\n"
        f"**Currently Enrolled Courses:**\n{current_text}\n\n"
        f"**Time Constraints:** {time_constraints or 'None'}\n\n"
        "**Class Offerings for the Next Semester:** "
        "[Provide the list of available courses in JSON format]\n\n"
        "**Task:** Based on the courses I have already completed and the available "
        "class offerings for the next semester, create a class schedule for me. "
        "Please make sure to:\n"
        "1. Recommend only those courses for which I meet the prerequisites.\n"
        "2. Ensure no recommended courses have overlapping class times.\n"
        "3. Align your recommendations with my current academic progress and graduation year.\n"
        "4. Ensure the schedule is appropriate for my academic standing and does not "
        "include courses I'm not eligible to take.\n"
        f"5. Ensure that your recommended schedule is at least {TARGET_MIN_CREDITS} credits, "
        f"use the credit information for each class and aim for {TARGET_MIN_CREDITS}-{TARGET_MAX_CREDITS} "
        "while staying within the requirements.\n"
        "6. If a course has prerequisites, only recommend it if I have already completed "
        "or am currently enrolled in those prerequisites.\n"
        "7. Do not recommend any course that requires a prerequisite I have not taken "
        "or am not currently enrolled in."
    )


def retrieve_and_generate(
    input_text: str,
    kb_id: str,
    region: str = AWS_REGION,
) -> Optional[str]:
    """
    Call AWS Bedrock Agent Runtime retrieve_and_generate API.

    Args:
        input_text: The prompt text for the knowledge base query
        kb_id: Knowledge base ID
        region: AWS region name

    Returns:
        Generated text response or None on failure
    """
    try:
        client = boto3.client("bedrock-agent-runtime", region_name=region)

        payload = {
            "input": {"text": input_text},
            "retrieveAndGenerateConfiguration": {
                "type": "KNOWLEDGE_BASE",
                "knowledgeBaseConfiguration": {
                    "knowledgeBaseId": kb_id,
                    "modelArn": RETRIEVE_MODEL_ARN,
                },
            },
        }

        response = client.retrieve_and_generate(**payload)

        # Navigate response structure safely
        output = response.get("output") or {}
        text = output.get("text")

        if not text:
            logger.warning("Empty text in response output")

        return text

    except ClientError as e:
        logger.exception("AWS ClientError in retrieve_and_generate: %s", e)
        return None
    except Exception as e:
        logger.exception("Unexpected error in retrieve_and_generate: %s", e)
        return None


def create_list(
    response: str,
    region: str = AWS_REGION,
) -> Optional[List[str]]:
    """
    Format the Bedrock response into a structured list of classes.

    Args:
        response: Raw text response from Bedrock
        region: AWS region name

    Returns:
        List of formatted class entries (one per line) or None on failure
    """
    if not response:
        logger.warning("Empty response provided to create_list")
        return None

    try:
        client = boto3.client("bedrock-runtime", region_name=region)

        # Build formatting prompt
        prompt = (
            "Create a list from this data providing the class numbers and class times "
            f"with each class's data on a separate line: {response}"
        )

        formatted_prompt = (
            "<|begin_of_text|><|start_header_id|>user<|end_header_id|>\n"
            f"{prompt}\n"
            "<|eot_id|>\n"
            "<|start_header_id|>assistant<|end_header_id|>"
        )

        native_request = {
            "prompt": formatted_prompt,
            "max_gen_len": MAX_GENERATION_LENGTH,
            "temperature": TEMPERATURE,
            "top_p": TOP_P,
        }

        # Invoke formatting model
        body = json.dumps(native_request).encode("utf-8")
        response_obj = client.invoke_model(
            modelId=FORMAT_MODEL_ID,
            body=body,
            contentType="application/json",
            accept="application/json",
        )

        # Parse response body
        raw = response_obj.get("body")
        if hasattr(raw, "read"):
            raw = raw.read()
        if isinstance(raw, (bytes, bytearray)):
            raw = raw.decode("utf-8")

        model_response = json.loads(raw)

        # Extract generated text (try common response keys)
        gen = (
            model_response.get("generation")
            or model_response.get("output")
            or model_response.get("text")
        )

        if not gen:
            logger.warning("No generation text found in model response")
            return None

        # Convert to list of lines
        if isinstance(gen, list):
            lines = [str(item).strip() for item in gen if str(item).strip()]
        else:
            gen_text = str(gen)
            lines = [ln.strip() for ln in gen_text.splitlines() if ln.strip()]

        return lines

    except ClientError as e:
        logger.exception("AWS ClientError in create_list: %s", e)
        return None
    except Exception as e:
        logger.exception("Unexpected error in create_list: %s", e)
        return None
