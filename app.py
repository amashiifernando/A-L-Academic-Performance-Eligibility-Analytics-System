import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from scipy.stats import chi2_contingency
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import os

# ==========================================
# 1. PAGE CONFIG & ENHANCED PALETTE
# ==========================================
st.set_page_config(page_title="A/L Academic Performance & Eligibility Analytics System", layout="wide")

PRIMARY_BLUE = "#002b5c"
BRAND_GOLD = "#d4af37"
COLOR_SEQ = ["#002b5c", "#d4af37", "#2e7d32", "#c62828", "#1565c0", "#ef6c00"]
HEATMAP_COLOR = ["#f8f9fa", BRAND_GOLD, PRIMARY_BLUE]

st.markdown(f"""
    <style>
    .stMetric {{ background-color: #ffffff; padding: 20px; border-radius: 12px; border-top: 5px solid {BRAND_GOLD}; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
    [data-testid="stSidebar"] {{ background-color: {PRIMARY_BLUE}; }}
    [data-testid="stSidebar"] * {{ color: white !important; }}
    h1, h2, h3 {{ color: {PRIMARY_BLUE}; font-weight: 800; }}
    .stButton>button {{ background-color: {BRAND_GOLD}; color: {PRIMARY_BLUE}; font-weight: bold; width: 100%; border-radius: 8px; border: none; }}
    .stButton>button:hover {{ background-color: #b8962e; color: white; }}
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. DATA ENGINE
# ==========================================
@st.cache_data
def get_data():
    file_path = "final_stratified_sample.csv" 
    if not os.path.exists(file_path): return None
    df = pd.read_csv(file_path)
    df.columns = df.columns.str.strip()
    mapping = {'zscore': 'z_score', 'stream': 'Stream', 'syllabus': 'Syllabus', 'gender': 'Gender', 'sex': 'Gender'}
    df = df.rename(columns={c: mapping[c.lower().replace(" ","")] for c in df.columns if c.lower().replace(" ","") in mapping})
    df = df.replace('-', np.nan)
    if 'z_score' in df.columns: df['z_score'] = pd.to_numeric(df['z_score'], errors='coerce')
    
    pass_grades = ['A', 'B', 'C', 'S']
    df['Eligible'] = df.apply(lambda r: 1 if all(str(r.get(f'sub{i}_r', 'F')) in pass_grades for i in [1,2,3]) else 0, axis=1)
    return df

df_raw = get_data()

def get_trained_model(df):
    if df is None or len(df) < 10: return None, 0, []
    g_map = {'A': 4, 'B': 3, 'C': 2, 'S': 1, 'F': 0}
    t_df = df[['sub1_r', 'sub2_r', 'sub3_r', 'Eligible']].dropna()
    for col in ['sub1_r', 'sub2_r', 'sub3_r']: t_df[col] = t_df[col].map(g_map).fillna(0)
    
    X = t_df[['sub1_r', 'sub2_r', 'sub3_r']]
    y = t_df['Eligible']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = LogisticRegression().fit(X_train, y_train)
    acc = accuracy_score(y_test, model.predict(X_test))
    importance = model.coef_[0]
    return model, acc, importance

ml_model, model_acc, weights = get_trained_model(df_raw)

# ==========================================
# 3. NAVIGATION & FILTERS
# ==========================================

st.sidebar.title("🏛️ Student Portal")
page = st.sidebar.radio("Navigation", [
    "Project & Data Explorer", 
    "Exploratory Analysis", 
    "Subject Dependency (Chi-Square)", 
    "Eligibility Model (ML)", 
    "Predict Your Eligibility"
])

df = df_raw.copy()
sel_streams = []

if page in ["Project & Data Explorer", "Exploratory Analysis"]:
    st.sidebar.divider()
    st.sidebar.subheader("🎯 Dashboard Filters")
    all_streams_list = sorted(df_raw['Stream'].unique().tolist())
    sel_streams = st.sidebar.multiselect("Filter Streams", all_streams_list, default=all_streams_list)
    
    st.sidebar.markdown("### 📖 Syllabus Type")
    if 'active_syl' not in st.session_state: 
        st.session_state.active_syl = "All"
    
    available_syl = sorted(df_raw['Syllabus'].dropna().unique().tolist())
    
    # Logic for Syllabus Buttons with "Active" state coloring
    c1, c2, c3 = st.sidebar.columns(3)
    
    # Helper function to set color
    def syl_button(label, key_val, column):
        # If this button matches the session state, use a unique key to style it differently or just logic
        is_active = st.session_state.active_syl == key_val
        button_label = f"🟢 {label}" if is_active else label
        if column.button(button_label, key=f"btn_{label}"):
            st.session_state.active_syl = key_val
            st.rerun()

    syl_button("All", "All", c1)
    if len(available_syl) > 0:
        syl_button("New", available_syl[0], c2)
    if len(available_syl) > 1:
        syl_button("Old", available_syl[1], c3)
    
    # Filter the dataframe
    df = df_raw[df_raw['Stream'].isin(sel_streams)]
    if st.session_state.active_syl != "All":
        df = df[df['Syllabus'] == st.session_state.active_syl]
    
    # Visual indicator of active filter
    st.sidebar.info(f"Filtering by: **{st.session_state.active_syl} Syllabus**")
# ==========================================
# 4. PAGES
# ==========================================

# --- PAGE 1: PROJECT & DATA EXPLORER ---
if page == "Project & Data Explorer":
    st.title("📂 Project Overview & Data Explorer")
    
    st.info("""
    ###  A/L Examination System Overview
    * **The A/L Exam:** The General Certificate of Education Advanced Level is the primary national examination in Sri Lanka used to select students for state universities.
    * **Z-Score:** A standardized value that ranks students relative to others nationwide. It corrects for differences in difficulty across various subject combinations.
    * **University Eligibility:** This is achieved by obtaining at least 3 passes (**S grade or above**) in all three main subjects in a single sitting.
    """)
    
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Candidates", f"{len(df):,}")
    c2.metric("Avg Z-Score", f"{df['z_score'].mean():.3f}")
    c3.metric("Uni Eligibility Rate", f"{(df['Eligible'].mean()*100):.1f}%")
    c4.metric("Active Streams", len(sel_streams) if sel_streams else len(df['Stream'].unique()))
    
    st.divider()
    st.subheader("📊 Statistical Scope")
    st.write("""
    This project utilizes a **stratified sample dataset** from the 2020 examination. We use this sample to perform 
    **Statistical Inference**, allowing us to identify patterns and predict future eligibility trends.
    """)

    st.subheader("Dataset Preview")
    st.dataframe(df, use_container_width=True)

# --- PAGE 2: EXPLORATORY ANALYSIS ---
elif page == "Exploratory Analysis":
    st.title("📊 Statistical Insights")
    
    st.subheader("1. Candidates by Academic Stream")
    counts = df['Stream'].value_counts().reset_index()
    counts.columns = ['Stream', 'count']
    st.plotly_chart(px.bar(counts, x='Stream', y='count', color='Stream', color_discrete_sequence=COLOR_SEQ), use_container_width=True)
    
    st.divider()
    st.subheader("2. Z-Score Performance Spread")
    st.plotly_chart(px.box(df, x="Stream", y="z_score", color="Stream", color_discrete_sequence=COLOR_SEQ), use_container_width=True)

       
    st.divider() 
    st.subheader("3. Grade Density Heatmap") 
    heat_sub = st.selectbox("Select Subject Grade to Map", ["sub1_r", "sub2_r", "sub3_r"]) 
    heat = pd.crosstab(df['Stream'], df[heat_sub]).reindex(columns=['A','B','C','S','F'], fill_value=0) 
    st.plotly_chart(px.imshow(heat, text_auto=True, color_continuous_scale=HEATMAP_COLOR), use_container_width=True)

    st.success("""
    ### 🔍 Observations & Insights
    * **Stream Performance:** The box plot shows the distribution of Z-scores. A higher median indicates a stream where students performed better relative to the national average.
    * **Z-Score Spread:** The length of the 'whiskers' shows the performance gap between the top and bottom students in each stream.
    * **Grade Density (Heatmap):** This reveals the 'Grade Profile' of each stream. For example, if the 'A' column is dark in the Science stream but light in others, it proves that 'A' grades are more frequent in Science. It helps identify 'high-scoring' vs 'low-scoring' subjects.
    """)

    st.info("""
### ⚠️ Assumptions & Limitations 
1. **Assumption:** We assume the 2020 stratified sample is representative of the entire national student body.
2. **Limitation:** Z-Scores are relative. A high Z-Score in a 'small' stream might not be directly comparable to one in a 'large' stream like Arts due to the ranking formula.
""")

# --- PAGE 3: CHI-SQUARE ---
elif page == "Subject Dependency (Chi-Square)":
    st.title("📈 Statistical Dependency Analysis")
    
    st.markdown("""
    ###  Hypothesis Testing
    * **H₀ (Null Hypothesis):** Performance in Subject A and Subject B are **independent**.
    * **H₁ (Alternative Hypothesis):** Performance in Subject A and Subject B are **dependent**.
    * **Decision Rule:** We use a significance level of **0.05**. If P-Value < 0.05, we reject H₀.
    """)
    
    sub_cols = [c for c in df_raw.columns if '_r' in c]
    v1 = st.selectbox("Select Subject A", sub_cols, index=0)
    v2 = st.selectbox("Select Subject B", sub_cols, index=1)
    
    ctab = pd.crosstab(df_raw[v1], df_raw[v2])
    chi2, p, _, _ = chi2_contingency(ctab)
    
    st.metric("P-Value", f"{p:.4e}")
    
    if p < 0.05:
        st.success(f"**Interpretation:** Since P < 0.05, we reject H₀. Grades in **{v1}** and **{v2}** are **dependent**. This suggests shared skill sets (like mathematical logic) affect both subjects.")
    else:
        st.warning(f"**Interpretation:** P > 0.05. We fail to reject H₀. Grades in **{v1}** and **{v2}** are **independent**.")
    
    st.plotly_chart(px.imshow(ctab, text_auto=True, color_continuous_scale=HEATMAP_COLOR), use_container_width=True)

    st.info("""
**⚠️ Statistical Assumptions:**
* We assume the observations are independent (one student's grade doesn't directly force another student's grade).
* We assume the sample size is large enough for the Chi-Square distribution to be valid.
""")

# --- PAGE 4: ML LOGIC ---
elif page == "Eligibility Model (ML)":
    st.title("📉 ML Logic & Weights")
    
    st.info("""
    ###  Model Selection & Feature Importance
    * **Why Classification?** We are predicting a categorical 'Yes/No' outcome (Eligible or not).
    * **Logistic Regression:** This model calculates the probability of eligibility based on the weights of different grades.
    * **Feature Importance:** This chart shows which subject 'weight' most heavily influences the AI's final decision.
    """)
    
    st.metric("Model Accuracy", f"{model_acc:.1%}")
    st.subheader("📊 Feature Importance")
    
    imp_df = pd.DataFrame({'Subject': ['Subject 1', 'Subject 2', 'Subject 3'], 'Weight': weights})
    st.plotly_chart(px.bar(imp_df, x='Weight', y='Subject', orientation='h', color='Weight', color_continuous_scale=[BRAND_GOLD, PRIMARY_BLUE]), use_container_width=True)

    st.info("""
**⚠️ ML Assumptions & Limitations:**
1. **Linearity:** Logistic Regression assumes a linear relationship between the log-odds of eligibility and the grades.
2. **Historical Bias:** This model is trained on **2020 data**. If the university intake criteria or exam difficulty changes significantly in future years, this model's accuracy may decrease.
3. **Feature Limit:** The model only uses 3 subject grades. It does not account for the 'Common General Test' or English requirements, which are also part of real-world eligibility.
""")

# --- PAGE 5: PREDICTOR ---
elif page == "Predict Your Eligibility":
    st.title("🎓 University Eligibility Predictor")
    
    st.error("""
    **⚠️ Disclaimer:** This predictor is a statistical tool based on **2020 historical data**. 
    It is **NOT** an official admission letter. Official eligibility is verified only by the UGC.
    """)
    
    g_map = {'A': 4, 'B': 3, 'C': 2, 'S': 1, 'F': 0}
    c1, c2, c3 = st.columns(3)
    g1 = c1.selectbox("Subject 1 Grade", ['A','B','C','S','F'], index=0)
    g2 = c2.selectbox("Subject 2 Grade", ['A','B','C','S','F'], index=0)
    g3 = c3.selectbox("Subject 3 Grade", ['A','B','C','S','F'], index=0)
    
    if st.button("Run Prediction"):
        grades = [g1, g2, g3]
        has_failed = 'F' in grades
        inputs = np.array([[g_map[g1], g_map[g2], g_map[g3]]])
        prob = ml_model.predict_proba(inputs)[0][1]
        
        st.divider()
        if has_failed:
            st.error("Outcome: INELIGIBLE")
            st.warning("Reasoning: Sri Lankan university entry rules require a minimum of an 'S' pass in all 3 subjects. An 'F' results in automatic ineligibility.")
        else:
            if ml_model.predict(inputs)[0] == 1:
                st.balloons()
                st.success(f"Outcome: ELIGIBLE")
            else:
                st.error(f"Outcome: INELIGIBLE")
            
            st.metric("AI Confidence Level", f"{prob:.1%}")
            st.progress(prob)