# Bank Customer & Transaction Analytics

An end-to-end data analytics project focused on customer behavior, transaction patterns, data quality, and business insights using a real-world banking transaction dataset.

The project demonstrates a complete analytics workflow using **Python, Pandas, NumPy, SQL, Power BI/DAX, and an interactive HTML/CSS/JavaScript dashboard**.

> **Note:** This is a data analytics project, not a machine learning project. There is no train/test split. Customer-level metrics are derived from transaction records because the dataset does not contain a separate complete customer master table.

---

## 📊 Project Overview

The objective of this project is to transform a large raw banking transaction dataset into a structured analytical solution that can be used to understand:

- Customer transaction behavior
- Transaction volume and monetary value
- Customer distribution by gender and location
- Monthly and hourly transaction patterns
- High-value transaction behavior
- Data quality issues
- Geographic transaction activity
- Business-level banking insights

The project processes more than **1 million transaction records** and provides both reproducible analytical outputs and an interactive dashboard.

---

## 🚀 Key Results

| Metric | Result |
|---|---:|
| Total Transactions | **1,048,567** |
| Unique Customers | **884,265** |
| Total Transaction Value | **₹1,650,795,731.57** |
| Average Transaction | **₹1,574.34** |
| Median Transaction | **₹459.03** |
| P95 Transaction Value | **₹5,000** |
| Locations | **9,354** |
| Duplicate Transaction IDs | **0** |
| Analysis Period | **2016-08-01 to 2016-10-21** |

> October 2016 is a partial month ending on October 21. Therefore, October should not be interpreted as a complete monthly period or as a full-year trend.

---

## 🛠️ Technology Stack

### Programming & Analytics
- Python
- Pandas
- NumPy

### Database & Querying
- SQL
- MySQL-compatible SQL concepts

### Visualization & BI
- Power BI
- DAX
- HTML
- CSS
- JavaScript

### Development Environment
- Jupyter Notebook
- VS Code
- Git
- GitHub

---

## 📁 Project Structure

```text
Bank_Customer_Analytics/
│
├── data/
│   ├── raw/
│   │   └── bank_transactions.csv
│   │
│   └── cleaned/
│       ├── hourly_summary.csv
│       ├── insights.json
│       ├── location_summary.csv
│       ├── monthly_summary.csv
│       └── quality_report.json
│
├── documentation/
│   ├── analysis_plan.md
│   ├── data_dictionary.md
│   ├── data_quality.md
│   └── insights.md
│
├── notebooks/
│   ├── 01_data_understanding.ipynb
│   ├── 02_data_cleaning.ipynb
│   └── 03_eda.ipynb
│
├── powerbi/
│   ├── README.md
│   └── measures.dax
│
├── sql/
│   ├── database.sql
│   └── analysis_queries.sql
│
├── dashboard/
│   ├── index.html
│   ├── styles.css
│   ├── app.js
│   └── README.md
│
├── scripts/
│   └── build_analytics.py
│
├── requirements.txt
└── README.md
