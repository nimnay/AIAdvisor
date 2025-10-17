# Quick Start Guide

## Setup (First Time)

1. **Install Dependencies**
   ```powershell
   pip install -r requirements.txt
   ```

2. **Generate Course Data**
   ```powershell
   # Generate course structure
   python -m src.preprocess
   
   # Generate class schedules with time slots
   python -m src.class_timings
   ```

3. **Configure AWS Credentials**
   Make sure your AWS credentials are configured:
   ```powershell
   aws configure
   ```
   You'll need:
   - AWS Access Key ID
   - AWS Secret Access Key
   - Region: `us-west-2`

## Running the Application

```powershell
python -m src.main
```

## Project Files Overview

### Source Code (`src/`)
- `config.py` - All configuration constants (AWS settings, time slots, etc.)
- `utils.py` - AWS Bedrock API integration functions
- `main.py` - Interactive CLI application
- `preprocess.py` - Course catalog data preprocessing
- `class_timings.py` - Generate schedules with time slots

### Data Files (`data/`)
- `course_structure.json` - CS degree requirements and course catalog
- `class_schedule.json` - Generated schedules with sections and times
- `*.txt` - Raw text files from preprocessing

## Common Commands

### Development
```powershell
# Format code
black src/

# Type checking
mypy src/

# Linting
pylint src/
```

### Regenerate Data
```powershell
# If you need to regenerate course data
python -m src.preprocess
python -m src.class_timings
```

## Troubleshooting

### "Import boto3 could not be resolved"
Install dependencies: `pip install -r requirements.txt`

### "AWS credentials not found"
Run `aws configure` and enter your credentials

### "Knowledge base not found"
Check that `KNOWLEDGE_BASE_ID` in `src/config.py` matches your AWS Bedrock KB

## Next Steps

1. Customize course data in `src/preprocess.py`
2. Adjust time slots in `src/config.py`
3. Modify prompt templates in `src/utils.py`
