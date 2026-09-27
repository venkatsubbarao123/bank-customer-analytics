
# Bank Customer & Transaction Analytics

An analytics-first portfolio project using Python, pandas, NumPy, SQL, Power BI/DAX, and a responsive HTML/CSS/JavaScript dashboard. It analyzes the full transaction extract; there is no train/test split because this is not a machine-learning project. Customer analytics are derived from transaction records, not a complete customer master table.

## Run the project on Windows

Open PowerShell in this project folder: `D:\Bank_Customer_Analytics`.

1. Confirm the source file exists at `data/raw/bank_transactions.csv` and leave it unchanged.
2. Install the Python dependencies:

	```powershell
	python -m pip install pandas numpy
	```

	If `python` is not on PATH, use the Python interpreter selected in VS Code, for example:

	```powershell
	& 'C:\Program Files\Python313\python.exe' -m pip install pandas numpy
	```

3. Rebuild the cleaned data and analytical outputs:

	```powershell
	python scripts/build_analytics.py
	```

4. Start the local dashboard server from the project root:

	```powershell
	python -m http.server 8000
	```

5. Open [http://localhost:8000/dashboard/](http://localhost:8000/dashboard/) in a browser. Keep the PowerShell server window open while using the dashboard. Press `Ctrl+C` to stop it.

If the `python` command is unavailable, run both commands with the same full Python path used in step 2.

## Expected verification results

After a successful rebuild, the main dashboard totals should be:

- Transactions: `1,048,567`
- Unique customers: `884,265`
- Total transaction value: `INR 1,650,795,731.57`
- Average transaction: approximately `INR 1,574.34`
- Date range: `2016-08-01` to `2016-10-21`

Test the filters with `Location = MUMBAI` and `Location = HYDERABAD`. The KPI values must change. `Year = 2016` can remain unchanged because the current extract contains only 2016.

## Outputs

The pipeline writes `data/cleaned/bank_transactions_cleaned.csv`, customer/location/monthly/hourly summaries, percentile and distribution analysis, a quality report, actual-data insights, filter aggregates, and `dashboard_data.json`. The three notebooks explain understanding, cleaning/feature engineering, and EDA. SQL schema and 20 business queries are in `sql/`.

## Analytical scope

The available transaction period is `2016-08-01` through `2016-10-21`. August and September are complete months; October is partial through October 21. Month totals are therefore descriptive and should not be presented as annual banking performance.

## Documentation

- [Data dictionary](documentation/data_dictionary.md)
- [Data-quality report](documentation/data_quality.md)
- [Business insights](documentation/insights.md)
- [Power BI build guide and DAX measures](powerbi/README.md)

Power BI Desktop is required to create the final `.pbix` binary. The repository includes the model guidance and measures but does not pretend that a `.pbix` was generated automatically.

## Data quality policy

Column names and categories are standardized, dates and times are parsed with invalid values coerced to missing, suspicious DOB values are investigated and nulled, required transaction fields are enforced, and duplicate transaction IDs are removed only if present. Missing customer attributes are retained as `Unknown` where appropriate.

## Source-data note

Check the source dataset's Kaggle license and redistribution terms before publishing the raw CSV to GitHub. The raw file is intentionally kept separate from generated outputs.

## File cleanup decision

No unnecessary files were found. Keep the raw CSV as the pipeline input, the cleaned CSV and summary files as reproducible analytical outputs, the notebooks as the analysis record, and the SQL/Power BI/dashboard files as project deliverables. Cache files such as `__pycache__`, `.ipynb_checkpoints`, virtual environments, and VS Code settings are already excluded by `.gitignore` and should not be added to the project.
