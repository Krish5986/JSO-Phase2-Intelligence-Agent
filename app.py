import streamlit as st
from google import genai
import os
import random
import pandas as pd
import matplotlib.pyplot as plt
import json
from dotenv import load_dotenv
from PyPDF2 import PdfReader
import re

# -----------------------------
# 1. API SETUP
# -----------------------------
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    st.error("API key not found. Please check your .env file.")
    st.stop()

client = genai.Client(api_key=api_key)
MODEL_NAME = "gemini-2.5-flash"

# -----------------------------
# 2. PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="JSO Platform Intelligence", layout="wide")
st.title("JSO Phase-2: Platform Intelligence Agent")
st.subheader("Super Admin Insights Dashboard")

# -----------------------------
# 3. SESSION STATE
# -----------------------------
if "resume_data" not in st.session_state:
    st.session_state.resume_data = []

if "ai_report" not in st.session_state:
    st.session_state.ai_report = None

# -----------------------------
# 4. HELPER FUNCTIONS
# -----------------------------
def extract_text_from_pdf(file):
    try:
        reader = PdfReader(file)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
        return text
    except Exception as e:
        return f"Error reading PDF: {e}"

def render_chart(chart_type, data, metric):
    metric_map = {
        "Logins": "logins",
        "Applications": "applications",
        "Readiness Score": "score"
    }
    col = metric_map.get(metric, "logins")

    df = pd.DataFrame({
        "Candidate": [d["name"] for d in data],
        "Value": [d[col] for d in data]
    })

    if chart_type == "Pie Chart":
        fig, ax = plt.subplots(figsize=(6, 6))
        fig.patch.set_facecolor('none')
        df.set_index("Candidate")["Value"].plot.pie(autopct="%1.1f%%", startangle=90, ax=ax)
        ax.set_ylabel("")
        st.pyplot(fig)
    else:
        st.bar_chart(df.set_index("Candidate")["Value"])

# -----------------------------
# 5. RESUME UPLOAD
# -----------------------------
st.info("👋 **Welcome Admin.** Upload resumes to generate Platform Intelligence.")
uploaded_files = st.file_uploader("📂 Drop Resumes Here", type="pdf", accept_multiple_files=True)

if uploaded_files:
    new_data = []
    existing_names = [d["name"] for d in st.session_state.resume_data]

    for file in uploaded_files:
        if file.name not in existing_names:
            text = extract_text_from_pdf(file)
            new_data.append({
                "name": file.name,
                "content": text,
                "logins": random.randint(5, 30),
                "applications": random.randint(1, 15),
                "score": random.randint(65, 95)
            })
            
    if new_data:
        st.session_state.resume_data.extend(new_data)
        st.success(f"{len(new_data)} new resumes processed.")

# -----------------------------
# 6. METRICS DASHBOARD
# -----------------------------
if st.session_state.resume_data:
    data = st.session_state.resume_data
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Candidates", len(data))
    c2.metric("Total Applications", sum(d["applications"] for d in data))
    c3.metric("Avg Readiness", round(sum(d["score"] for d in data) / len(data), 1))

    # -----------------------------
    # 7. RUN DYNAMIC AI ANALYSIS
    # -----------------------------
    if st.button("🚀 Run Platform Intelligence Agent"):
        with st.spinner("Agent is analyzing resumes and extracting structured scores..."):
            context = ""
            for d in data:
                context += f"\nCandidate: {d['name']}\n{d['content'][:2500]}\n"
            
            prompt = f"""
            Analyze these resumes for JSO Phase-2.

            1) USER SUCCESS RATES
            Format this EXACTLY as a markdown table with ALL rows filled:
            | Name | Core Skills | Readiness Score |
            |------|-------------|-----------------|
            | filename.pdf | skill1, skill2 | 85 |
            (One row per candidate, no empty rows, no skipping)

            2) JOB MARKET TRENDS (Gaps & Demand)
            3) STRATEGY SUGGESTIONS (3 ways to improve outcomes)

            CRITICAL INSTRUCTION: At the very end of your response, you MUST type exactly "===JSON===" followed by a valid JSON array containing the Readiness Scores you calculated.
            Example Format:
            ===JSON===
            [ {{"name": "resume1.pdf", "score": 85}}, {{"name": "resume2.pdf", "score": 92}} ]

            DATA: {context}
            """
            
            try:
                response = client.models.generate_content(
                    model=MODEL_NAME,
                    contents=prompt,
                    config={"temperature": 0.0}
                )
                output_text = response.text
                
                if "===JSON===" in output_text:
                    parts = output_text.split("===JSON===")
                    st.session_state.ai_report = parts[0].strip()
                    
                    json_str = parts[1].strip().strip("```json").strip("```").strip()
                    
                    try:
                        ai_scores = json.loads(json_str)
                        for candidate in st.session_state.resume_data:
                            for ai_data in ai_scores:
                                if candidate["name"] == ai_data.get("name"):
                                    candidate["score"] = int(ai_data.get("score", candidate["score"]))
                    except json.JSONDecodeError as e:
                        st.warning(f"⚠️ Could not parse AI scores. Dashboard will use placeholder values. ({e})")
                else:
                    st.session_state.ai_report = output_text
                
                st.rerun()

            except Exception as e:
                err = str(e).lower()
                if "quota" in err or "429" in err or "resource exhausted" in err:
                    st.error("🚫 API Quota Exhausted. Please wait a moment and try again.")
                elif "api key" in err or "401" in err or "403" in err:
                    st.error("🔑 Invalid or missing API key. Please check your `.env` file.")
                elif "timeout" in err or "deadline" in err:
                    st.error("⏱️ Request timed out. Please try again.")
                elif "network" in err or "connection" in err:
                    st.error("🌐 Network/connection error. Check your internet and try again.")
                else:
                    st.error(f"❌ Unexpected error: {e}")

# -----------------------------
# 8. RESULTS DISPLAY
# -----------------------------
if st.session_state.ai_report:
    st.divider()
    st.header("📋 Admin Intelligence Report")
    st.markdown(st.session_state.ai_report)
    
    st.divider()
    st.subheader("📊 Engagement Analytics")
    col_a, col_b = st.columns(2)
    
    with col_a:
        m = st.selectbox("Select Metric", ["Logins", "Applications", "Readiness Score"])
    with col_b:
        c = st.selectbox("Chart Type", ["Bar Chart", "Pie Chart"])
    
    render_chart(c, st.session_state.resume_data, m)
