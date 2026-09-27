# Power BI Build Guide

A `.pbix` file cannot be generated reliably as plain text; create it in Power BI Desktop using the cleaned CSV and the model below. The HTML dashboard remains an additional portfolio presentation.

## Import and model

1. Get Data > Text/CSV > `data/cleaned/bank_transactions_cleaned.csv`.
2. Rename the table to `BankTransactions`.
3. Set dates, times, whole numbers, decimal numbers, and currency types correctly.
4. Create a `Date` table from the minimum and maximum transaction dates.
5. Relate `Date[Date]` (one) to `BankTransactions[transaction_date]` (many).
6. Mark `Date` as the date table and sort month names by month number.

This is a transaction-grain model. Customer analysis is derived from transaction rows; do not present it as a complete customer master dataset.

## Pages

- Executive Overview: KPI cards, period-aware monthly trend, location value, transaction distribution, and data-quality card.
- Customer Analytics: derived customer count, gender, age group, top customers, frequency, and balance.
- Transaction Analytics: count/value, percentile profile, distribution, hourly activity, and high-value transactions.
- Geographic Analytics: location count/value/average, ranking table, and location slicer.

Add slicers for year, month, gender, location, age group, and transaction value group. Use drill-down on the date hierarchy and a report-page tooltip for location and customer summaries.

## Validation checklist

- Display the period as `2016-08-01 to 2016-10-21`.
- Label October as partial through October 21.
- Confirm total transactions = 1,048,567 and unique customers = 884,265.
- Confirm total value = INR 1,650,795,731.57.
- Confirm no train/test split is used.
