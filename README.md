# Gmail Auto-Reply Bot

## Overview
A Python Tkinter application that automates email responses using the Gmail API and an AI-powered response generation system.

## Prerequisites
- Python 3.7+
- Google Cloud Project with Gmail API enabled
- Required Python packages (install via `pip install -r requirements.txt`)

## Setup and Installation

### 1. Google Cloud Configuration
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Gmail API
4. Create OAuth 2.0 Credentials
   - Select "Desktop app" as the application type
   - Download the `credentials.json` file

### 2. Project Setup
```bash
# Clone the repository
git clone https://your-repository-url.git
cd gmail-auto-reply-bot

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

# Install dependencies
pip install -r requirements.txt
```

## Sensitive Information Management

### Handling Credentials
1. Add `credentials.json` and `token.pickle` to `.gitignore`
```
# .gitignore
credentials.json
token.pickle
```

2. Create a `credentials.example.json` with placeholder content to show file structure

### Environment Variables (Optional)
Consider using environment variables for sensitive configuration:
```python
import os
from dotenv import load_dotenv

load_dotenv()  # Load variables from .env file
SYSTEM_PROMPT = os.getenv('SYSTEM_PROMPT', 'Default prompt')
```

Create a `.env` file (also added to `.gitignore`):
```
SYSTEM_PROMPT=Your custom system prompt
```

## Running the Application
```bash
python gmail_auto_reply_bot.py
```

## Features
- Gmail API integration
- Configurable response interval
- Advanced email filtering
- AI-powered response generation
- Tkinter-based user interface

## Security Considerations
- Never commit sensitive credentials to version control
- Use environment variables or secure credential management
- Regularly rotate OAuth tokens

## License
[Specify your project's license]

## Disclaimer
This bot is for educational purposes. Ensure compliance with email service providers' terms of service.
