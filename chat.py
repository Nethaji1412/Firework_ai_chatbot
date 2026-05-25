import streamlit as st
from openai import OpenAI

# =====================================================
# CONFIG
# =====================================================

API_KEY = "fw_TUbfVQ2rJ6sJpuWPptaHoC"
BASE_URL = "https://api.fireworks.ai/inference/v1"

client = OpenAI(
    api_key=API_KEY,
    base_url=BASE_URL
)

# =====================================================
# AUTO MODEL DETECTION
# =====================================================

@st.cache_data(show_spinner=True)
def get_working_model():
    """
    Fetch available models and return first usable one.
    """
    try:
        models = client.models.list()

        # Priority keywords (best models first)
        priority_keywords = [
            "llama",
            "deepseek",
            "mixtral",
            "firefunction",
            "qwen"
        ]

        model_ids = [m.id for m in models.data]

        # Try priority match first
        for keyword in priority_keywords:
            for m in model_ids:
                if keyword in m.lower():
                    return m

        # fallback: first model
        return model_ids[0]

    except Exception as e:
        return None


MODEL_NAME = get_working_model()

# =====================================================
# STREAMLIT UI
# =====================================================

st.set_page_config(page_title="JARVIS", page_icon="⁕", layout="wide")

st.title("JARVIS")

if MODEL_NAME:
    st.success(f"Using model: {MODEL_NAME}")
else:
    st.error("No models found. Check API key or account access.")
    st.stop()

# =====================================================
# SESSION STATE
# =====================================================

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": """
You are JARVIS, a highly intelligent assistant.
Respond concisely, formally, assistively and firendly.
Be precise, avoid unnecessary text, and prioritize usefulness.
"""}
    ]

# =====================================================
# CHAT HISTORY
# =====================================================

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# =====================================================
# INPUT
# =====================================================

prompt = st.chat_input("Type your message...")

if prompt:

    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""

        try:
            stream = client.chat.completions.create(
                model=MODEL_NAME,
                messages=st.session_state.messages,
                temperature=0.7,
                max_tokens=1024,
                stream=True
            )

            for chunk in stream:
                if chunk.choices and chunk.choices[0].delta.content:
                    full_response += chunk.choices[0].delta.content
                    placeholder.markdown(full_response + "▌")

            placeholder.markdown(full_response)

        except Exception as e:
            st.error(f"Model error: {str(e)}")

    st.session_state.messages.append(
        {"role": "assistant", "content": full_response}
    )

# =====================================================
# CLEAR CHAT
# =====================================================

if st.button("🗑 Clear Chat"):
    st.session_state.messages = [
        {"role": "assistant", "content": "Chat cleared ✅"}
    ]
    st.rerun()


#     Streamlit (UI)
#    ↓
# OpenAI SDK (translator)
#    ↓
# Base URL (Fireworks server)
#    ↓
# API Key (access pass)
#    ↓
# Model (AI brain)
#    ↓
# Response streamed back
