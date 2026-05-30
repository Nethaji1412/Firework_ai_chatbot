import streamlit as st
from openai import OpenAI
 
# =====================================================
# PAGE CONFIG
# =====================================================
 
st.set_page_config(
    page_title="JARVIS AI",
    page_icon="",
    layout="wide",
    initial_sidebar_state="collapsed"
)
 
# =====================================================
# SESSION STATE DEFAULTS
# =====================================================
 
if "messages" not in st.session_state:
    st.session_state.messages = []
if "selected_model" not in st.session_state:
    st.session_state.selected_model = None
if "temperature" not in st.session_state:
    st.session_state.temperature = 0.7
if "max_tokens" not in st.session_state:
    st.session_state.max_tokens = 1024
if "show_config" not in st.session_state:
    st.session_state.show_config = False
 
# =====================================================
# CSS
# =====================================================
 
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;600&display=swap');
 
*, *::before, *::after { box-sizing: border-box; }
 
html, body, [data-testid="stAppViewContainer"] {
    background: #020b18 !important;
    color: #c8e6ff !important;
    font-family: 'Rajdhani', sans-serif !important;
}
 
/* Hide default Streamlit sidebar toggle arrow */
[data-testid="collapsedControl"] { display: none !important; }
 
/* Hide sidebar entirely */
[data-testid="stSidebar"] { display: none !important; }
 
/* Neural dot background */
[data-testid="stAppViewContainer"]::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image:
        radial-gradient(circle, rgba(0,180,255,0.15) 1px, transparent 1px),
        radial-gradient(circle, rgba(255,140,0,0.08) 1px, transparent 1px);
    background-size: 60px 60px, 90px 90px;
    background-position: 0 0, 30px 45px;
    animation: neuralDrift 20s linear infinite;
    pointer-events: none;
    z-index: 0;
}
@keyframes neuralDrift {
    0%   { background-position: 0 0, 30px 45px; }
    100% { background-position: 60px 60px, 90px 105px; }
}
 
/* Main block padding */
[data-testid="stMainBlockContainer"] {
    padding-top: 1rem !important;
    padding-bottom: 6rem !important;
}
 
/* ── Header bar ── */
.jarvis-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 0 1rem 0;
    border-bottom: 1px solid rgba(0,180,255,0.12);
    margin-bottom: 1.2rem;
}
.jarvis-title {
    font-family: 'Orbitron', sans-serif;
    font-weight: 900;
    font-size: 1.9rem;
    background: linear-gradient(90deg, #00b4ff 0%, #ffffff 50%, #ff8c00 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: 4px;
    animation: titlePulse 4s ease-in-out infinite;
    margin: 0;
}
@keyframes titlePulse {
    0%, 100% { filter: brightness(1); }
    50%       { filter: brightness(1.35); }
}
.jarvis-subtitle {
    font-family: 'Rajdhani', sans-serif;
    font-size: 0.75rem;
    letter-spacing: 3px;
    color: rgba(0,180,255,0.45);
    margin: 2px 0 0 0;
}
.header-right {
    display: flex;
    align-items: center;
    gap: 10px;
}
.model-badge {
    font-family: 'Rajdhani', sans-serif;
    font-size: 0.78rem;
    letter-spacing: 1px;
    color: rgba(0,180,255,0.6);
    background: rgba(0,30,70,0.6);
    border: 1px solid rgba(0,180,255,0.2);
    border-radius: 20px;
    padding: 4px 12px;
}
 
/* ── Config panel ── */
.config-panel {
    background: rgba(0,15,40,0.92);
    border: 1px solid rgba(0,180,255,0.25);
    border-radius: 16px;
    padding: 20px 24px;
    margin-bottom: 1.5rem;
    backdrop-filter: blur(12px);
    animation: panelSlide 0.25s ease-out;
}
@keyframes panelSlide {
    from { opacity: 0; transform: translateY(-10px); }
    to   { opacity: 1; transform: translateY(0); }
}
.config-title {
    font-family: 'Orbitron', sans-serif;
    font-size: 0.75rem;
    letter-spacing: 3px;
    color: #00b4ff;
    text-shadow: 0 0 10px rgba(0,180,255,0.5);
    margin: 0 0 16px 0;
}
.config-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
}
 
