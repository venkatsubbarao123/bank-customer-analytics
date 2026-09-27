# Data Dictionary

The cleaned table is transaction-grain data. Customer-level metrics are derived by grouping transaction records by `customer_id`; this is not a complete customer master table.

| Column | Meaning | Data type |
|---|---|---|
| `transaction_id` | Unique transaction identifier | String |
| `customer_id` | Customer identifier | String |
| `customer_dob` | Customer date of birth after validation | Date |
| `customer_gender` | Standardized gender: Female, Male, or Unknown | Categorical |
| `customer_location` | Standardized customer location | Categorical |
| `customer_account_balance` | Account balance reported on the transaction record | Numeric, INR |
| `transaction_date` | Date of the transaction | Date |
| `transaction_time` | Time of the transaction | Time |
| `transaction_amount_inr` | Transaction amount | Numeric, INR |
| `transaction_year` | Calendar year derived from transaction date | Integer |
| `transaction_month` | Calendar month number | Integer |
| `transaction_month_name` | Calendar month abbreviation | String |
| `transaction_quarter` | Calendar quarter | Categorical |
| `transaction_day` | Day of month | Integer |
| `transaction_day_name` | Day name | Categorical |
| `transaction_hour` | Hour derived from transaction time | Integer |
| `time_period` | Night, Morning, Afternoon, or Evening | Categorical |
| `customer_age` | Approximate age at the latest transaction date, when valid | Numeric |
| `age_group` | 18-25, 26-35, 36-45, 46-55, 56+, or Unknown | Categorical |
| `transaction_value_group` | Low, Medium, or High based on transaction quartiles | Categorical |

## Source columns

The raw CSV uses the original names `TransactionID`, `CustomerID`, `CustomerDOB`, `CustGender`, `CustLocation`, `CustAccountBalance`, `TransactionDate`, `TransactionTime`, and `TransactionAmount (INR)`. The raw file remains unchanged.
