# AI Advisor - Student Schedule Planner 🎓

An intelligent course scheduling assistant powered by AWS Bedrock that helps students plan their academic schedules based on completed courses, prerequisites, and time constraints.

## 🌟 Features

- **Personalized Recommendations**: Get schedule suggestions based on your academic history
- **Prerequisite Validation**: Ensures you only see courses you're eligible to take
- **Time Conflict Prevention**: Automatically avoids scheduling overlapping classes
- **Credit Hour Optimization**: Aims for 16-18 credits while respecting constraints
- **AWS Bedrock Integration**: Leverages Claude 3 Sonnet for intelligent recommendations

## 📁 Project Structure

```
AIAdvisor/
├── src/                      # Source code
│   ├── config.py            # Configuration constants
│   ├── utils.py             # AWS Bedrock utilities
│   ├── main.py              # Main application entry point
│   ├── preprocess.py        # Course catalog preprocessing
│   └── class_timings.py     # Schedule generation with time slots
├── data/                     # Data files (generated)
│   ├── course_structure.json
│   └── class_schedule.json
├── docs/                     # Documentation
├── requirements.txt          # Python dependencies
├── .gitignore
└── README.md
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- AWS Account with Bedrock access
- AWS credentials configured locally

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/nimnay/AIAdvisor.git
   cd AIAdvisor
   ```

2. **Create a virtual environment**
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

3. **Install dependencies**
   ```powershell
   pip install -r requirements.txt
   ```

4. **Configure AWS credentials**
   Ensure your AWS credentials are configured with Bedrock access:
   ```powershell
   aws configure
   ```

### Usage

#### 1. Generate Course Data (First Time Setup)

Generate the course structure and class schedules:

```powershell
# Generate course structure
python -m src.preprocess

# Generate class schedules with time slots
python -m src.class_timings
```

#### 2. Run the Schedule Planner

```powershell
python -m src.main
```

Follow the interactive prompts to:
- Enter your name
- List completed courses (e.g., `CPSC 1010, ENGL 1030`)
- List current courses
- Specify time constraints (optional)

## 📋 Example

```
==============================================================
AI Advisor - Student Schedule Planner
==============================================================

Enter your name: 
John Doe

Enter courses you have **already completed**, separated by commas:
CPSC 1010, ENGL 1030, MATH 1060

Enter courses you are **currently enrolled in**:
CPSC 1020, MATH 1080

Enter any time slot constraints:
No classes before 10am

🔄 Generating schedule recommendations...

==============================================================
Schedule Recommendations for John Doe
==============================================================

Recommended Schedule:

1. CPSC 2070 - Discrete Structures for Computing | MWF 10:10 AM - 11:00 AM
2. COMM 1500 - Introduction to Human Communication | TTh 12:00 PM - 1:15 PM
3. BIOL 1030 - General Biology I | MWF 1:25 PM - 2:15 PM
...
```

## 🔧 Configuration

Edit `src/config.py` to customize:

- AWS region and model ARNs
- Credit hour requirements
- Time slot options
- Generation parameters

## 📚 Data Files

### Course Structure (`data/course_structure.json`)
Contains the Computer Science BS degree requirements including:
- General education requirements
- Major-specific courses
- Prerequisites
- Credit hours

### Class Schedule (`data/class_schedule.json`)
Generated schedule with:
- Course sections
- Time slots (MWF/TTh)
- Section IDs

## 🛠️ Development

### Code Style

The project uses:
- **Black** for code formatting
- **Pylint** for linting
- **MyPy** for type checking

Format code:
```powershell
black src/
```

### Project Organization

- `src/config.py` - All configuration constants
- `src/utils.py` - AWS Bedrock API integration
- `src/main.py` - Interactive CLI application
- `src/preprocess.py` - Course data preprocessing
- `src/class_timings.py` - Schedule generation

## 📝 License

This project is for educational purposes.

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📧 Contact

For questions or issues, please open a GitHub issue.

---

**Note**: This application requires active AWS Bedrock credentials and may incur AWS costs based on usage.
