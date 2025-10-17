"""Configuration constants for AI Advisor application."""

# AWS Bedrock Configuration
AWS_REGION = "us-west-2"
KNOWLEDGE_BASE_ID = "IIPMMYP0DR"

# Model ARNs
RETRIEVE_MODEL_ARN = (
    "arn:aws:bedrock:us-west-2::foundation-model/"
    "anthropic.claude-3-sonnet-20240229-v1:0"
)
FORMAT_MODEL_ID = (
    "arn:aws:bedrock:us-west-2:363793501045:inference-profile/"
    "us.meta.llama3-2-1b-instruct-v1:0"
)

# Generation Parameters
MAX_GENERATION_LENGTH = 512
TEMPERATURE = 1.0
TOP_P = 0.1

# Credit Requirements
MIN_CREDITS = 12
TARGET_MIN_CREDITS = 16
TARGET_MAX_CREDITS = 18

# Time Slots
MWF_TIME_SLOTS = [
    "8:00 AM - 8:50 AM",
    "9:05 AM - 9:55 AM",
    "10:10 AM - 11:00 AM",
    "11:15 AM - 12:05 PM",
    "12:20 PM - 1:10 PM",
    "1:25 PM - 2:15 PM",
    "2:30 PM - 3:20 PM",
    "3:35 PM - 4:25 PM",
    "4:40 PM - 5:30 PM",
]

TTH_TIME_SLOTS = [
    "8:00 AM - 9:15 AM",
    "10:30 AM - 11:45 AM",
    "12:00 PM - 1:15 PM",
    "1:30 PM - 2:45 PM",
]
