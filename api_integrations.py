"""
API integrations for Google Calendar, Notion, Google Sheets
"""
import os
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import json


class GoogleCalendarIntegration:
    """Google Calendar API integration"""
    
    def __init__(self):
        """Initialize Google Calendar client"""
        self.credentials_path = os.getenv("GOOGLE_CALENDAR_CREDENTIALS")
        self.service = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize Google Calendar API client"""
        if not self.credentials_path or not os.path.exists(self.credentials_path):
            return
        
        try:
            from google.oauth2 import service_account
            from googleapiclient.discovery import build
            
            SCOPES = ['https://www.googleapis.com/auth/calendar']
            credentials = service_account.Credentials.from_service_account_file(
                self.credentials_path, scopes=SCOPES
            )
            self.service = build('calendar', 'v3', credentials=credentials)
        except Exception as e:
            print(f"Warning: Failed to initialize Google Calendar: {e}")
    
    def schedule_interview(self, candidate_email: str, candidate_name: str, 
                          interview_date: datetime, duration_minutes: int = 60) -> bool:
        """Schedule an interview in Google Calendar"""
        if not self.service:
            return False
        
        try:
            event = {
                'summary': f'Interview: {candidate_name}',
                'description': f'Interview with {candidate_name} ({candidate_email})',
                'start': {
                    'dateTime': interview_date.isoformat(),
                    'timeZone': 'UTC',
                },
                'end': {
                    'dateTime': (interview_date + timedelta(minutes=duration_minutes)).isoformat(),
                    'timeZone': 'UTC',
                },
                'attendees': [
                    {'email': candidate_email}
                ],
            }
            
            event = self.service.events().insert(calendarId='primary', body=event).execute()
            return True
        except Exception as e:
            print(f"Error scheduling interview: {e}")
            return False


class NotionIntegration:
    """Notion API integration"""
    
    def __init__(self):
        """Initialize Notion client"""
        self.api_key = os.getenv("NOTION_API_KEY")
        self.client = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize Notion API client"""
        if not self.api_key:
            return
        
        try:
            from notion_client import Client
            self.client = Client(auth=self.api_key)
        except Exception as e:
            print(f"Warning: Failed to initialize Notion: {e}")
    
    def create_candidate_page(self, database_id: str, candidate_data: Dict) -> Optional[str]:
        """Create a candidate page in Notion database"""
        if not self.client:
            return None
        
        try:
            properties = {
                "Name": {
                    "title": [
                        {
                            "text": {
                                "content": candidate_data.get("name", "Unknown")
                            }
                        }
                    ]
                },
                "Email": {
                    "email": candidate_data.get("email", "")
                },
                "Score": {
                    "number": candidate_data.get("score", 0)
                },
                "Status": {
                    "select": {
                        "name": candidate_data.get("status", "Screening")
                    }
                }
            }
            
            response = self.client.pages.create(
                parent={"database_id": database_id},
                properties=properties
            )
            
            return response.get("id")
        except Exception as e:
            print(f"Error creating Notion page: {e}")
            return None


class GoogleSheetsIntegration:
    """Google Sheets API integration"""
    
    def __init__(self):
        """Initialize Google Sheets client"""
        self.credentials_path = os.getenv("GOOGLE_SHEETS_CREDENTIALS")
        self.client = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize Google Sheets API client"""
        if not self.credentials_path or not os.path.exists(self.credentials_path):
            return
        
        try:
            import gspread
            from google.oauth2 import service_account
            
            scope = ['https://spreadsheets.google.com/feeds',
                    'https://www.googleapis.com/auth/drive']
            credentials = service_account.Credentials.from_service_account_file(
                self.credentials_path, scopes=scope
            )
            # Use gspread.Client for newer versions (5.x+)
            try:
                self.client = gspread.Client(auth=credentials)
            except TypeError:
                # Fallback for older gspread versions
                self.client = gspread.authorize(credentials)
        except Exception as e:
            print(f"Warning: Failed to initialize Google Sheets: {e}")
    
    def export_results(self, spreadsheet_id: str, results: List[Dict]) -> bool:
        """Export screening results to Google Sheets"""
        if not self.client:
            return False
        
        try:
            sheet = self.client.open_by_key(spreadsheet_id).sheet1
            
            # Headers
            headers = ["Rank", "Name", "Email", "Score", "Recommendation", "Skills", "Experience"]
            sheet.append_row(headers)
            
            # Data rows
            for result in results:
                row = [
                    result.get("rank", ""),
                    result.get("metadata", {}).get("name", ""),
                    result.get("metadata", {}).get("email", ""),
                    result.get("score", 0),
                    result.get("recommendation", ""),
                    ", ".join(result.get("matched_skills", [])),
                    result.get("experience_years", 0)
                ]
                sheet.append_row(row)
            
            return True
        except Exception as e:
            print(f"Error exporting to Google Sheets: {e}")
            return False

