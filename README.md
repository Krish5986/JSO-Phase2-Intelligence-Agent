# JSO-Phase2-Intelligence-Agent
An Agentic AI dashboard built with Streamlit and Gemini 2.5 Flash that processes candidate resumes, extracts structured readiness scores via JSON, and visualizes platform engagement for Admins.
That is very smart thinking. 

[image (2).png](https://github.com/Krish5986/JSO-Phase2-Intelligence-Agent/blob/main/image%20(2).png?raw=true)

## 🧠 Project Overview
The Platform Intelligence Agent moves beyond standard chat interfaces by utilizing **Agentic Data Extraction**. It reads unstructured PDF resumes, processes them through a Large Language Model (LLM), and outputs structured JSON data. This data is then dynamically mapped to an interactive Business Intelligence (BI) dashboard.

## ✨ Key Features
* **Multi-Resume Processing:** Upload multiple candidate PDFs simultaneously using `PyPDF2`.
* **Agentic JSON Extraction:** Prompts Gemini 2.5 Flash to grade resumes and strictly output structured JSON arrays, bridging the gap between natural language reasoning and data visualization.
* **Dynamic Analytics Engine:** Uses `Pandas` and `Matplotlib` to render real-time Pie and Bar charts based on the AI's real-time scoring.
* **Stateful Architecture:** Utilizes Streamlit's `session_state` to prevent redundant API calls, mitigate "429 Quota Exhausted" errors, and ensure a smooth, crash-free user experience.
* **Deterministic AI:** Model temperature is set to `0.0` to ensure auditable, fair, and consistent candidate evaluations (addressing key ethical governance pillars).

## 🛠️ Tech Stack
* **Frontend/UI:** Streamlit
* **AI/LLM:** Google Gemini 2.5 Flash (`google-generativeai`)
* **Data Processing:** Pandas, PyPDF2
* **Visualization:** Matplotlib

## 💻 Local Setup & Installation

**1. Clone the repository**
```bash
git clone [https://github.com/Krish5986/JSO-Phase2-Intelligence-Agent.git](https://github.com/Krish5986/JSO-Phase2-Intelligence-Agent.git)
cd JSO-Phase2-Intelligence-Agent

```

**2. Install Dependencies**

```bash
pip install -r requirements.txt

```

**3. Configure Environment Variables**
Create a `.env` file in the root directory and add your Google Gemini API key:

```env
GOOGLE_API_KEY="your_api_key_here"

```

**4. Run the Application**

```bash
streamlit run app.py

```

## 🤝 Note to Reviewers

This project demonstrates the ability to orchestrate multi-step AI pipelines, handle API rate limits gracefully, and build user-centric data tools.

```

***


```
