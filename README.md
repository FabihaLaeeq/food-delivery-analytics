# 🍔 Food Delivery Analytics Dashboard

A Python and Pandas based analytics dashboard that analyzes food delivery performance and identifies the operational factors behind delivery delays.

The project focuses on **data analysis, statistical insights, visualization, and AI-powered business interpretation** without using Machine Learning.

## 🚀 Live Demo

[Streamlit App]

## 📊 Project Overview

The dashboard analyzes **38,964 food delivery records** and explores how factors such as traffic, weather, delivery distance, and vehicle conditions affect delivery performance.

### Key Metrics

* **38,964** total deliveries
* **26.58 minutes** average delivery time
* **9.77 km** average delivery distance
* **23.59 km/h** average delivery speed
* **4.63** average delivery-person rating

## 🔍 Analysis Performed

### 1. Dataset Understanding

The dashboard provides:

* Dataset dimensions
* Column information
* Data types
* Missing-value analysis
* Duplicate detection
* Data-cleaning summary
* Dataset preview

### 2. Basic Analysis

Key delivery-performance metrics are calculated using Pandas, including:

* Total deliveries
* Average delivery time
* Minimum and maximum delivery time
* Average distance
* Average speed
* Average delivery-person rating
* Average delivery-person age

### 3. Competition Questions

The analysis answers three key operational questions.

#### Traffic Impact

Jam traffic has the highest average delivery time:

**31.44 minutes**

#### Distance Impact

The Pearson correlation between delivery distance and delivery time is:

**0.322**

This indicates a positive relationship between distance and delivery time.

#### Combined Conditions

The slowest combination is:

**Fog weather + Jam traffic**

with an average delivery time of:

**36.89 minutes**

## 📈 Visualizations

The dashboard includes four visualizations:

1. 🚦 Average Delivery Time by Traffic
2. 📍 Delivery Distance vs Delivery Time
3. 🌦️ Average Delivery Time by Weather
4. 🚗 Average Delivery Time by Vehicle Condition

The charts use a **premium muted color palette** for a clean analytical dashboard aesthetic.

## 🤖 AI-Powered Explanation

The dashboard uses **Gemini AI** to interpret the calculated analytical results.

Instead of asking the AI to perform the analysis itself, Python and Pandas first calculate the actual metrics. Gemini then converts those findings into concise business-oriented insights.

This keeps the numerical analysis deterministic while using AI for interpretation.

## 🧹 Data Cleaning

The cleaning process includes:

* Removing exact duplicate rows
* Converting relevant columns to numeric values
* Handling missing delivery-person age and rating values using median values
* Removing invalid or non-positive delivery times
* Removing invalid or non-positive distances
* Calculating delivery speed from distance and delivery time

## 🛠️ Technologies

* Python
* Pandas
* Matplotlib
* Streamlit
* Google Gemini API

## 📁 Project Structure

```text
food_delivery_hackathon/
│
├── app.py
├── analysis.py
├── visualization.py
├── ai_explanation.py
├── food_delivery_dataset.csv
├── requirements.txt
├── .gitignore
└── README.md
```

## ▶️ Run Locally

Clone the repository:

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

Navigate into the project:

```bash
cd food_delivery_hackathon
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Add your Gemini API key to `.env`:

```text
GEMINI_API_KEY=your_api_key_here
```

Run the application:

```bash
streamlit run app.py
```

## 🎯 Business Takeaways

The analysis highlights three important operational findings:

* 🚦 **Traffic congestion** has a major impact on delivery time.
* 📍 **Longer delivery distances** generally require more delivery time.
* 🌦️ **Combined adverse conditions**, particularly fog and heavy traffic, can significantly increase delivery delays.

These insights can help food-delivery businesses identify operational bottlenecks and prioritize delivery optimization efforts.

## 📌 Project Goal

This project demonstrates how **Python + Pandas + statistical analysis + visualization + generative AI** can transform raw operational data into understandable business insights.

**No Machine Learning was used.**

