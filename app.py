import streamlit as st
import os
import re
from dotenv import load_dotenv
from tavily import TavilyClient
from google import genai
import json
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
import tempfile
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Mock Data
MOCK_EMAIL = "Subject: CRM Issues. From: John @ [Prospect]. Hi, we are struggling with data silos. Our current tool is too slow."
MOCK_TRANSCRIPT = "Teams Meeting: We need AI features. Budget is around $50k/year. Need implementation in Q1."

# Page configuration
st.set_page_config(
    page_title="NexusCRM Sales Proposal Copilot",
    page_icon="🤖",
    layout="wide"
)

# Custom CSS for styling
st.markdown("""
<style>
    /* Remove default Streamlit padding */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 0rem;
    }
    
    /* M365 background color */
    .stApp {
        background-color: #f3f2f1;
    }
    
    /* Font family */
    * {
        font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Hide Streamlit header and footer */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Chat message styling */
    .stChatMessage {
        background-color: white;
        border-radius: 8px;
        padding: 12px 16px;
        margin-bottom: 12px;
        box-shadow: 0 1px 2px rgba(0,0,0,0.08);
    }
    
    /* Input styling */
    .stChatInputContainer {
        border-top: 1px solid #e1dfdd;
        padding-top: 16px;
    }
    
    /* Right panel styling */
    .right-panel {
        background-color: #f5f5f5;
        padding: 20px;
        border-radius: 8px;
        border: 1px solid #e1dfdd;
        height: 100%;
    }
    
    /* Container styling for editable forms */
    .draft-container {
        background-color: white;
        border: 1px solid #e1dfdd;
        border-radius: 8px;
        padding: 16px;
        margin: 12px 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

if "company_data" not in st.session_state:
    st.session_state.company_data = {
        "name": "",
        "full_draft": "",
        "edited_full_draft": "",
        "ppt_theme": {
            "bg_color": [243, 242, 241],
            "title_color": [0, 120, 212],
            "body_color": [50, 49, 48],
            "accent_color": [0, 120, 212]
        }
    }

if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = ["Company_Overview.pdf", "Pricing_Tier_2025.pptx"]

# Helper Functions
def research_company(name):
    """Research company using Tavily and generate proposal content using the new Gemini SDK."""
    try:
        tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
        client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

        # 1. Search Tavily
        logger.info(f"Searching Tavily for {name}...")
        search_query = f"{name} strategic goals 2025 financial challenges recent news"
        search_result = tavily.search(query=search_query, search_depth="advanced")
        context = search_result.get("results", [])

        # 2. Generate Content with Gemini
        logger.info(f"Generating proposal for {name} using Gemini (gemini-2.0-flash)...")
        prompt = f"""
        You are writing a sales proposal from 'NexusCRM' (a CRM software company) to {name}.
        
        Context gathered:
        - Web Research: {json.dumps(context)}
        - Email from prospect: {MOCK_EMAIL}
        - Teams Meeting Notes: {MOCK_TRANSCRIPT}
        
        Based on this information, draft a sales proposal with 3 distinct sections.
        The values for each key MUST be a plain string (markdown formatted), NOT a nested JSON object.
        
        1. **Executive Summary**: Brief overview addressing their pain points (data silos, speed issues).
        2. **The NexusCRM Solution**: How our AI-powered CRM can help with their specific needs.
        3. **Investment**: Pricing proposal aligned with their ~$50k/year budget, including implementation timeline for Q1.

        Return the output strictly as a JSON object with keys: "executive_summary", "solution", "pricing".
        """

        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=prompt
        )
        content = response.text
        logger.info(f"Raw AI Response: {content}")
        
        if content.startswith("```json"):
            content = content.replace("```json", "").replace("```", "")
        if content.startswith("```"):
            content = content.replace("```", "")
            
        data = json.loads(content)
        
        # Ensure all values are strings (prevent nested JSON appearing in UI)
        for key in ["executive_summary", "solution", "pricing"]:
            if isinstance(data.get(key), (dict, list)):
                data[key] = json.dumps(data[key], indent=2)
                
        logger.info("Successfully parsed and cleaned response.")
        return data

    except Exception as e:
        logger.error(f"Error in research_company: {str(e)}", exc_info=True)
        st.error(f"NexusCRM Agent Error: {e}")
        return {
            "executive_summary": f"Research/AI Error: {str(e)}",
            "solution": "Check your .env for Tavily/Gemini API keys.",
            "pricing": "Internal Error."
        }

def get_theme_update(user_suggestion, current_theme):
    """Use Gemini to translate a theme suggestion into RGB values."""
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    prompt = f"""
    Current PPT Theme (RGB):
    {json.dumps(current_theme)}
    
    User Suggestion: "{user_suggestion}"
    
    Translate this suggestion into a new RGB theme. 
    Return strictly a JSON object with these keys:
    - bg_color: [R, G, B]
    - title_color: [R, G, B]
    - body_color: [R, G, B]
    - accent_color: [R, G, B]
    """
    try:
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=prompt
        )
        content = response.text
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0]
        elif "```" in content:
            content = content.split("```")[1].split("```")[0]
        return json.loads(content.strip())
    except:
        return current_theme

def generate_pptx(data):
    """Generate PowerPoint presentation based on content and theme."""
    prs = Presentation()
    theme = data.get('ppt_theme', {})
    
    def rgb_to_color(rgb_list):
        return RGBColor(rgb_list[0], rgb_list[1], rgb_list[2])

    bg_color = rgb_to_color(theme.get('bg_color', [255, 255, 255]))
    title_color = rgb_to_color(theme.get('title_color', [0, 120, 212]))
    body_color = rgb_to_color(theme.get('body_color', [0, 0, 0]))

    def add_slide(title_text, content_text):
        slide_layout = prs.slide_layouts[1]
        slide = prs.slides.add_slide(slide_layout)
        
        # Set background
        background = slide.background
        fill = background.fill
        fill.solid()
        fill.fore_color.rgb = bg_color
        
        title = slide.shapes.title
        title.text = title_text
        title.text_frame.paragraphs[0].font.color.rgb = title_color
        title.text_frame.paragraphs[0].font.bold = True
        
        content = slide.placeholders[1]
        content.text = content_text
        # Optional: Set body color if needed (more complex to iterate all runs)

    # Parsing logic
    draft = data.get('edited_full_draft', '')
    sections = {}
    current_key = "Executive Summary"
    for line in draft.split('\n'):
        if re.match(r'^(#|##|\*\*)\s*(Executive Summary|Understanding)', line, re.I):
            current_key = "Executive Summary"
            sections[current_key] = ""
        elif re.match(r'^(#|##|\*\*)\s*(Solution|The Nexus)', line, re.I):
            current_key = "Solution"
            sections[current_key] = ""
        elif re.match(r'^(#|##|\*\*)\s*(Investment|Pricing)', line, re.I):
            current_key = "Investment"
            sections[current_key] = ""
        else:
            if current_key:
                sections[current_key] = sections.get(current_key, "") + line + "\n"

    # Slide 1: Title
    slide_layout = prs.slide_layouts[0]
    slide = prs.slides.add_slide(slide_layout)
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = bg_color
    
    title = slide.shapes.title
    title.text = f"NexusCRM → {data['name']}"
    title.text_frame.paragraphs[0].font.color.rgb = title_color
    
    subtitle = slide.placeholders[1]
    subtitle.text = "Strategic Proposal for Digital Transformation"

    # slides 2-4
    add_slide("Understanding Your Needs", sections.get("Executive Summary", "Details in full draft."))
    add_slide("The NexusCRM Solution", sections.get("Solution", "Details in full draft."))
    add_slide("Investment/Pricing", sections.get("Investment", "Details in full draft."))

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pptx")
    prs.save(temp_file.name)
    return temp_file.name

# Main Layout: Two Columns
chat_col, right_panel = st.columns([0.7, 0.3])

# ===== RIGHT PANEL =====
with right_panel:
    st.markdown('<div class="right-panel">', unsafe_allow_html=True)
    
    # Tools Section
    st.markdown("### Tools")
    st.success("✅ Outlook - Active")
    st.success("✅ Teams - Active")
    
    st.markdown("---")
    
    # Knowledge Section
    st.markdown("### Knowledge")
    uploaded_file = st.file_uploader(
        "Upload Past Proposals/Brochures",
        type=["pdf", "pptx"],
        help="Upload reference documents to improve proposal quality"
    )
    
    if uploaded_file:
        if uploaded_file.name not in st.session_state.uploaded_files:
            st.session_state.uploaded_files.append(uploaded_file.name)
    
    st.markdown("**Active Files:**")
    for file in st.session_state.uploaded_files:
        st.markdown(f"- 📄 {file}")
    
    st.markdown('</div>', unsafe_allow_html=True)

# ===== CHAT COLUMN =====
with chat_col:
    st.title("🤖 NexusCRM Sales Proposal Copilot")
    st.markdown("---")
    
    # Display chat messages
    for message in st.session_state.messages:
        avatar = "https://upload.wikimedia.org/wikipedia/en/a/aa/Microsoft_Copilot_Icon.svg" if message["role"] == "assistant" else "https://ui-avatars.com/api/?name=User&background=random"
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])
            
            # Show draft editor if this message has it
            if message.get("show_editor"):
                with st.container():
                    st.markdown('<div class="draft-container">', unsafe_allow_html=True)
                    st.subheader("Edit Proposal Draft")
                    st.session_state.company_data["edited_full_draft"] = st.text_area(
                        "Edit the proposal content below. Use markdown headers for sections.", 
                        value=st.session_state.company_data["edited_full_draft"],
                        height=500,
                        key=f"full_draft_{message.get('id', 0)}"
                    )
                    
                    if st.button("Generate PPT", key=f"confirm_{message.get('id', 0)}"):
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": "Generating your PowerPoint presentation...",
                            "show_download": True,
                            "id": len(st.session_state.messages)
                        })
                        st.rerun()
                    
                    st.markdown('</div>', unsafe_allow_html=True)
            
            # Show download/preview button if this message has it
            if message.get("show_download"):
                with st.container():
                    st.markdown('<div class="draft-container">', unsafe_allow_html=True)
                    st.subheader("PPT Preview & Customization")
                    
                    # PPT Viewer Simulation
                    tabs = st.tabs(["Slide 1", "Slide 2", "Slide 3", "Slide 4"])
                    
                    # Render mock slides in tabs
                    draft_text = st.session_state.company_data["edited_full_draft"]
                    # (Quick split for preview)
                    prev_sections = {"Executive Summary": "", "Solution": "", "Investment": ""}
                    curr = "Executive Summary"
                    for l in draft_text.split('\n'):
                        if "Executive Summary" in l: curr = "Executive Summary"
                        elif "Solution" in l: curr = "Solution"
                        elif "Investment" in l: curr = "Investment"
                        else: prev_sections[curr] += l + "\n"

                    theme = st.session_state.company_data["ppt_theme"]
                    bg_hex = '#%02x%02x%02x' % tuple(theme['bg_color'])
                    text_hex = '#%02x%02x%02x' % tuple(theme['title_color'])

                    def slide_style(content):
                        return f"""
                        <div style="background-color: {bg_hex}; border: 1px solid #ccc; padding: 20px; border-radius: 5px; min-height: 200px; color: {text_hex};">
                            <h3 style="color: {text_hex};">{content['title']}</h3>
                            <p style="color: #333; font-size: 14px;">{content['body'][:300]}...</p>
                        </div>
                        """

                    tabs[0].markdown(slide_style({"title": f"NexusCRM → {st.session_state.company_data['name']}", "body": "Strategic Proposal"}), unsafe_allow_html=True)
                    tabs[1].markdown(slide_style({"title": "Needs", "body": prev_sections["Executive Summary"]}), unsafe_allow_html=True)
                    tabs[2].markdown(slide_style({"title": "Solution", "body": prev_sections["Solution"]}), unsafe_allow_html=True)
                    tabs[3].markdown(slide_style({"title": "Investment", "body": prev_sections["Investment"]}), unsafe_allow_html=True)

                    st.markdown("---")
                    theme_suggestion = st.text_input("🎨 Suggest your theme changes", placeholder="e.g. Dark mode with gold accents", key=f"theme_input_{message.get('id', 0)}")
                    
                    col1, col2 = st.columns(2)
                    if col1.button("🔄 Regenerate Theme", key=f"regen_{message.get('id', 0)}"):
                        if theme_suggestion:
                            with st.spinner("Applying theme changes..."):
                                new_theme = get_theme_update(theme_suggestion, st.session_state.company_data["ppt_theme"])
                                st.session_state.company_data["ppt_theme"] = new_theme
                                st.rerun()

                    try:
                        pptx_path = generate_pptx(st.session_state.company_data)
                        with open(pptx_path, "rb") as f:
                            col2.download_button(
                                "📥 Download Final (PPTX)",
                                f,
                                file_name=f"NexusCRM_Proposal_{st.session_state.company_data['name']}.pptx",
                                mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                                key=f"download_{message.get('id', 0)}"
                            )
                    except Exception as e:
                        st.error(f"Error: {e}")
                    
                    st.markdown('</div>', unsafe_allow_html=True)

    # Chat input
    if prompt := st.chat_input("Ask Copilot... (Try: @SPG create proposal for Tesla)"):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Check for @SPG trigger
        spg_match = re.search(r"@SPG.*for\s+(.+)", prompt, re.IGNORECASE)
        
        if spg_match:
            company_name = spg_match.group(1).strip()
            st.session_state.company_data["name"] = company_name
            
            # Show thinking message
            with st.chat_message("assistant", avatar="https://upload.wikimedia.org/wikipedia/en/a/aa/Microsoft_Copilot_Icon.svg"):
                # Status 1: Web Search
                with st.spinner(f"🔍 Searching Web for {company_name}..."):
                    try:
                        research_results = research_company(company_name)
                    except Exception as e:
                        st.error(f"Error during research: {e}")
                        research_results = {
                            "executive_summary": "Unable to complete research.",
                            "solution": "Unable to complete research.",
                            "pricing": "Unable to complete research."
                        }
                
                # Status 2: Reading Emails & Teams
                with st.spinner("📧 Reading Emails & Teams Logs..."):
                    st.write(f"**Email Context:** {MOCK_EMAIL[:50]}...")
                    st.write(f"**Teams Context:** {MOCK_TRANSCRIPT[:50]}...")
                
                # Status 3: Analyzing Knowledge
                with st.spinner("📂 Analyzing Knowledge Base..."):
                    st.write(f"**Analyzing {len(st.session_state.uploaded_files)} files...**")
                
                full_draft = f"## Executive Summary\n{research_results.get('executive_summary', '')}\n\n"
                full_draft += f"## Solution\n{research_results.get('solution', '')}\n\n"
                full_draft += f"## Investment\n{research_results.get('pricing', '')}"
                
                st.session_state.company_data["full_draft"] = full_draft
                st.session_state.company_data["edited_full_draft"] = full_draft
                
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": f"I've gathered insights on **{company_name}** from web research, your email/Teams history, and the knowledge base. Here's a draft proposal - please review and edit:",
                    "show_editor": True,
                    "id": len(st.session_state.messages)
                })
            
            st.rerun()
        else:
            # Generic response
            st.session_state.messages.append({
                "role": "assistant",
                "content": "👋 I'm the **NexusCRM Sales Proposal Agent**. Tag me with `@SPG create proposal for [Company Name]` to get started!"
            })
            st.rerun()
