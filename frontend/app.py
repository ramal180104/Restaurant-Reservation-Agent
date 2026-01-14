import streamlit as st
import requests

# Backend endpoint
BACKEND_URL = "http://localhost:8001/chat"

# Page config
st.set_page_config(
    page_title="GoodFoods Reservation Assistant",
    page_icon="🍽️",
    layout="centered"
)

# App header
st.title("🍽️ GoodFoods Reservation Assistant")
st.caption("Discover GoodFoods locations, get recommendations, and book tables easily.")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# 🔥 INITIALIZE CONTEXT (CRITICAL)
if "context" not in st.session_state:
    st.session_state.context = {}

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
user_input = st.chat_input("Ask me to find or book a GoodFoods location...")

if user_input:
    # Add user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    # Call backend
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = requests.post(
                    BACKEND_URL,
                    json={
                        "messages": st.session_state.messages,
                        "context": st.session_state.context  # ✅ SEND CONTEXT
                    },
                    timeout=60
                )

                if response.status_code == 200:
                    data = response.json()

                    # ✅ UPDATE CONTEXT FROM BACKEND
                    st.session_state.context = data.get("context", {})

                    assistant_reply = data.get("content", "⚠️ No response")

                else:
                    assistant_reply = (
                        f"❌ Backend error {response.status_code}: "
                        f"{response.text}"
                    )

            except requests.exceptions.Timeout:
                assistant_reply = (
                    "❌ Backend took too long to respond. "
                    "Please try again."
                )

            except Exception as e:
                assistant_reply = f"❌ Backend error: {e}"

        st.markdown(assistant_reply)

    # Save assistant response
    st.session_state.messages.append({
        "role": "assistant",
        "content": assistant_reply
    })