/* Streamlit widgets inside config */
[data-testid="stSelectbox"] > div > div {
    background: rgba(0,20,55,0.85) !important;
    border: 1px solid rgba(0,180,255,0.3) !important;
    color: #c8e6ff !important;
    border-radius: 10px !important;
    font-family: 'Rajdhani', sans-serif !important;
}
[data-testid="stSlider"] > div > div > div {
    background: rgba(0,180,255,0.15) !important;
}
[data-testid="stSlider"] [data-baseweb="slider"] div[role="slider"] {
    background: #00b4ff !important;
    box-shadow: 0 0 10px #00b4ff !important;
}
label[data-testid="stWidgetLabel"] p {
    color: rgba(0,180,255,0.7) !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 0.85rem !important;
    letter-spacing: 1px !important;
}
 
/* ── Buttons ── */
button[kind="secondary"], button[data-testid="baseButton-secondary"] {
    background: rgba(0,30,70,0.7) !important;
    border: 1px solid rgba(0,180,255,0.35) !important;
    color: #00b4ff !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-weight: 600 !important;
    letter-spacing: 1.5px !important;
    border-radius: 10px !important;
    transition: all 0.25s ease !important;
}
button[kind="secondary"]:hover, button[data-testid="baseButton-secondary"]:hover {
    background: rgba(0,180,255,0.12) !important;
    box-shadow: 0 0 14px rgba(0,180,255,0.25) !important;
    border-color: rgba(0,180,255,0.6) !important;
}
 
/* Primary button (config toggle) */
button[kind="primary"], button[data-testid="baseButton-primary"] {
    background: linear-gradient(135deg, rgba(0,100,200,0.4), rgba(0,50,130,0.5)) !important;
    border: 1px solid rgba(0,180,255,0.5) !important;
    color: #00d4ff !important;
    font-family: 'Orbitron', sans-serif !important;
    font-size: 0.7rem !important;
    letter-spacing: 2px !important;
    border-radius: 10px !important;
    box-shadow: 0 0 12px rgba(0,180,255,0.15) !important;
    transition: all 0.25s ease !important;
}
button[kind="primary"]:hover, button[data-testid="baseButton-primary"]:hover {
    box-shadow: 0 0 22px rgba(0,180,255,0.35) !important;
    border-color: rgba(0,220,255,0.7) !important;
}
 
/* ── Chat messages ── */
[data-testid="stChatMessage"] {
    background: rgba(0,20,50,0.55) !important;
    border: 1px solid rgba(0,180,255,0.1) !important;
    border-radius: 14px !important;
    backdrop-filter: blur(6px) !important;
    margin-bottom: 10px !important;
    padding: 14px 18px !important;
    transition: border-color 0.3s ease !important;
}
[data-testid="stChatMessage"]:hover {
    border-color: rgba(0,180,255,0.28) !important;
}
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
    border-left: 3px solid rgba(255,140,0,0.55) !important;
    background: rgba(28,12,0,0.45) !important;
}
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) {
    border-left: 3px solid rgba(0,180,255,0.55) !important;
}
[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] li,
[data-testid="stChatMessage"] td {
    color: #c8e6ff !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 1.05rem !important;
    line-height: 1.7 !important;
}
[data-testid="stChatMessage"] code {
    background: rgba(0,180,255,0.1) !important;
    color: #7dd3fc !important;
    border: 1px solid rgba(0,180,255,0.2) !important;
    border-radius: 4px !important;
    padding: 1px 5px !important;
}
[data-testid="stChatMessage"] pre {
    background: rgba(0,10,30,0.85) !important;
    border: 1px solid rgba(0,180,255,0.2) !important;
    border-radius: 10px !important;
}
 
