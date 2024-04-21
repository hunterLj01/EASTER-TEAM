import streamlit as st
from datetime import datetime, timedelta, date
import pandas as pd
import numpy as np
import time
import torch
from langchain_community.llms import Ollama

st.set_page_config(page_title="Train", page_icon="💪")

# SIDEBAR -----------------------

## MENU
#st.sidebar.page_link("app.py", label="Train", icon="💪")
#st.sidebar.page_link("pages/dashboard.py", label="Leaderboard", icon="🥇")

## EXAM COUNTDOWN
def days_until_exam(exam_date):
    today = datetime.now().date()
    days_left = (exam_date - today).days
    return days_left

st.sidebar.title("💯 Tell us more about you ")
exam_date = st.sidebar.date_input('⏰ Date of your exam')
days_left = days_until_exam(exam_date)
if days_left == 0:
  days_left = days_until_exam(date.fromisoformat('2024-04-29'))
st.sidebar.write('➡️➡️➡️', days_left, 'days until your exam')
# Simulating progress
progress_bar = st.sidebar.progress(34, text="Topics covered 34%")

# Sidebar line chart
np.random.seed(42)  # Setting random seed for reproducibility
values = np.arange(50, 90, 4) + np.random.randint(-10, 30, 10)
st.sidebar.write("🔅 Progress over time 🧗 ...")
chart_data = pd.DataFrame(values)
st.sidebar.line_chart(chart_data, height=200)

# Topics you have mastered
st.sidebar.write("🔄🔄🔄 Active recall queue 🏃")
df_active_recall = pd.DataFrame({
    'Topic': ['LU factorization', 'QR factorization', 'SVD'],
    'Review in': ['In an hour', 'In two days', 'In a week']
}, index=pd.Index(['🚨', '🌄', '🛫'], name='Rank'))
st.sidebar.table(df_active_recall)


## UPLOAD PDFs & VIDEOs
st.sidebar.title("📄🎥 Load prep material ")
st.sidebar.file_uploader(label='Allowed formats: .mp3, .mp4, .pdf')

## CLASS CODE
st.sidebar.title("🤝 Join your class ")
class_code = st.sidebar.text_input("Enter the class code:")
if class_code:
##ANALYTICS
  st.sidebar.title("🗽 Class Leaderboard")
  df_leaderboard = pd.DataFrame({
      'Name': ['Alice', 'Bob', 'Charlie'],
      'Score': ['100%', '90%', '85%']
  }, index=pd.Index(['🥇', '🥈', '🥉'], name='Rank'))
  st.sidebar.table(df_leaderboard)
else:
  st.sidebar.write("Enter a class code to see the leaderboard 😉")
# ----------------------------------------------------------------
st.write('# 🏋️‍♀️ SocratAI')

#st.header("Let's see what you know 🐱")

# CHATBOT -----------------------
if "messages" not in st.session_state:
  st.session_state["messages"] = [{
    "role": "assistant",
    "content": "🌟 Welcome to the ultimate countdown training 🥊 🌟"
  }]

### MESSAGE HISTORY
for msg in st.session_state.messages:
  if msg["role"]=="user":
    st.chat_message(msg["role"], avatar = "🏋️").write(msg["content"])
  else:  
    st.chat_message(msg["role"], avatar = "🐱").write(msg["content"])

### GENERATOR FOR STREAMING TOKENS
def generate_response():
  return " Who discovered the LU factorization method?"

if prompt := st.chat_input():
  st.session_state.messages.append({"role":"user", "content":prompt})
  st.chat_message("user", avatar = "🏋️").write(prompt)
  st.session_state["full_message"] = ""
  if "shorts" in prompt:
    st.chat_message("assistant", avatar = "🐱").write("See, this 30 sec part from class explains it all 😉")
    st.video("shorts1.mp4")
    st.session_state.messages.append({"role":"assistant","content":"See, this 30 sec part from class explains it all 😉    --- to watch again type shorts"})
  elif "test me" in prompt:
    st.chat_message("assistant", avatar = "🐱").write("Why is LU factorization useful?")
    st.session_state.messages.append({"role":"assistant","content":"Why is LU factorization useful?"})
  elif "i don't understand what my slides images refer to "
    st.chat_message("assistant", avatar = "🐱").write("It's a dancing cartoon tho")
    st.image("img1.jpeg")
    st.session_state.messages.append({"role":"assistant","content":"It's a dancing cartoon tho"})
  else:
    st.chat_message("assistant", avatar = "🐱").write_stream(generate_response())
    st.session_state.messages.append({"role":"assistant","content":st.session_state["full_message"]})

