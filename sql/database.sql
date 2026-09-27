-- Bank Customer Transaction Analytics schema
-- Compatible with PostgreSQL-style SQL. Adjust the load command for your database.

CREATE TABLE IF NOT EXISTS bank_transactions (
    transaction_id VARCHAR(32) PRIMARY KEY,
    customer_id VARCHAR(32) NOT NULL,
    customer_dob DATE,
    customer_gender VARCHAR(16),
    customer_location VARCHAR(128),
    customer_account_balance DECIMAL(18, 2),
    transaction_date DATE NOT NULL,
    transaction_time TIME,
    transaction_amount_inr DECIMAL(18, 2) NOT NULL
);

-- Example PostgreSQL load after producing the cleaned CSV:
-- COPY bank_transactions(
--     transaction_id, customer_id, customer_dob, customer_gender,
--     customer_location, customer_account_balance, transaction_date,
--     transaction_time, transaction_amount_inr
-- )
-- FROM '/absolute/path/to/data/cleaned/bank_transactions_cleaned.csv'
-- WITH (FORMAT csv, HEADER true);
