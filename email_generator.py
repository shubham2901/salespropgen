"""
Email Generator Module
Generates realistic company-specific emails for the Sales Proposal Copilot.
"""

from datetime import datetime, timedelta
import random

def generate_emails(company_name: str):
    """
    Generate 5 contextual emails about a company's CRM needs.
    
    Args:
        company_name: The name of the company to generate emails for
        
    Returns:
        List of email dictionaries with sender, subject, date, and body
    """
    
    # Email templates with placeholders for company name
    templates = [
        {
            "sender": "john.smith@{company}.com",
            "subject": "Re: CRM System Performance Issues",
            "body": """Hi Team,

I wanted to follow up on our discussion about the current CRM system at {company}. We're experiencing significant performance issues that are impacting our sales team's productivity.

Key pain points:
- System takes 5-10 seconds to load customer records
- Frequent timeouts during peak hours
- Data sync issues between departments

Our team is spending more time waiting for the system than actually engaging with customers. We need to explore alternatives that can handle our growing data volume.

Can we schedule a call to discuss potential solutions?

Best regards,
John Smith
Sales Director, {company}"""
        },
        {
            "sender": "sarah.johnson@{company}.com",
            "subject": "Data Silos - Urgent Discussion Needed",
            "body": """Team,

I'm reaching out because we have a critical issue with data silos across {company}. Marketing, Sales, and Customer Success are all working with different versions of customer data.

This is causing:
- Duplicate outreach to the same customers
- Inconsistent messaging
- Lost opportunities due to lack of visibility

We need a unified CRM solution that can break down these silos and give everyone a single source of truth. This is becoming a major blocker for our Q1 initiatives.

Let's prioritize finding a solution ASAP.

Sarah Johnson
VP of Marketing, {company}"""
        },
        {
            "sender": "michael.chen@{company}.com",
            "subject": "Budget Approval for CRM Upgrade",
            "body": """Hi Leadership Team,

Following our strategic planning session, I've been reviewing options for upgrading our CRM infrastructure at {company}.

Budget considerations:
- Current system costs: $35k/year
- Proposed budget for new solution: $50k/year
- Expected ROI: 25% increase in sales productivity

The investment is justified given our growth trajectory and the limitations of our current system. I've identified a few vendors that could meet our needs within this budget range.

Timeline: We should aim for Q1 implementation to align with our fiscal year planning.

Looking forward to your feedback.

Michael Chen
CFO, {company}"""
        },
        {
            "sender": "emily.rodriguez@{company}.com",
            "subject": "AI Features - Competitive Necessity",
            "body": """Hello,

I wanted to share some competitive intelligence regarding CRM capabilities at {company}.

Our main competitors are leveraging AI-powered CRM features:
- Predictive lead scoring
- Automated task prioritization
- Intelligent customer insights
- Sentiment analysis

We're falling behind in this area. Our current CRM lacks any AI capabilities, which is putting us at a disadvantage in terms of sales efficiency and customer engagement.

I strongly recommend we prioritize AI features in our CRM evaluation criteria.

Emily Rodriguez
Head of Sales Operations, {company}"""
        },
        {
            "sender": "david.park@{company}.com",
            "subject": "Integration Requirements for New CRM",
            "body": """Team,

As we evaluate CRM solutions for {company}, I want to outline our technical integration requirements:

Must integrate with:
- Salesforce (current data source)
- Microsoft Teams (communication)
- Outlook (email tracking)
- Our custom billing system
- Marketing automation platform

The new CRM needs to have robust APIs and pre-built connectors. We can't afford another system that operates in isolation.

Also, we need strong mobile support - our field sales team is constantly on the go.

Let me know if you need any technical specifications.

David Park
IT Director, {company}"""
        }
    ]
    
    # Generate dates for the last 2-3 weeks
    base_date = datetime.now()
    emails = []
    
    for i, template in enumerate(templates):
        # Create dates going backwards from today
        days_ago = random.randint(1, 21)
        email_date = base_date - timedelta(days=days_ago)
        
        # Format company name for email address (lowercase, no spaces)
        company_email = company_name.lower().replace(" ", "").replace(",", "")
        
        emails.append({
            "sender": template["sender"].format(company=company_email),
            "subject": template["subject"],
            "date": email_date.strftime("%B %d, %Y at %I:%M %p"),
            "body": template["body"].format(company=company_name)
        })
    
    # Sort by date (most recent first)
    emails.sort(key=lambda x: datetime.strptime(x["date"], "%B %d, %Y at %I:%M %p"), reverse=True)
    
    return emails
