# 🎓 A/L Academic Performance & Eligibility Analytics System

## 📌 Project Overview

The **A/L Academic Performance & Eligibility Analytics System** is an interactive data analytics and machine learning application developed using Streamlit.

The system analyzes Sri Lankan G.C.E. Advanced Level examination data and provides insights into student performance, academic stream trends, subject dependencies and university eligibility prediction.

This project combines:

* Data Preprocessing
* Exploratory Data Analysis (EDA)
* Statistical Hypothesis Testing
* Machine Learning
* Interactive Dashboard Development

The application is built using a stratified sample of the 2020 A/L examination dataset.

---

## 🎯 Objectives

* Analyze academic performance patterns across streams.
* Visualize Z-score distributions and grade trends.
* Identify statistical relationships between subjects.
* Predict university eligibility using Machine Learning.
* Provide an interactive decision-support tool for educational analytics.

---

## ⚙️ Technologies Used

### Programming Language

* Python

### Libraries

* Streamlit
* Pandas
* NumPy
* Plotly
* Scikit-Learn
* SciPy

### Statistical Techniques

* Descriptive Statistics
* Chi-Square Test of Independence
* Logistic Regression Classification

### Machine Learning

* Logistic Regression
* Train-Test Split
* Accuracy Evaluation

---

## 📊 Key Features

### 📂 Project & Data Explorer

* Overview of the Sri Lankan A/L examination system
* Key performance indicators
* Dataset preview
* Stream and syllabus filtering

### 📈 Exploratory Analysis

* Candidate distribution by academic stream
* Z-score performance comparison
* Interactive grade density heatmap
* Dynamic filtering capabilities

### 📉 Subject Dependency Analysis

* Chi-Square Test of Independence
* Automated hypothesis testing
* P-value interpretation
* Subject relationship heatmap

### 🤖 Eligibility Model

* Logistic Regression classification model
* Feature importance visualization
* Model accuracy evaluation

### 🎓 Smart Eligibility Predictor

A hybrid prediction system combining:

#### Rule-Based Logic

If a student receives an **F grade** in any subject, the system automatically classifies the student as **Ineligible** according to official university admission regulations.

#### Machine Learning Prediction

If all subjects have at least an **S pass**, the Logistic Regression model predicts eligibility probability using historical examination patterns.

This approach ensures predictions remain both statistically meaningful and aligned with real-world admission rules.

---

## 📄 Individual Contribution

This application extends the statistical analyses performed in the group project by transforming them into a fully interactive educational analytics platform.

### Contributions

* Implemented Logistic Regression as a real-time eligibility predictor.
* Developed an interactive Chi-Square testing module.
* Designed and implemented a Hybrid Eligibility Prediction Engine.
* Created dynamic filters and interactive visualizations.
* Integrated machine learning outputs with official university eligibility rules.
* Developed the Streamlit user interface and dashboard workflow.

Detailed contribution report:

📄 **Individual_Contribution_Report.pdf**

---

## 🎥 Video Demonstration

Watch the complete system demonstration here:

🔗 **[Insert Video Link Here]**

---

## 📊 Dataset

The project uses a stratified sample dataset derived from the 2020 Sri Lankan Advanced Level examination results.

The dataset is included solely for educational and analytical purposes.

---

## 🚀 How to Run the Project

### Clone Repository

```bash
git clone https://github.com/yourusername/A-L-Academic-Performance-Eligibility-Analytics-System.git
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Application

```bash
streamlit run app.py
```

---

## ⚠️ Disclaimer

This system is intended for educational and analytical purposes only.

Eligibility predictions are based on historical 2020 examination data and should not be interpreted as official university admission decisions.

Official eligibility is determined by the relevant Sri Lankan higher education authorities.

---

## 👩‍💻 Author

**Amashi Fernando**

Final-Year Applied Statistics Undergraduate
University of Colombo

Sri Lanka
