🚀 NUVORA - AI Resume Analyser

---

🧠 Overview

NUVORA is an AI-powered Resume Analyzer that intelligently evaluates resumes against job descriptions and provides actionable insights to improve them.

It helps candidates optimize their resumes, align with job requirements, and significantly improve their chances of getting shortlisted.

---

✨ Key Features

- 📄 Extract text from PDF resumes
- 🤖 AI-powered analysis using LLM models (Gemini / Groq)
- 🔍 Compare resumes with job descriptions
- 📊 Generate resume match score (%)
- ✅ Identify matching skills
- ⚠️ Highlight missing skills
- 📌 Provide structured improvement suggestions
- 📈 Interactive analytics dashboard with visual insights
- 🎯 Clean and responsive UI built with Streamlit

---

🛠️ Tech Stack

- Frontend/UI: Streamlit
- Backend Logic: Python
- AI Processing: Gemini / Groq APIs
- Data Handling: Pandas
- Visualization: Plotly
- File Processing: PyMuPDF, Pillow

---

⚙️ Installation & Setup

1️⃣ Install Dependencies

pip install pymupdf Pillow google-generativeai python-dotenv streamlit pandas plotly-express

---

2️⃣ Set Up API Key

Create a ".env" file and add:

GEMINI_API_KEY=your_api_key_here

(or configure Groq if you're using it)

---

3️⃣ Run the Application

streamlit run app.py

---

🧠 How It Works

1. Upload your Resume (PDF)
2. Paste the Job Description
3. Click Analyze Resume
4. Get detailed insights:
   - 📊 Resume Match Score
   - ✅ Matching Skills
   - ⚠️ Missing Skills
   - 📌 Improvement Suggestions

---

📂 Project Structure

📂 NUVORA-AI-Resume-Analyser  
 ┣ 📂 pdf_images/         # Converted resume images  
 ┣ 📜 app.py              # Streamlit UI  
 ┣ 📜 analyzer.py         # AI processing logic  
 ┣ 📜 requirements.txt    # Dependencies  
 ┣ 📜 .env.example        # API key setup  
 ┗ 📜 README.md           # Documentation  

---

💡 Use Cases

- 🎓 Students preparing for placements
- 💼 Job seekers optimizing resumes
- 🔄 Career switchers targeting new roles
- 🧑‍💻 Freelancers tailoring resumes for clients

---

🚀 Future Enhancements

- 💬 Chat-based AI assistant
- ✍️ Resume rewriting suggestions
- 📄 ATS optimization
- 🎯 Multi-role resume comparison
- 🎤 Voice-based queries

---

👨‍💻 Author

Built by Vasu Bhardwaj

---

⭐ Final Note

NUVORA is designed to bridge the gap between your resume and job expectations using AI.
Keep improving, keep applying — and let AI guide your journey 🚀