/* ── Welcome screen ── */
.welcome-wrap {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 3rem 1rem 2rem;
    text-align: center;
}
.welcome-brain {
    width: 90px;
    height: 90px;
    margin-bottom: 1.2rem;
    animation: brainPulse 2.5s ease-in-out infinite;
    filter: drop-shadow(0 0 14px rgba(0,180,255,0.7));
}
@keyframes brainPulse {
    0%, 100% { transform: scale(1);   filter: drop-shadow(0 0 10px rgba(0,180,255,0.6)); }
    50%       { transform: scale(1.07); filter: drop-shadow(0 0 22px rgba(0,180,255,0.95)); }
}
.welcome-heading {
    font-family: 'Orbitron', sans-serif;
    font-size: 1.1rem;
    letter-spacing: 4px;
    color: #00b4ff;
    text-shadow: 0 0 16px rgba(0,180,255,0.5);
    margin: 0 0 8px;
}
.welcome-sub {
    font-family: 'Rajdhani', sans-serif;
    font-size: 1rem;
    color: rgba(140,200,240,0.55);
    letter-spacing: 1px;
    margin: 0 0 1.8rem;
}
.suggestions {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    justify-content: center;
    max-width: 680px;
}
.suggestion-chip {
    background: rgba(0,30,70,0.7);
    border: 1px solid rgba(0,180,255,0.22);
    border-radius: 24px;
    padding: 8px 18px;
    font-family: 'Rajdhani', sans-serif;
    font-size: 0.9rem;
    color: rgba(160,210,255,0.8);
    cursor: pointer;
    transition: all 0.2s ease;
    letter-spacing: 0.5px;
}
.suggestion-chip:hover {
    background: rgba(0,80,180,0.25);
    border-color: rgba(0,180,255,0.5);
    color: #c8e6ff;
    box-shadow: 0 0 10px rgba(0,180,255,0.15);
}
 
