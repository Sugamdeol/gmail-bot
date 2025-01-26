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
# Install dependencies
pip install -r requirements.txt

# Clone the repository
git clone https://github.com/Sugamdeol/gmail-bot.git
cd gmail-auto-reply-bot
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


## Disclaimer
This bot is for educational purposes. Ensure compliance with email service providers' terms of service.
