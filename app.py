import base64
import os
from analyzer import pdf_to_jpg, process_image
import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------------
# 🔧 Streamlit Config
# -------------------------------
st.set_page_config(layout="wide", page_title="AI Resume Analyzer")

# Initialize session state
if "page" not in st.session_state:
    st.session_state.page = "main"


# -------------------------------
# 🧩 Helper Functions
# -------------------------------

# ✅ ADDED (for logo)
def get_base64_image(image_path):
    with open(image_path, "rb") as img:
        return base64.b64encode(img.read()).decode()


def show_project_title():
    # ✅ ADDED LOGO
    logo_base64 = get_base64_image("logo.jpeg")

    st.markdown(f"""
    <div style="display:flex; justify-content:center; align-items:center; margin-top:10px;">
        <img src="data:image/jpeg;base64,{logo_base64}" width="220">
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        """
        <h2 style="text-align: center; color: #4A90E2;">AI-Powered Resume Analyzer</h2>
        """,
        unsafe_allow_html=True
    )


def show_loading_screen():
    """Show full-screen loading spinner."""
    placeholder = st.empty()
    with placeholder.container():
        st.markdown(
            """
            <div style="position: fixed; top: 0; left: 0; width: 100%; height: 100%;
                        background-color: rgba(0, 0, 0, 0.8); display: flex; justify-content: center;
                        align-items: center; color: white; font-size: 24px; font-weight: bold;">
                ⏳ Analyzing your resume... Please wait.
            </div>
            """,
            unsafe_allow_html=True
        )
    return placeholder


def remove_resume():
    st.session_state.resume_uploaded = False
    st.session_state.uploaded_file = None
    st.rerun()


def save_uploaded_file(uploaded_file):
    file_path = os.path.join(os.getcwd(), uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path


# -------------------------------
# 📊 Analytics Page
# -------------------------------
def show_analytics():
    show_project_title()
    st.title("📊 Resume & Job Description Analytics")

    if "extracted_data" in st.session_state and st.session_state.extracted_data:
        extracted_data = st.session_state.extracted_data

        overall_score = extracted_data.get("overall_score", 0)
        matching_skills = extracted_data.get("keyword_matching", [])
        missing_skills = extracted_data.get("missing_keywords", [])
        suggestions = extracted_data.get("suggestions", [])

        st.subheader(f"Matching Score: {overall_score}%")
        fig = px.bar(
            x=[overall_score], y=["Resume Match"],
            orientation="h", text=[f"{overall_score}%"],
            color_discrete_sequence=[
                "#2ECC71" if overall_score >= 80 else "#F39C12" if overall_score >= 60 else "#E74C3C"
            ]
        )
        fig.update_traces(textposition="inside")
        fig.update_layout(xaxis=dict(range=[0, 100]), height=150, width=500)
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("🔍 Key Insights")
        st.write(f"✅ Your resume matches **{overall_score}%** with the job description.")
        if overall_score >= 80:
            st.success("Strong alignment with the job requirements 🎯")
        elif overall_score >= 60:
            st.warning("Partial alignment — consider improving a few areas.")
        else:
            st.error("Resume needs significant improvements to match the job description.")

        st.subheader("✅ Matching Skills")
        if matching_skills:
            st.success(", ".join(matching_skills[:5]))
            if len(matching_skills) > 5:
                with st.expander(f"View all matched skills ({len(matching_skills)})"):
                    st.write(", ".join(matching_skills))
        else:
            st.warning("No matching skills found.")

        st.subheader("⚠️ Missing Skills")
        if missing_skills:
            st.error(", ".join(missing_skills[:5]))
            if len(missing_skills) > 5:
                with st.expander(f"View all missing skills ({len(missing_skills)})"):
                    st.write(", ".join(missing_skills))
        else:
            st.success("No critical missing skills.")

        st.subheader("📌 Categorized Improvements")
        important_keys = {
            "Skills & Certifications": ["skill", "certification", "training"],
            "Experience & Work History": ["experience", "projects", "work history"],
            "Resume Formatting & Structure": ["format", "layout", "structure", "design"],
            "Education & Qualifications": ["education", "degree", "qualification"]
        }

        categorized_suggestions = {category: [] for category in important_keys.keys()}
        for suggestion in suggestions:
            for category, keywords in important_keys.items():
                if any(word in suggestion.lower() for word in keywords):
                    categorized_suggestions[category].append(f"🔹 {suggestion}")
                    break

        if any(categorized_suggestions.values()):
            for category, items in categorized_suggestions.items():
                if items:
                    with st.expander(f"{category} ({len(items)})"):
                        for item in items:
                            st.markdown(item)
        else:
            st.success("No major improvements needed. 👍")

        st.write("### 🚀 High-Priority Improvement Suggestions")
        priority_data = []
        for suggestion in suggestions:
            if "experience" in suggestion.lower():
                priority = "High"; color = "🔴"
            elif "skill" in suggestion.lower():
                priority = "Medium"; color = "🟠"
            else:
                priority = "Low"; color = "🟢"
            priority_data.append({
                "Improvement Suggestion": suggestion,
                "Priority": f"{color} {priority}"
            })

        if priority_data:
            priority_df = pd.DataFrame(priority_data)
            if "Priority" in priority_df.columns:
                priority_df = priority_df.sort_values(by="Priority", ascending=False).head(5)
            st.dataframe(priority_df, use_container_width=True)
        else:
            st.info("✅ No high-priority improvements found. Your resume looks strong!")

    else:
        st.error("No extracted data available. Please upload and analyze a resume first.")

    st.markdown("<br>", unsafe_allow_html=True)
    col_center = st.columns([1, 2, 1])[1]
    with col_center:
        if st.button("🔙 Back to Upload", use_container_width=True):
            st.session_state.page = "main"
            st.rerun()


# -------------------------------
# 🧾 Main Page
# -------------------------------
if st.session_state.page == "main":
    show_project_title()
    col1, col2 = st.columns([1, 1], gap="medium")

    with col1:
        st.subheader("Enter Job Description")
        job_description = st.text_area("Paste the job description here", height=400)

    with col2:
        if "resume_uploaded" not in st.session_state:
            st.session_state.resume_uploaded = False
            st.session_state.uploaded_file = None

        if not st.session_state.resume_uploaded:
            st.subheader("Upload Resume")
            uploaded_file = st.file_uploader("Upload your PDF Resume", type=["pdf"])
            if uploaded_file:
                file_path = save_uploaded_file(uploaded_file)
                st.session_state.resume_uploaded = True
                st.session_state.uploaded_file = uploaded_file
                st.session_state.file_path = file_path
                st.rerun()

        if st.session_state.resume_uploaded and st.session_state.uploaded_file:
            def get_pdf_base64(file_path):
                with open(file_path, "rb") as file:
                    base64_pdf = base64.b64encode(file.read()).decode("utf-8")
                return f"data:application/pdf;base64,{base64_pdf}"

            pdf_data = get_pdf_base64(st.session_state.file_path)
            st.subheader("Uploaded Resume")
            st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
            col3, col4 = st.columns([10, 1])
            with col3:
                st.markdown(
                    f'<iframe src="{pdf_data}" width="100%" height="400" style="border:none;"></iframe>',
                    unsafe_allow_html=True,
                )
            with col4:
                if st.button("❌", key="remove_resume", help="Remove Resume", use_container_width=True):
                    remove_resume()

    is_analyze_enabled = bool(job_description.strip()) and st.session_state.resume_uploaded
    st.markdown("<br>", unsafe_allow_html=True)
    col_center = st.columns([1, 2, 1])[1]
    with col_center:
        if st.button("🔍 Analyze Resume", use_container_width=True, disabled=not is_analyze_enabled):
            if is_analyze_enabled:
                loading_placeholder = show_loading_screen()
                try:
                    st.session_state.page = "analytics"
                    file_path = st.session_state.file_path
                    image_paths = pdf_to_jpg(file_path)
                    extracted_text = []

                    for img_path in image_paths:
                        result = process_image(file_path=img_path, prompt="Extract text from this image.", type="image")
                        extracted_text.append(result)

                    final_prompt = f"""
                    You are an AI-powered Resume Analyzer. Compare the extracted resume text with the job description below and provide structured insights in JSON format.

                    Job Description:
                    {job_description}

                    Extracted Text:
                    {extracted_text}

                    Output Format:
                    {{
                        "overall_score": 75,
                        "keyword_matching": ["Python", "SQL"],
                        "missing_keywords": ["AWS", "Power BI"],
                        "suggestions": ["Add experience with cloud tools", "Highlight data visualization skills"]
                    }}
                    """

                    final_result = process_image(file_path=extracted_text, prompt=final_prompt, type="text")
                    st.session_state.extracted_data = final_result

                finally:
                    loading_placeholder.empty()
                st.rerun()

elif st.session_state.page == "analytics":
    show_analytics()