/* ── Brain thinking animation ── */
.brain-thinking {
    display: flex;
    align-items: center;
    gap: 14px;
    padding: 14px 18px;
    background: rgba(0,20,50,0.7);
    border: 1px solid rgba(0,180,255,0.2);
    border-left: 3px solid rgba(0,180,255,0.6);
    border-radius: 14px;
    margin-bottom: 10px;
}
.brain-svg {
    flex-shrink: 0;
    width: 44px;
    height: 44px;
    animation: brainPulse 2s ease-in-out infinite;
    filter: drop-shadow(0 0 8px rgba(0,180,255,0.7));
}
.brain-right { display: flex; flex-direction: column; gap: 7px; }
.brain-label {
    font-family: 'Orbitron', sans-serif;
    font-size: 0.7rem;
    letter-spacing: 3px;
    color: #00b4ff;
    animation: labelFlicker 3s ease-in-out infinite;
}
@keyframes labelFlicker {
    0%, 88%, 100% { opacity: 1; }
    93% { opacity: 0.35; }
}
.synapses { display: flex; gap: 5px; align-items: center; }
.synapse {
    width: 7px; height: 7px; border-radius: 50%;
    animation: synapsefire 1.4s ease-in-out infinite;
}
.synapse:nth-child(1) { background:#00b4ff; animation-delay:0s; }
.synapse:nth-child(2) { background:#0090e0; animation-delay:0.2s; }
.synapse:nth-child(3) { background:#ff8c00; animation-delay:0.4s; }
.synapse:nth-child(4) { background:#0090e0; animation-delay:0.6s; }
.synapse:nth-child(5) { background:#00b4ff; animation-delay:0.8s; }
.synapse:nth-child(6) { background:#ff8c00; animation-delay:1.0s; }
.synapse:nth-child(7) { background:#0090e0; animation-delay:1.2s; }
@keyframes synapsefire {
    0%,100% { transform:scale(1);   opacity:0.3; box-shadow:none; }
    50%      { transform:scale(1.6); opacity:1;   box-shadow:0 0 8px currentColor; }
}
.neural-bar {
    width: 170px; height: 3px;
    background: rgba(0,180,255,0.12);
    border-radius: 3px; overflow: hidden;
}
.neural-bar-fill {
    height: 100%; width: 35%;
    background: linear-gradient(90deg, transparent, #00b4ff, #ff8c00, #00b4ff, transparent);
    border-radius: 3px;
    animation: neuralScan 1.8s ease-in-out infinite;
}
@keyframes neuralScan {
    0%   { transform: translateX(-250%); }
    100% { transform: translateX(450%); }
}
 
/* ── Chat input ── */
[data-testid="stChatInput"] {
    background: rgba(0,20,50,0.75) !important;
    border: 1px solid rgba(0,180,255,0.28) !important;
    border-radius: 30px !important;
    backdrop-filter: blur(10px) !important;
    box-shadow: 0 0 20px rgba(0,180,255,0.08) !important;
}
[data-testid="stChatInput"]:focus-within {
    border-color: rgba(0,180,255,0.65) !important;
    box-shadow: 0 0 28px rgba(0,180,255,0.22) !important;
}
[data-testid="stChatInput"] textarea {
    color: #c8e6ff !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 1rem !important;
    background: transparent !important;
}
[data-testid="stChatInput"] textarea::placeholder {
    color: rgba(0,180,255,0.3) !important;
}
[data-testid="stChatInput"] button {
    background: radial-gradient(circle, rgba(0,150,255,0.4), rgba(0,60,150,0.4)) !important;
    border: 1px solid rgba(0,180,255,0.5) !important;
    border-radius: 50% !important;
    box-shadow: 0 0 10px rgba(0,180,255,0.25) !important;
}
 
/* ── Caption / footer ── */
[data-testid="stCaptionContainer"] p {
    color: rgba(0,180,255,0.35) !important;
    font-family: 'Rajdhani', sans-serif !important;
    letter-spacing: 2px !important;
    font-size: 0.8rem !important;
}
hr { border-color: rgba(0,180,255,0.08) !important; }
 
/* Scrollbar */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: #010c1a; }
::-webkit-scrollbar-thumb { background: rgba(0,180,255,0.25); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: rgba(0,180,255,0.5); }
 
/* Hide streamlit branding */
#MainMenu, footer, header { visibility: hidden !important; }
</style>
""", unsafe_allow_html=True)
 
# =====================================================
# BRAIN SVG (reusable)
# =====================================================
 
BRAIN_SVG = """
<svg viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
  <path d="M32 8C24 8 18 13 17 20C13 20 10 23 10 27C8 28 6 31 7 35C6 38 8 42 12 43C13 47 17 50 22 50C24 52 27 53 32 53C37 53 40 52 42 50C47 50 51 47 52 43C56 42 58 38 57 35C58 31 56 28 54 27C54 23 51 20 47 20C46 13 40 8 32 8Z"
    stroke="#00b4ff" stroke-width="1.5" fill="rgba(0,40,100,0.3)"/>
  <line x1="32" y1="8"  x2="32" y2="53" stroke="rgba(0,180,255,0.2)" stroke-width="0.5"/>
  <line x1="17" y1="20" x2="47" y2="20" stroke="rgba(0,180,255,0.2)" stroke-width="0.5"/>
  <line x1="12" y1="43" x2="52" y2="43" stroke="rgba(0,180,255,0.2)" stroke-width="0.5"/>
  <circle cx="32" cy="20" r="2" fill="#ff8c00"><animate attributeName="opacity" values="0.3;1;0.3" dur="1.2s" repeatCount="indefinite"/></circle>
  <circle cx="20" cy="31" r="2" fill="#00b4ff"><animate attributeName="opacity" values="1;0.3;1" dur="1.4s" repeatCount="indefinite"/></circle>
  <circle cx="44" cy="31" r="2" fill="#00b4ff"><animate attributeName="opacity" values="0.3;1;0.3" dur="1.0s" repeatCount="indefinite"/></circle>
  <circle cx="32" cy="42" r="2" fill="#ff8c00"><animate attributeName="opacity" values="1;0.3;1" dur="1.6s" repeatCount="indefinite"/></circle>
  <circle cx="25" cy="25" r="1.5" fill="#7dd3fc"><animate attributeName="opacity" values="0.2;1;0.2" dur="0.9s" repeatCount="indefinite"/></circle>
  <circle cx="39" cy="25" r="1.5" fill="#7dd3fc"><animate attributeName="opacity" values="1;0.2;1" dur="1.1s" repeatCount="indefinite"/></circle>
  <line x1="20" y1="31" x2="32" y2="20" stroke="#00b4ff" stroke-width="0.8"><animate attributeName="opacity" values="0.1;0.7;0.1" dur="1.3s" repeatCount="indefinite"/></line>
  <line x1="44" y1="31" x2="32" y2="20" stroke="#00b4ff" stroke-width="0.8"><animate attributeName="opacity" values="0.7;0.1;0.7" dur="1.3s" repeatCount="indefinite"/></line>
  <line x1="20" y1="31" x2="32" y2="42" stroke="#ff8c00" stroke-width="0.8"><animate attributeName="opacity" values="0.1;0.8;0.1" dur="1.5s" repeatCount="indefinite"/></line>
  <line x1="44" y1="31" x2="32" y2="42" stroke="#ff8c00" stroke-width="0.8"><animate attributeName="opacity" values="0.8;0.1;0.8" dur="1.5s" repeatCount="indefinite"/></line>
</svg>
"""
 
BRAIN_THINKING_HTML = f"""
<div class="brain-thinking">
  <svg class="brain-svg" viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M32 8C24 8 18 13 17 20C13 20 10 23 10 27C8 28 6 31 7 35C6 38 8 42 12 43C13 47 17 50 22 50C24 52 27 53 32 53C37 53 40 52 42 50C47 50 51 47 52 43C56 42 58 38 57 35C58 31 56 28 54 27C54 23 51 20 47 20C46 13 40 8 32 8Z"
      stroke="#00b4ff" stroke-width="1.5" fill="rgba(0,40,100,0.3)"/>
    <circle cx="32" cy="20" r="2" fill="#ff8c00"><animate attributeName="opacity" values="0.3;1;0.3" dur="1.2s" repeatCount="indefinite"/></circle>
    <circle cx="20" cy="31" r="2" fill="#00b4ff"><animate attributeName="opacity" values="1;0.3;1" dur="1.4s" repeatCount="indefinite"/></circle>
    <circle cx="44" cy="31" r="2" fill="#00b4ff"><animate attributeName="opacity" values="0.3;1;0.3" dur="1.0s" repeatCount="indefinite"/></circle>
    <circle cx="32" cy="42" r="2" fill="#ff8c00"><animate attributeName="opacity" values="1;0.3;1" dur="1.6s" repeatCount="indefinite"/></circle>
    <line x1="20" y1="31" x2="32" y2="20" stroke="#00b4ff" stroke-width="0.8"><animate attributeName="opacity" values="0.1;0.7;0.1" dur="1.3s" repeatCount="indefinite"/></line>
    <line x1="44" y1="31" x2="32" y2="42" stroke="#ff8c00" stroke-width="0.8"><animate attributeName="opacity" values="0.8;0.1;0.8" dur="1.5s" repeatCount="indefinite"/></line>
  </svg>
  <div class="brain-right">
    <div class="brain-label">NEURAL PROCESSING ...</div>
    <div class="synapses">
      <div class="synapse"></div><div class="synapse"></div><div class="synapse"></div>
      <div class="synapse"></div><div class="synapse"></div><div class="synapse"></div>
      <div class="synapse"></div>
    </div>
    <div class="neural-bar"><div class="neural-bar-fill"></div></div>
  </div>
</div>
"""
 
# =====================================================
# API CONFIG  ← paste your key here
# =====================================================
 
API_KEY = "fw_TUbfVQ2rJ6sJpuWPptaHoC"
 
BASE_URL = "https://api.fireworks.ai/inference/v1"
client = OpenAI(api_key=API_KEY, base_url=BASE_URL)
 
# =====================================================
# SYSTEM PROMPT
# =====================================================
 
SYSTEM_PROMPT = SYSTEM_PROMPT = """
You are JARVIS, the personal AI assistant of Nethaji.
you always call him as Sir

About Nethaji:
- Nethaji is an AI/ML Engineer.
- He is passionate about learning, building, experimenting, and improving.
- He enjoys understanding concepts deeply rather than just getting answers.
- He values practical solutions, technical excellence, and continuous growth.

Your Role:
- Act as Nethaji's trusted AI companion, technical partner, mentor, researcher, and productivity assistant.
- Help him learn faster, think deeper, and build better solutions.
- Be proactive in suggesting improvements, optimizations, and alternative approaches.
- Function like a highly intelligent personal assistant similar to JARVIS from Iron Man: knowledgeable, reliable, efficient, and supportive.

Core Principles:

1. Accuracy First
- Prioritize factual correctness.
- Never fabricate information, code behavior, or technical results.
- Clearly state uncertainty when necessary.
- Ask clarifying questions when requirements are unclear.

2. Engineering Mindset
- Think like a senior engineer.
- Analyze problems before solving them.
- Consider scalability, maintainability, security, performance, and cost.
- Explain trade-offs between different approaches.
- Recommend industry best practices.

3. AI & ML Expertise
- Provide strong support in:
  - Artificial Intelligence
  - Machine Learning
  - Deep Learning
  - Generative AI
  - LLMs and Agent Systems
  - RAG Architectures
  - Data Science
  - Python
  - SQL
  - FastAPI
  - Cloud Technologies
  - MLOps
  - System Design
- Explain concepts from beginner to advanced levels when needed.

4. Learning Companion
- Help Nethaji continuously learn and improve.
- Teach concepts, not just answers.
- Break complex topics into understandable steps.
- Provide real-world examples and practical applications.
- Recommend learning paths, resources, and best practices.

5. Friendly & Human
- Communicate naturally and conversationally.
- Be encouraging and collaborative.
- Treat discussions as teamwork rather than simple question-answer exchanges.
- Maintain professionalism while being approachable and friendly.

6. Proactive Thinking
- Anticipate edge cases and potential issues.
- Suggest optimizations and automation opportunities.
- Identify better solutions when appropriate.
- Think one step ahead.

7. Coding Standards
- Generate clean, production-ready code.
- Follow modern best practices.
- Write maintainable and readable solutions.
- Explain important implementation decisions.
- Include error handling and edge cases when relevant.

8. Research & Problem Solving
For complex tasks:
- Understand the goal.
- Analyze the requirements.
- Identify constraints.
- Explore possible solutions.
- Recommend the best approach.
- Explain reasoning clearly.
- Suggest future improvements.

Response Style:
- Clear and structured.
- Concise for simple questions.
- Detailed for complex topics.
- Use markdown formatting.
- Use headings, bullet points, tables, and code blocks when helpful.

Personality:
- Intelligent like JARVIS.
- Curious like a researcher.
- Practical like an engineer.
- Supportive like a trusted friend.
- Always eager to learn, adapt, and improve alongside Nethaji.

Primary Objective:
Help Nethaji learn faster, build smarter, solve problems effectively, and continuously grow as an AI/ML engineer.
"""
 
# =====================================================
# MODEL FETCHING — auto-selects best available model
# =====================================================
 
@st.cache_data(show_spinner="🧠 Initialising neural networks...")
def get_working_model():
    """Fetch available models and return first usable one by priority."""
    try:
        models = client.models.list()
        priority_keywords = ["llama", "deepseek", "mixtral", "firefunction", "qwen"]
        model_ids = [m.id for m in models.data]
        for keyword in priority_keywords:
            for m in model_ids:
                if keyword in m.lower():
                    return m
        # Fallback: return whatever is first
        return model_ids[0] if model_ids else None
    except Exception as e:
        st.error(f"Error fetching models: {e}")
        return None
 
if st.session_state.selected_model is None:
    st.session_state.selected_model = get_working_model()
 
# =====================================================
# HEADER
# =====================================================
 
model_short = (st.session_state.selected_model or "").split("/")[-1]
 
st.markdown(f"""
<div class="jarvis-header">
  <div>
    <div class="jarvis-title">JARVIS AI</div>
    <div class="jarvis-subtitle">NEURAL INTELLIGENCE SYSTEM</div>
  </div>
  <div class="header-right">
    <span class="model-badge">⚡ {model_short}</span>
  </div>
</div>
""", unsafe_allow_html=True)
 
# =====================================================
# CONFIG TOGGLE BUTTON ROW
# =====================================================
 
btn_col1, btn_col2, btn_col3 = st.columns([1, 1, 6])
 
with btn_col1:
    cfg_label = "✦ CONFIG ▲" if st.session_state.show_config else "✦ CONFIG ▼"
    if st.button(cfg_label, key="toggle_config", type="primary", use_container_width=True):
        st.session_state.show_config = not st.session_state.show_config
        st.rerun()
 
with btn_col2:
    if st.button("🗑 CLEAR", key="clear_chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
 
# =====================================================
# COLLAPSIBLE CONFIG PANEL
# =====================================================
 
if st.session_state.show_config:
    st.markdown('<div class="config-panel"><div class="config-title">⚙ SYSTEM CONFIGURATION</div>', unsafe_allow_html=True)
 
    cfg1, cfg2, cfg3 = st.columns([2, 1, 1])
 
    with cfg1:
        model_display = (st.session_state.selected_model or "None").split("/")[-1]
        st.markdown(f"""
        <div style="padding:8px 0;">
          <div style="font-family:Rajdhani,sans-serif;font-size:0.82rem;letter-spacing:1px;color:rgba(0,180,255,0.7);margin-bottom:4px;">🧬 AUTO-SELECTED MODEL</div>
          <div style="font-family:Orbitron,sans-serif;font-size:0.78rem;color:#00d4ff;background:rgba(0,30,70,0.7);border:1px solid rgba(0,180,255,0.3);border-radius:8px;padding:8px 14px;letter-spacing:1px;">
            ⚡ {model_display}
          </div>
          <div style="font-family:Rajdhani,sans-serif;font-size:0.72rem;color:rgba(0,180,255,0.4);margin-top:4px;letter-spacing:1px;">Selected by priority: llama › deepseek › mixtral › qwen</div>
        </div>
        """, unsafe_allow_html=True)
 
    with cfg2:
        st.session_state.temperature = st.slider(
            "🌡 Temperature", 0.0, 1.5,
            st.session_state.temperature, 0.1,
            help="Higher = more creative"
        )
 
    with cfg3:
        st.session_state.max_tokens = st.slider(
            "⚡ Max Tokens", 100, 4096,
            st.session_state.max_tokens, 100,
            help="Max response length"
        )
 
    st.markdown('</div>', unsafe_allow_html=True)
 
# =====================================================
# WELCOME SCREEN (when no messages)
# =====================================================
 
SUGGESTIONS = [
    "🐍 Write a Python web scraper",
    "🧠 Explain neural networks",
    "📊 Write a SQL query for sales data",
    "🔧 Debug my code",
    "📝 Summarise a research paper",
    "🚀 Build a REST API in FastAPI",
]
 
if not st.session_state.messages:
    chips_html = "".join(
        f'<div class="suggestion-chip" onclick="void(0)">{s}</div>'
        for s in SUGGESTIONS
    )
    st.markdown(f"""
    <div class="welcome-wrap">
      <svg class="welcome-brain" viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M32 8C24 8 18 13 17 20C13 20 10 23 10 27C8 28 6 31 7 35C6 38 8 42 12 43C13 47 17 50 22 50C24 52 27 53 32 53C37 53 40 52 42 50C47 50 51 47 52 43C56 42 58 38 57 35C58 31 56 28 54 27C54 23 51 20 47 20C46 13 40 8 32 8Z"
          stroke="#00b4ff" stroke-width="1.5" fill="rgba(0,40,100,0.25)"/>
        <circle cx="32" cy="20" r="2.5" fill="#ff8c00"><animate attributeName="opacity" values="0.3;1;0.3" dur="1.2s" repeatCount="indefinite"/></circle>
        <circle cx="20" cy="31" r="2.5" fill="#00b4ff"><animate attributeName="opacity" values="1;0.3;1" dur="1.4s" repeatCount="indefinite"/></circle>
        <circle cx="44" cy="31" r="2.5" fill="#00b4ff"><animate attributeName="opacity" values="0.3;1;0.3" dur="1.0s" repeatCount="indefinite"/></circle>
        <circle cx="32" cy="42" r="2.5" fill="#ff8c00"><animate attributeName="opacity" values="1;0.3;1" dur="1.6s" repeatCount="indefinite"/></circle>
      </svg>
      <div class="welcome-heading">ONLINE · READY</div>
      <div class="welcome-sub">What can I process for you today?</div>
      <div class="suggestions">{chips_html}</div>
    </div>
    """, unsafe_allow_html=True)
 
    # Clickable suggestion buttons (functional)
    st.markdown("---")
    cols = st.columns(3)
    for i, s in enumerate(SUGGESTIONS):
        with cols[i % 3]:
            if st.button(s, key=f"sug_{i}", use_container_width=True):
                st.session_state.messages.append({"role": "user", "content": s})
                st.rerun()
 
# =====================================================
# CHAT HISTORY
# =====================================================
 
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
 
# =====================================================
# CHAT INPUT + RESPONSE
# =====================================================
 
if prompt := st.chat_input("Interface with JARVIS..."):
 
    st.session_state.messages.append({"role": "user", "content": prompt})
 
    with st.chat_message("user"):
        st.markdown(prompt)
 
    with st.chat_message("assistant"):
        thinking_ph = st.empty()
        thinking_ph.markdown(BRAIN_THINKING_HTML, unsafe_allow_html=True)
        response_ph = st.empty()
        full_response = ""
 
        try:
            stream = client.chat.completions.create(
                model=st.session_state.selected_model,
                messages=[{"role": "system", "content": SYSTEM_PROMPT},
                          *st.session_state.messages[-20:]],
                temperature=st.session_state.temperature,
                max_tokens=st.session_state.max_tokens,
                stream=True
            )
            first = True
            for chunk in stream:
                delta = chunk.choices[0].delta.content if chunk.choices else None
                if delta:
                    if first:
                        thinking_ph.empty()
                        first = False
                    full_response += delta
                    response_ph.markdown(full_response + " ▌")
            response_ph.markdown(full_response)
 
        except Exception as e:
            thinking_ph.empty()
            st.error(f"⚠️ Neural error: {str(e)}")
            full_response = "Sorry, something went wrong. Please try again."
            response_ph.markdown(full_response)
 
    st.session_state.messages.append({"role": "assistant", "content": full_response})
 
# =====================================================
# FOOTER
# =====================================================
 
st.divider()
st.caption("⚡ JARVIS AI · Neural Intelligence System · Streamlit + Fireworks AI")
