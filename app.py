import streamlit as st
import joblib
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
import os
import datetime

# 1. Page Configuration & Futuristic Cyber Theme
st.set_page_config(
    page_title="NEURAL-SHIELD // Enterprise Job Forensics", 
    page_icon="🛡️", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Dark Sci-Fi Cyberpunk Theme
st.markdown("""
    <style>
    .stApp { background-color: #0b0f19; color: #e2e8f0; }
    h1, h2, h3 { color: #38bdf8 !important; font-family: 'Courier New', monospace; letter-spacing: 1px; }
    .stTextArea textarea { background-color: #1e293b !important; color: #38bdf8 !important; border: 1px solid #334155 !important; border-radius: 8px; }
    .stTextInput input { background-color: #1e293b !important; color: #38bdf8 !important; border: 1px solid #334155 !important; }
    .stButton>button {
        background: linear-gradient(90deg, #0284c7 0%, #2563eb 100%);
        color: white; border: none; font-weight: bold; border-radius: 6px; padding: 0.6rem 1.2rem;
        box-shadow: 0 0 10px rgba(37, 99, 235, 0.4); transition: 0.3s ease;
    }
    .stButton>button:hover { box-shadow: 0 0 20px rgba(56, 189, 248, 0.8); }
    </style>
""", unsafe_allow_html=True)

# 2. Model Loader / Auto-Trainer
@st.cache_resource
def load_ai_model():
    m_file = 'job_scam_model.pkl'
    v_file = 'tfidf_vectorizer.pkl'
    
    if not os.path.exists(m_file) or not os.path.exists(v_file):
        df = pd.DataFrame({
            'description': [
                "Software engineer position with python and sql skills. Competitive salary and benefits package.",
                "URGENT work from home data entry. Earn $5000 weekly instantly. No experience needed. Send telegram @recruiter.",
                "Marketing manager position. Office located in downtown. Official corporate portal application.",
                "Make money fast processing data. Must pay refundable training fee via crypto or gift card before start."
            ],
            'telecommuting': [0, 1, 0, 1],
            'has_company_logo': [1, 0, 1, 0],
            'has_questions': [1, 0, 1, 0],
            'fraudulent': [0, 1, 0, 1]
        })
        vec = TfidfVectorizer(max_features=5000, stop_words='english')
        X_txt = vec.fit_transform(df['description']).toarray()
        X_meta = df[['telecommuting', 'has_company_logo', 'has_questions']].values
        X = np.hstack((X_txt, X_meta))
        
        clf = RandomForestClassifier(n_estimators=100, random_state=42)
        clf.fit(X, df['fraudulent'])
        
        joblib.dump(clf, m_file)
        joblib.dump(vec, v_file)
        
    return joblib.load(m_file), joblib.load(v_file)

model, vectorizer = load_ai_model()

# 3. Sidebar Navigation & Features
st.sidebar.markdown("### 🎛️ ENTERPRISE NAVIGATION")
app_mode = st.sidebar.radio("Select Module:", ["🛡️ Threat Forensics Engine", "🧠 Scam Awareness Academy (Quiz)"])

if app_mode == "🛡️ Threat Forensics Engine":
    st.markdown("### 🛡️ NEURAL-SHIELD // AI JOB FORENSICS & THREAT INTEL")
    st.markdown("Advanced Machine Learning pipeline designed to intercept employment fraud, phishing hooks, and deceptive remote job offers.")
    st.markdown("---")

    # Sidebar Controls
    st.sidebar.markdown("### ⚙️ METADATA TELEMETRY")
    telecommuting = st.sidebar.selectbox("🌐 Location Vector", [0, 1], format_func=lambda x: "Remote / Work From Home" if x == 1 else "On-Site / Office")
    has_logo = st.sidebar.selectbox("🏢 Corporate Identity Vector", [1, 0], format_func=lambda x: "Verified Company Logo Present" if x == 1 else "No Logo / Unverified Brand")
    has_questions = st.sidebar.selectbox("📋 Screening Vector", [1, 0], format_func=lambda x: "Formal Screening / Questionnaire" if x == 1 else "Direct Hire / No Questions")
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🌐 DOMAIN REPUTATION CHECK")
    company_url = st.sidebar.text_input("Enter Employer Domain/URL (optional)", placeholder="e.g., google.com or hr-secure-jobs.xyz")

    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🚀 QUICK SAMPLE LOADER")
    sample_choice = st.sidebar.selectbox("Load Test Profile:", ["Select...", "Simulated Scam Post", "Simulated Legitimate Post"])

    default_text = ""
    if sample_choice == "Simulated Scam Post":
        default_text = "URGENT WORK FROM HOME OPPORTUNITY!! Data entry clerk needed immediately. Earn $5000 weekly instantly. No experience needed. To secure your equipment kit, you must pay a fully refundable training fee via crypto. Contact our hiring manager on Telegram @scamrecruiter right now."
    elif sample_choice == "Simulated Legitimate Post":
        default_text = "We are seeking a full-time Software Engineer with 3+ years experience in Python, SQL, and REST APIs. Competitive salary, healthcare benefits, and 401(k) matching included. Please apply through our official corporate careers portal."

    st.markdown("#### 📥 Input Job Description Text Stream")
    job_text = st.text_area("Paste raw text payload below:", value=default_text, height=180, placeholder="Paste job offer context here...")

    if st.button("⚡ EXECUTE ADVANCED SCAN", use_container_width=True):
        if not job_text.strip():
            st.warning("⚠️ Error: Data stream empty. Input target description.")
        else:
            with st.spinner("Decoding language structure, threat markers & telemetry..."):
                txt_vec = vectorizer.transform([job_text]).toarray()
                meta = np.array([[telecommuting, has_logo, has_questions]])
                features = np.hstack((txt_vec, meta))
                
                pred = model.predict(features)[0]
                prob = model.predict_proba(features)[0][1]
                
                st.markdown("---")
                st.markdown("### 📊 ENTERPRISE FORENSIC INTELLIGENCE REPORT")
                
                res_col1, res_col2 = st.columns(2)
                
                with res_col1:
                    if pred == 1:
                        st.error("### THREAT STATUS: 🚨 FRAUDULENT DETECTED")
                        st.metric(label="Malicious Risk Probability", value=f"{prob * 100:.2f}%", delta="CRITICAL ALERT", delta_color="inverse")
                    else:
                        st.success("### THREAT STATUS: ✅ VERIFIED SECURE")
                        st.metric(label="Malicious Risk Probability", value=f"{prob * 100:.2f}%", delta="SAFE", delta_color="normal")
                
                with res_col2:
                    st.markdown("#### 🔬 Diagnostic Vectors:")
                    
                    # Domain Check Simulation Heuristic
                    if company_url:
                        if any(ext in company_url.lower() for ext in ['.xyz', '.top', 'secure-hr', 'telegram', 'whatsapp']):
                            st.error(f"🔴 **Domain Risk Alert:** `{company_url}` matches known suspicious naming conventions or TLDs.")
                        else:
                            st.success(f"🟢 **Domain Check:** `{company_url}` appears standard.")

                    risk_keywords = ['telegram', 'whatsapp', 'fee', 'crypto', 'urgent', 'gift card', 'instant', 'no experience']
                    detected_flags = [kw for kw in risk_keywords if kw in job_text.lower()]
                    
                    if detected_flags:
                        st.warning(f"⚠️ **Social Engineering Hooks Flagged:** `{', '.join(detected_flags)}`")
                    else:
                        st.info("✅ **No primary malicious trigger keywords discovered.**")
                    
                    if has_logo == 0:
                        st.markdown("- 🔴 **Anomalous Branding:** Missing verified visual identifier.")

                # Downloadable Report Feature
                report_content = f"""NEURAL-SHIELD FORENSIC REPORT
Timestamp: {datetime.datetime.now()}
Threat Prediction: {'FRAUDULENT / SCAM' if pred == 1 else 'SECURE / LEGITIMATE'}
Risk Probability: {prob * 100:.2f}%
Domain Checked: {company_url if company_url else 'N/A'}
Flagged Keywords: {', '.join(detected_flags) if detected_flags else 'None'}
"""
                st.download_button(
                    label="📥 Download Official Threat Report (TXT)",
                    data=report_content,
                    file_name="neural_shield_report.txt",
                    mime="text/plain"
                )

elif app_mode == "🧠 Scam Awareness Academy (Quiz)":
    st.markdown("### 🧠 Scam Awareness Academy")
    st.markdown("Test your ability to spot corporate phishing and AI employment scams before falling victim.")
    st.markdown("---")
    
    question = st.radio(
        "**Quiz Question 1:** A recruiter reaches out on WhatsApp offering a $4,000/week job, but asks you to purchase an initial software equipment kit using cryptocurrency. What should you do?",
        (
            "A) Pay immediately to secure the high-paying job.",
            "B) Block and report them—this is a classic employment scam pattern.",
            "C) Ask if you can pay via credit card instead."
        )
    )
    
    if st.button("Submit Answer"):
        if "Block and report" in question:
            st.success("🎉 **Correct!** Legitimate companies never ask candidates to buy equipment upfront via cryptocurrency or gift cards.")
            st.balloons()
        else:
            st.error("❌ **Incorrect!** This is a textbook financial scam. Real employers provide company hardware directly without requiring out-of-pocket crypto payments.")

st.markdown("---")
st.markdown("<p style='text-align: center; color: #64748b;'>NEURAL-SHIELD Cyber-Forensics Engine • Enterprise Project Demo Edition</p>", unsafe_allow_html=True)