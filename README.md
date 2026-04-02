---

# **AI Resume Analyzer - Build Your Own AI-Powered Job Application Assistant! 🚀**  

## **Overview**  
This project is an **AI-powered Resume Matcher** that analyzes resumes against job descriptions and provides actionable insights to improve them. Whether you're applying for jobs or optimizing your resume, this tool helps you **boost your chances of getting hired!**  

## **Features**  
✅ Extract text from **PDF resumes**  
✅ Process resumes using **Google Gemini AI**  
✅ Compare resumes with job descriptions  
✅ Generate **AI-powered resume scores & improvement suggestions**  
✅ Build a user-friendly interface with **Streamlit**  

## **Installation & Setup**  

### ** Install Required Libraries**  
```bash
pip install pymupdf Pillow google-generativeai python-dotenv streamlit pandas plotly-express
```

### ** Set Up API Keys**  
- Get an API key from **Google Gemini AI**  
- Create a `.env` file and add:  
  ```
  GEMINI_API_KEY=your_api_key_here
  ```

### ** Run the Application**  
```bash
streamlit run app.py
```

---

## **How It Works**  

1️⃣ **Upload a Resume (PDF Format)**  
2️⃣ **Paste a Job Description** into the text area  
3️⃣ Click **Analyze Resume**  
4️⃣ Get AI-generated insights, including:  
   - **Resume Score**  
   - **Matching Skills**  
   - **Unmatched Skills**  
   - **Improvement Suggestions**  

---

## **Project Structure**  
```
📂 AI-Resume-Matcher  
 ┣ 📂 pdf_images/         # Stores converted resume images  
 ┣ 📜 app.py              # Main Streamlit UI  
 ┣ 📜 analyzer.py         # AI processing logic  
 ┣ 📜 requirements.txt    # Python dependencies  
 ┣ 📜 .env.example        # API key setup guide  
 ┗ 📜 README.md           # Project documentation  
```

