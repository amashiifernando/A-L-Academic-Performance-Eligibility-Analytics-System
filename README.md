# 🎓 A/L Academic Performance & Eligibility Analytics System

An interactive Streamlit-based educational analytics dashboard developed as an individual extension of the **Student Performance Analysis** group project.

This application transforms statistical analyses into a real-time decision-support system for exploring academic performance patterns and predicting university eligibility using historical 2020 A/L examination data.

---

## 📌 About This Project

The original group project focused on statistical analysis of factors associated with university eligibility.

This individual work extends that analysis by developing a fully interactive web application that allows users to:

* Explore examination data dynamically
* Perform statistical hypothesis testing
* Visualize academic performance patterns
* Predict university eligibility using Machine Learning
* Apply real-world eligibility rules through a hybrid prediction system

---

## 🚀 Individual Contributions

### 📊 Interactive Analytics Dashboard

* Developed using Streamlit and Plotly.
* Added dynamic filtering by academic stream and syllabus type.
* Designed interactive visualizations for data exploration.

### 📈 Chi-Square Testing Module

* Converted manual Chi-Square analysis into an interactive statistical tool.
* Allows users to select subject pairs and perform hypothesis testing automatically.
* Displays p-values, interpretations, and contingency heatmaps.

### 🤖 Logistic Regression Integration

* Implemented a Logistic Regression classification model for eligibility prediction.
* Applied train-test split methodology.
* Evaluated model performance using prediction accuracy.
* Visualized feature importance of subject grades.

### 🎯 Smart-Rule Hybrid Eligibility Predictor

One of the key enhancements of this application is the Hybrid Eligibility Prediction Engine.

#### Rule-Based Validation

* Automatically checks whether a student has received an **F grade**.
* If an F grade is detected, the system immediately returns an **Ineligible** result.

#### Machine Learning Prediction

* If all subjects meet the minimum pass requirement, the Logistic Regression model calculates the probability of eligibility.
* Combines official admission rules with machine learning predictions to produce realistic results.

---

## 🎥 Demonstration Video

Watch the complete system demonstration:

🔗 **[Insert Video Link Here]**

---

## 📄 Individual Contribution Report

The detailed report describing the implemented enhancements and technical contributions is available in:

📄 **Individual_Contribution_Report.pdf**
* `report/`: Individual report. [View the PDF Report](Individual_Analysis/Individual_contribution_report.pdf)

* `code/`: Python codes. [View Python Code](Individual_Analysis/app.py)
---

## 🔗 Related Repository

This project is an individual enhancement of the original group project:

➡️ **Student Performance Analysis**
[Insert Repository Link Here]

---

## ⚠️ Disclaimer

This system is intended for educational and analytical purposes only.

Predictions are generated using historical 2020 examination data and should not be interpreted as official university admission decisions.

Official eligibility is determined by the relevant Sri Lankan higher education authorities.

---

## 👩‍💻 Author

**Amashi Fernando**
Final-Year Applied Statistics Undergraduate
University of Colombo
Sri Lanka
