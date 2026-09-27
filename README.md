
````markdown
# Bank Customer & Transaction Analytics

An end-to-end data analytics project focused on customer behavior, transaction patterns, data quality, and business insights using a real-world banking transaction dataset.

The project demonstrates a complete analytics workflow using **Python, Pandas, NumPy, SQL, Power BI/DAX, and an interactive HTML/CSS/JavaScript dashboard**.

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
````

---

## 🔄 Analytics Workflow

```text
Raw Banking Dataset
        ↓
Data Understanding
        ↓
Data Cleaning & Validation
        ↓
Feature Engineering
        ↓
Exploratory Data Analysis
        ↓
Business Aggregations
        ↓
SQL Analysis
        ↓
Power BI / DAX
        ↓
Interactive Web Dashboard
        ↓
Business Insights
```

---

## 🧹 Data Cleaning & Quality

The Python analytics pipeline performs the following data-quality operations:

* Standardizes column names and categorical values
* Parses transaction dates and times
* Handles invalid date/time values
* Identifies suspicious customer DOB values
* Converts invalid/suspicious DOB values to missing
* Validates required transaction fields
* Checks for duplicate transaction IDs
* Retains missing customer attributes as `Unknown` where appropriate
* Generates a structured data-quality report

### Verified Quality Results

* Source rows analyzed: **1,048,567**
* Cleaned rows retained: **1,048,567**
* Duplicate transaction IDs: **0**
* Suspicious DOB values converted to missing: **174,917**

---

## 📈 Exploratory Data Analysis

The analysis covers:

### Transaction Analysis

* Total transaction volume
* Total transaction value
* Average transaction amount
* Median transaction amount
* Transaction value distribution
* High-value transaction analysis

### Customer Analysis

* Unique customer count
* Customer distribution by gender
* Customer activity by location
* Customer transaction behavior

### Time Analysis

* Monthly transaction trends
* Hourly transaction activity
* Peak transaction periods

### Geographic Analysis

* Location-level transaction volume
* Location-level transaction value
* Average transaction amount by location
* Top-performing locations

---

## 📍 Selected Business Findings

Based on the analyzed transaction data:

### Mumbai

* Customers: **101,730**
* Transactions: **103,596**
* Transaction value: **₹179,689,116.82**
* Average transaction: **₹1,734.52**

### Hyderabad

* Customers: **22,929**
* Transactions: **23,049**
* Transaction value: **₹36,177,394.43**
* Average transaction: **₹1,570.59**

### Gender Analysis

Female customers account for:

* **268,662 distinct customers**
* **281,936 transactions**

The dashboard provides additional interactive filtering for gender and location.

---

## 🖥️ Interactive Dashboard

The project includes a responsive web dashboard built with:

* HTML
* CSS
* JavaScript
* JSON-based analytical outputs

### Dashboard Features

* KPI cards
* Transaction trend analysis
* Location analysis
* Gender analysis
* Customer segmentation
* Transaction distribution
* Year filtering
* Gender filtering
* Location filtering
* Reset filters
* Data-quality indicators
* Business insights

The dashboard filters dynamically update the displayed analytical metrics and visualizations.

---

## 🗃️ SQL Analysis

The `sql/` directory contains:

* Database schema
* Analytical SQL queries
* Business-oriented transaction analysis

Example analysis areas include:

* Customer transaction activity
* Location performance
* Gender-based analysis
* Transaction trends
* High-value transactions
* Aggregated customer metrics

---

## 📊 Power BI

The `powerbi/` directory contains:

* Power BI implementation guidance
* DAX measures
* Recommended analytical model structure

The repository does **not** include a `.pbix` file because Power BI Desktop is required to create the final binary report.

---

## 📓 Jupyter Notebooks

The project contains three notebooks representing the analytical workflow:

### `01_data_understanding.ipynb`

Dataset structure, columns, data types, missing values, and initial observations.

### `02_data_cleaning.ipynb`

Data cleaning, validation, transformation, and feature preparation.

### `03_eda.ipynb`

Exploratory analysis, statistical summaries, trends, distributions, and business insights.

---

## ▶️ Run the Project Locally

### 1. Clone the repository

```bash
git clone https://github.com/venkatsubbarao123/bank-customer-analytics.git
cd bank-customer-analytics
```

### 2. Install dependencies

```bash
python -m pip install -r requirements.txt
```

If the `python` command is unavailable on Windows:

```powershell
& 'C:\Program Files\Python313\python.exe' -m pip install -r requirements.txt
```

### 3. Add the source dataset

Place the original dataset at:

```text
data/raw/bank_transactions.csv
```

Keep the original source file unchanged.

### 4. Run the analytics pipeline

```bash
python scripts/build_analytics.py
```

The pipeline generates the cleaned analytical outputs and dashboard data.

### 5. Start the dashboard

From the project root:

```bash
python -m http.server 8000
```

Open:

```text
http://localhost:8000/dashboard/
```

Press `Ctrl+C` to stop the local server.

---

## ✅ Dashboard Verification

After running the pipeline, verify the following:

```text
Transactions        : 1,048,567
Unique Customers    : 884,265
Transaction Value   : ₹1,650,795,731.57
Average Transaction : ₹1,574.34
Date Range          : 2016-08-01 to 2016-10-21
```

Test the dashboard filters using:

```text
Location = MUMBAI
Location = HYDERABAD
Gender
Year = 2016
```

The KPI values should update when filters are applied.

---

## 📅 Data Scope

The available transaction period is:

```text
2016-08-01 → 2016-10-21
```

August and September represent complete months in the available extract.

October contains data only through **October 21**, so October should be treated as a **partial month**.

The project therefore focuses on descriptive analysis of the available transaction period rather than presenting the results as annual banking performance.

---

## 📚 Documentation

Additional project documentation:

* [Analysis Plan](documentation/analysis_plan.md)
* [Data Dictionary](documentation/data_dictionary.md)
* [Data Quality Report](documentation/data_quality.md)
* [Business Insights](documentation/insights.md)
* [Power BI Guide](powerbi/README.md)

---

## 🔐 Data & Redistribution

The raw banking transaction dataset is intentionally excluded from the GitHub repository.

Before redistributing or publishing the original dataset, verify the dataset provider's licensing and redistribution terms.

The repository focuses on the **analytics workflow, code, documentation, SQL, notebooks, and dashboard implementation**.

---

## 🎯 Project Objectives Demonstrated

This project demonstrates practical skills in:

* Data cleaning
* Data validation
* Exploratory data analysis
* Python data analysis
* Pandas and NumPy
* SQL querying
* Business KPI development
* Customer analytics
* Transaction analytics
* Data visualization
* Power BI/DAX concepts
* Dashboard development
* Data-quality analysis
* Git and GitHub
* Reproducible analytics workflows

---

## 👨‍💻 Author

**Choppavrapu Venkata Subbarao**

Data Analyst | Python | SQL | Excel | Power BI | Data Analytics

GitHub:
[https://github.com/venkatsubbarao123](https://github.com/venkatsubbarao123)
my project: https://bank-customer-analytics.netlify.app
live demo : http://localhost:8000/dashboard/
