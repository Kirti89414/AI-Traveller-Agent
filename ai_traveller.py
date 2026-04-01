import os
from dotenv import load_env
import streamlit as st
from langchain_groq import ChatGroq 
from langchain.messages import HumanMessage, AIMessage

load_dotenv()

# ---------------- CONFIG ----------------
st.set_page_config(page_title="AI Travel Agent", page_icon="🌍")

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.4,
    api_key = os.getenv("GROQ_API_KEY")

# ---------------- SESSION STATE ----------------
if "chat" not in st.session_state:
    st.session_state.chat = []
if "step" not in st.session_state:
    st.session_state.step = 0

if "data" not in st.session_state:
    st.session_state.data = {
        "destination": None,
        "days": None,
        "budget": None,
        "travel_type": None,
        "interests": None
    }

# ---------------- QUESTIONS FLOW ----------------
QUESTIONS = [
    "🌍 Great! First tell me **your destination city or country**.",
    "📅 How many **days** is your trip?",
    "💰 What is your **total budget** (approx)?",
    "🎒 What type of trip do you prefer? (adventure / leisure / family / honeymoon)",
    "🎯 What are your **main interests**? (history, food, nature, shopping, etc.)"
]

# ---------------- UI ----------------
st.title("🌍 AI Travel Agent")
st.caption("Step-by-step professional travel planning")

# Show chat history
for msg in st.session_state.chat:
    st.chat_message(msg["role"]).write(msg["content"])

# ---------------- INPUT ----------------
user_input = st.chat_input("Type your answer...")

if user_input:
    # show user msg
    st.chat_message("user").write(user_input)
    st.session_state.chat.append({"role": "user", "content": user_input})

    # save data step-wise
    if st.session_state.step == 0:
        st.session_state.data["destination"] = user_input
    elif st.session_state.step == 1:
        st.session_state.data["days"] = user_input
    elif st.session_state.step == 2:
        st.session_state.data["budget"] = user_input
    elif st.session_state.step == 3:
        st.session_state.data["travel_type"] = user_input
    elif st.session_state.step == 4:
        st.session_state.data["interests"] = user_input

    st.session_state.step += 1

    # ---------------- NEXT RESPONSE ----------------
    if st.session_state.step < len(QUESTIONS):
        ai_text = QUESTIONS[st.session_state.step]
    else:
        # -------- FINAL TRAVEL PLAN --------
        prompt = f"""
        You are a professional travel planner.

        User Details:
        Destination: {st.session_state.data['destination']}
        Days: {st.session_state.data['days']}
        Budget: {st.session_state.data['budget']}
        Travel Type: {st.session_state.data['travel_type']}
        Interests: {st.session_state.data['interests']}

        Create a detailed travel plan with:
        - Day-wise itinerary
        - Hotel suggestions
        - Local transport
        - Budget breakdown
        - Travel tips

        Use friendly and professional tone.
        """

        response = llm.invoke([HumanMessage(content=prompt)])
        ai_text = response.content

    # show AI msg
    st.chat_message("assistant").write(ai_text)
    st.session_state.chat.append({"role": "assistant", "content": ai_text})

# ---------------- START MESSAGE ----------------
if st.session_state.step == 0 and len(st.session_state.chat) == 0:
    welcome = "Hello! 👋 I’m your **AI Travel Agent**. Let’s plan an amazing trip together ✨"
    question = QUESTIONS[0]

    st.chat_message("assistant").write(welcome)
    st.chat_message("assistant").write(question)

    st.session_state.chat.append({"role": "assistant", "content": welcome})
    st.session_state.chat.append({"role": "assistant", "content": question})
