import google.generativeai as genai
import streamlit as st
from pptx import Presentation
import tempfile
import os

# Configure Gemini API
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])


def analyze_slide(slide_text):
    """Get AI analysis for slide content using Gemini"""
    model = genai.GenerativeModel("models/gemini-1.5-pro")  # Recommended model
    response = model.generate_content(
        f"Using the following slide content, provide a comprehensive and detailed explanation. Summarize the main ideas, elaborate on key concepts, and highlight the information that is most critical for exam preparation. If appropriate, include bullet points or key takeaways to clearly outline the important points.Slide content:{slide_text}"
    )
    return response.text

def process_ppt(file):
    """Extract and analyze slides"""
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(file.read())
        prs = Presentation(tmp.name)
    
    results = []
    for i, slide in enumerate(prs.slides):
        text = "\n".join(
            shape.text for shape in slide.shapes 
            if shape.has_text_frame
        )
        analysis = analyze_slide(text)
        results.append((f"Slide {i+1}", text, analysis))
    
    os.unlink(tmp.name)
    return results

# Streamlit UI
st.title("AI PPT Explainer 🎓")
uploaded_file = st.file_uploader("Upload PowerPoint file", type=["ppt", "pptx"])

if uploaded_file:
    with st.spinner("Analyzing your presentation..."):
        slides = process_ppt(uploaded_file)
    
    for slide_num, content, analysis in slides:
        with st.expander(slide_num):
            st.subheader("Slide Content")
            st.write(content or "No text detected")
            
            st.subheader("AI Explanation")
            st.write(analysis)
