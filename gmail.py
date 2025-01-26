import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import json
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import base64
from email.mime.text import MIMEText
import threading
import requests
from datetime import datetime
import time

class AdvancedGmailBot:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Gmail Auto-Reply Bot")
        self.window.geometry("800x600")
        
        # Gmail API setup
        self.SCOPES = ['https://www.googleapis.com/auth/gmail.modify']
        self.service = None
        
        # Create main container
        self.main_container = ttk.Frame(self.window, padding="10")
        self.main_container.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.setup_advanced_ui()
        self.load_credentials()

    def setup_advanced_ui(self):
        # Status section
        status_frame = ttk.LabelFrame(self.main_container, text="Status", padding="5")
        status_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        self.status_label = ttk.Label(status_frame, text="Not Connected")
        self.status_label.grid(row=0, column=0, sticky=tk.W)
        
        self.connect_button = ttk.Button(status_frame, text="Connect Gmail", command=self.connect_gmail)
        self.connect_button.grid(row=0, column=1, padx=5)
        
        # Settings section
        settings_frame = ttk.LabelFrame(self.main_container, text="Settings", padding="5")
        settings_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # Check Interval
        ttk.Label(settings_frame, text="Check Interval (minutes):").grid(row=0, column=0, sticky=tk.W)
        self.interval_var = tk.StringVar(value="5")
        self.interval_entry = ttk.Entry(settings_frame, textvariable=self.interval_var, width=10)
        self.interval_entry.grid(row=0, column=1, sticky=tk.W, padx=5)
        
        # Advanced Filtering
        ttk.Label(settings_frame, text="Email Filters:").grid(row=1, column=0, sticky=tk.W)
        self.filter_text = scrolledtext.ScrolledText(settings_frame, height=3, width=40)
        self.filter_text.grid(row=1, column=1, columnspan=2, sticky=(tk.W, tk.E))
        self.filter_text.insert('1.0', "Ignore newsletters, spam, and automated emails.")
        
        # Prompt Configuration
        ttk.Label(settings_frame, text="System Prompt:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.system_prompt = scrolledtext.ScrolledText(settings_frame, height=3, width=40)
        self.system_prompt.grid(row=2, column=1, columnspan=2, sticky=(tk.W, tk.E))
        self.system_prompt.insert('1.0', "You are a professional email assistant. Keep responses concise and friendly.")
        
        # Control buttons
        control_frame = ttk.Frame(self.main_container)
        control_frame.grid(row=2, column=0, columnspan=2, pady=10)
        
        self.start_button = ttk.Button(control_frame, text="Start Bot", command=self.start_bot)
        self.start_button.grid(row=0, column=0, padx=5)
        
        self.stop_button = ttk.Button(control_frame, text="Stop Bot", command=self.stop_bot, state=tk.DISABLED)
        self.stop_button.grid(row=0, column=1, padx=5)
        
        # Log section
        log_frame = ttk.LabelFrame(self.main_container, text="Activity Log", padding="5")
        log_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=15)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.main_container.columnconfigure(0, weight=1)
        self.main_container.rowconfigure(3, weight=1)
        
        # Bot state
        self.is_running = False
        self.bot_thread = None

    def load_credentials(self):
        self.creds = None
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                self.creds = pickle.load(token)
        
        if self.creds and self.creds.valid:
            self.service = build('gmail', 'v1', credentials=self.creds)
            self.status_label.config(text="Connected")
            self.log_message("Gmail credentials loaded successfully")
        else:
            self.status_label.config(text="Not Connected")

    def connect_gmail(self):
        if not os.path.exists('credentials.json'):
            messagebox.showerror("Error", "credentials.json file not found!\nPlease download it from Google Cloud Console.")
            return
            
        try:
            if not self.creds or not self.creds.valid:
                if self.creds and self.creds.expired and self.creds.refresh_token:
                    self.creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', self.SCOPES)
                    self.creds = flow.run_local_server(port=8080)  # Using fixed port 8080
                
                with open('token.pickle', 'wb') as token:
                    pickle.dump(self.creds, token)
            
            self.service = build('gmail', 'v1', credentials=self.creds)
            self.status_label.config(text="Connected")
            self.log_message("Successfully connected to Gmail")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to connect: {str(e)}")
            self.log_message(f"Connection error: {str(e)}")

    def generate_response(self, email_content):
        try:
            url = "https://text.pollinations.ai/"
            headers = {
                "Content-Type": "application/json"
            }
            
            payload = {
                "messages": [
                    {
                        "role": "system",
                        "content": self.system_prompt.get("1.0", tk.END).strip()
                    },
                    {
                        "role": "user",
                        "content": f"Please generate a professional response to this email:\n\n{email_content}"
                    }
                ],
                "model": "openai",
                "jsonMode": False
            }
            
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            
            return response.text.strip()
            
        except Exception as e:
            self.log_message(f"Error generating response: {str(e)}")
            return None

    def create_message(self, to, subject, message_text):
        message = MIMEText(message_text)
        message['to'] = to
        message['subject'] = f"Re: {subject}"
        return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}

    def should_skip_email(self, subject, from_email, body):
        # Advanced email filtering
        filters = self.filter_text.get("1.0", tk.END).lower().strip()
        
        skip_conditions = [
            'unsubscribe' in body.lower(),
            'newsletter' in subject.lower(),
            'no-reply' in from_email.lower(),
            filters in body.lower() or filters in subject.lower()
        ]
        
        return any(skip_conditions)

    def check_emails(self):
        while self.is_running:
            try:
                # Get unread messages
                results = self.service.users().messages().list(
                    userId='me',
                    labelIds=['INBOX', 'UNREAD']
                ).execute()
                
                messages = results.get('messages', [])
                
                for message in messages:
                    msg = self.service.users().messages().get(
                        userId='me',
                        id=message['id']
                    ).execute()
                    
                    # Extract email content and metadata
                    headers = msg['payload']['headers']
                    subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
                    from_email = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown Sender')
                    
                    # Get email body
                    if 'parts' in msg['payload']:
                        email_body = base64.urlsafe_b64decode(
                            msg['payload']['parts'][0]['body']['data']
                        ).decode()
                    else:
                        email_body = base64.urlsafe_b64decode(
                            msg['payload']['body']['data']
                        ).decode()
                    
                    # Skip emails based on filters
                    if self.should_skip_email(subject, from_email, email_body):
                        continue
                    
                    # Generate and send response
                    response_text = self.generate_response(email_body)
                    if response_text:
                        # Extract email address from "Name <email>" format
                        email_address = from_email.split('<')[-1].rstrip('>')
                        
                        response_message = self.create_message(
                            email_address,
                            subject,
                            response_text
                        )
                        
                        self.service.users().messages().send(
                            userId='me',
                            body=response_message
                        ).execute()
                        
                        # Mark as read
                        self.service.users().messages().modify(
                            userId='me',
                            id=message['id'],
                            body={'removeLabelIds': ['UNREAD']}
                        ).execute()
                        
                        self.log_message(f"Responded to email from {from_email}")
                
                # Wait for next check
                time.sleep(int(self.interval_var.get()) * 60)
                
            except Exception as e:
                self.log_message(f"Error checking emails: {str(e)}")
                time.sleep(60)  # Wait a minute before retrying

    def start_bot(self):
        if not self.service:
            messagebox.showerror("Error", "Please connect to Gmail first!")
            return
            
        try:
            interval = int(self.interval_var.get())
            if interval < 1:
                raise ValueError("Interval must be at least 1 minute")
                
            self.is_running = True
            self.bot_thread = threading.Thread(target=self.check_emails)
            self.bot_thread.daemon = True
            self.bot_thread.start()
            
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.log_message("Bot started")
            
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start bot: {str(e)}")

    def stop_bot(self):
        self.is_running = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.log_message("Bot stopped")

    def log_message(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    bot = AdvancedGmailBot()
    bot.run()
