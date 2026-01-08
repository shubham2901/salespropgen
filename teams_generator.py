"""
Teams Chat Generator Module
Generates realistic Teams group chat conversations for the Sales Proposal Copilot.
"""

from datetime import datetime, timedelta
import random

def generate_team_chat(company_name: str):
    """
    Generate a realistic Teams group chat about a company's CRM needs.
    
    Args:
        company_name: The name of the company to generate chat for
        
    Returns:
        Dictionary with chat title and list of messages
    """
    
    # Generate timestamps for the last week
    base_time = datetime.now()
    
    messages = [
        {
            "sender": "Alex Rivera (Sales Rep)",
            "timestamp": (base_time - timedelta(days=6, hours=2)).strftime("%b %d, %I:%M %p"),
            "content": f"Hey team, I just got off a call with the decision makers at {company_name}. They're really interested in upgrading their CRM."
        },
        {
            "sender": "Jordan Lee (Account Manager)",
            "timestamp": (base_time - timedelta(days=6, hours=1, minutes=45)).strftime("%b %d, %I:%M %p"),
            "content": "That's great news! What are their main pain points?"
        },
        {
            "sender": "Alex Rivera (Sales Rep)",
            "timestamp": (base_time - timedelta(days=6, hours=1, minutes=30)).strftime("%b %d, %I:%M %p"),
            "content": f"They mentioned three big issues:\n1. Data silos between departments\n2. Current system is way too slow\n3. No AI capabilities - they're falling behind competitors"
        },
        {
            "sender": "Sam Chen (Solution Architect)",
            "timestamp": (base_time - timedelta(days=6, hours=1, minutes=15)).strftime("%b %d, %I:%M %p"),
            "content": "Those are exactly the problems NexusCRM solves. Did they mention budget?"
        },
        {
            "sender": "Alex Rivera (Sales Rep)",
            "timestamp": (base_time - timedelta(days=6, hours=1)).strftime("%b %d, %I:%M %p"),
            "content": f"Yes! They have around $50k/year allocated. Their CFO already got approval from leadership."
        },
        {
            "sender": "Jordan Lee (Account Manager)",
            "timestamp": (base_time - timedelta(days=6, hours=0, minutes=45)).strftime("%b %d, %I:%M %p"),
            "content": "Perfect, that fits our Enterprise tier. What's their timeline?"
        },
        {
            "sender": "Alex Rivera (Sales Rep)",
            "timestamp": (base_time - timedelta(days=6, hours=0, minutes=30)).strftime("%b %d, %I:%M %p"),
            "content": "They want to implement in Q1. It's tied to their fiscal year planning."
        },
        {
            "sender": "Sam Chen (Solution Architect)",
            "timestamp": (base_time - timedelta(days=6, hours=0, minutes=20)).strftime("%b %d, %I:%M %p"),
            "content": f"Q1 is doable. I'll need to understand their current tech stack. Do they have any integration requirements?"
        },
        {
            "sender": "Alex Rivera (Sales Rep)",
            "timestamp": (base_time - timedelta(days=6, hours=0, minutes=10)).strftime("%b %d, %I:%M %p"),
            "content": f"Their IT Director mentioned they need to integrate with Salesforce, Teams, Outlook, and their custom billing system. Mobile support is also critical for their field sales team."
        },
        {
            "sender": "Jordan Lee (Account Manager)",
            "timestamp": (base_time - timedelta(days=6, hours=0, minutes=5)).strftime("%b %d, %I:%M %p"),
            "content": "All standard integrations for us. I'll start drafting the proposal. Can you send over any notes from the call?"
        },
        {
            "sender": "Alex Rivera (Sales Rep)",
            "timestamp": (base_time - timedelta(days=6)).strftime("%b %d, %I:%M %p"),
            "content": "Will do. I also have email threads with their Sales Director and VP of Marketing that provide more context on their pain points."
        },
        {
            "sender": "Sam Chen (Solution Architect)",
            "timestamp": (base_time - timedelta(days=5, hours=23, minutes=55)).strftime("%b %d, %I:%M %p"),
            "content": f"Great work Alex! {company_name} sounds like an ideal fit for NexusCRM. Let's make sure we highlight our AI features and data unification capabilities in the proposal."
        }
    ]
    
    return {
        "title": f"💼 {company_name} - CRM Opportunity",
        "participants": ["Alex Rivera (Sales Rep)", "Jordan Lee (Account Manager)", "Sam Chen (Solution Architect)"],
        "messages": messages
    }
