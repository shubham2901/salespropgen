# NexusCRM Sales Proposal Copilot 🚀

A Microsoft 365 Copilot-style Sales Proposal Generator built with Streamlit, Gemini AI, and Tavily.

## Features
- **Conversational Interface**: Interact with a dedicated Sales Proposal Agent.
- **Two-Column Layout**: Chat on the left, context and tools on the right.
- **Automated Research**: Gathers company insights using Tavily Search.
- **Context Awareness**: Incorporates mock email and Teams transcript data for realistic proposal drafting.
- **Single-Draft Editor**: Unified text area for reviewing and editing the generated proposal.
- **Dynamic PPT Generation**: Creates branded PowerPoint presentations with sections for Executive Summary, Solution, and Investment.
- **Theme Support**: Iteratively customize the PPT theme using natural language (powered by Gemini).

## Setup Instructions

### 1. Prerequisites
- Python 3.9+
- [Gemini API Key](https://aistudio.google.com/app/apikey)
- [Tavily API Key](https://tavily.com/)

### 2. Installation
Clone the repository and install dependencies:
```bash
git clone <your-repo-url>
cd sales-proposal-gen
pip install -r requirements.txt
```

### 3. Environment Variables
Create a `.env` file in the root directory and add your API keys:
```env
GEMINI_API_KEY=your_gemini_api_key
TAVILY_API_KEY=your_tavily_api_key
```

### 4. Running the App
```bash
streamlit run app.py
```

## How to Use
1. Type `@SPG create proposal for [Company Name]` in the chat.
2. Review the generated draft in the text area.
3. Click "Generate PPT" to see a preview.
4. (Optional) Suggest theme changes like "Dark mode with neon accents" and click "Regenerate Theme".
5. Download your final PowerPoint proposal!

---
Built for NexusCRM Sales Teams.
