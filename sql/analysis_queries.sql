-- Reusable analysis queries for bank_transactions

-- 1. Daily transaction volume and value
SELECT
    transaction_date,
    COUNT(*) AS transaction_count,
    SUM(transaction_amount_inr) AS total_transaction_amount_inr,
    AVG(transaction_amount_inr) AS average_transaction_amount_inr
FROM bank_transactions
GROUP BY transaction_date
ORDER BY transaction_date;

-- 2. Customer transaction summary
SELECT
    customer_id,
    COUNT(*) AS transaction_count,
    SUM(transaction_amount_inr) AS total_spend_inr,
    AVG(transaction_amount_inr) AS average_transaction_inr,
    MAX(customer_account_balance) AS account_balance_inr
FROM bank_transactions
GROUP BY customer_id
ORDER BY total_spend_inr DESC;

-- 3. Location performance
SELECT
    customer_location,
    COUNT(DISTINCT customer_id) AS customer_count,
    COUNT(*) AS transaction_count,
    SUM(transaction_amount_inr) AS total_transaction_amount_inr
FROM bank_transactions
GROUP BY customer_location
ORDER BY total_transaction_amount_inr DESC;

-- 4. Gender-level comparison
SELECT
    customer_gender,
    COUNT(DISTINCT customer_id) AS customer_count,
    COUNT(*) AS transaction_count,
    AVG(transaction_amount_inr) AS average_transaction_amount_inr
FROM bank_transactions
GROUP BY customer_gender
ORDER BY customer_gender;

-- 5. Largest transactions
SELECT *
FROM bank_transactions
ORDER BY transaction_amount_inr DESC
LIMIT 20;

-- 6. Monthly transaction trend
SELECT DATE_TRUNC('month', transaction_date) AS month,
       COUNT(*) AS transaction_count,
       SUM(transaction_amount_inr) AS total_amount_inr
FROM bank_transactions
GROUP BY 1 ORDER BY 1;

-- 7. Top 10 customers by value
SELECT customer_id, COUNT(*) AS transaction_count,
       SUM(transaction_amount_inr) AS total_amount_inr,
       RANK() OVER (ORDER BY SUM(transaction_amount_inr) DESC) AS value_rank
FROM bank_transactions
GROUP BY customer_id ORDER BY total_amount_inr DESC LIMIT 10;

-- 8. Running monthly value
WITH monthly AS (
    SELECT DATE_TRUNC('month', transaction_date) AS month,
           SUM(transaction_amount_inr) AS amount_inr
    FROM bank_transactions GROUP BY 1
)
SELECT month, amount_inr,
       SUM(amount_inr) OVER (ORDER BY month) AS running_amount_inr
FROM monthly ORDER BY month;

-- 9. Location contribution percentage
WITH locations AS (
    SELECT customer_location, SUM(transaction_amount_inr) AS amount_inr
    FROM bank_transactions GROUP BY customer_location
)
SELECT customer_location, amount_inr,
       amount_inr / NULLIF(SUM(amount_inr) OVER (), 0) * 100 AS contribution_percent
FROM locations ORDER BY amount_inr DESC;

-- 10. High-value transactions using the 75th percentile threshold
SELECT transaction_id, customer_id, transaction_date, transaction_amount_inr
FROM bank_transactions
WHERE transaction_amount_inr >= (SELECT PERCENTILE_CONT(0.75)
                                  WITHIN GROUP (ORDER BY transaction_amount_inr)
                                  FROM bank_transactions)
ORDER BY transaction_amount_inr DESC;

-- 11. Repeat customers (more than one transaction)
SELECT customer_id, COUNT(*) AS transaction_count,
       MIN(transaction_date) AS first_transaction,
       MAX(transaction_date) AS last_transaction
FROM bank_transactions GROUP BY customer_id
HAVING COUNT(*) > 1 ORDER BY transaction_count DESC;

-- 12. Time-period performance
SELECT CASE WHEN EXTRACT(HOUR FROM transaction_time) BETWEEN 6 AND 11 THEN 'Morning'
            WHEN EXTRACT(HOUR FROM transaction_time) BETWEEN 12 AND 16 THEN 'Afternoon'
            WHEN EXTRACT(HOUR FROM transaction_time) BETWEEN 17 AND 20 THEN 'Evening'
            ELSE 'Night' END AS time_period,
       COUNT(*) AS transaction_count, SUM(transaction_amount_inr) AS amount_inr
FROM bank_transactions GROUP BY 1 ORDER BY amount_inr DESC;

-- 13. Core portfolio KPIs
SELECT COUNT(*) AS total_transactions,
       COUNT(DISTINCT customer_id) AS unique_customers,
       SUM(transaction_amount_inr) AS total_value_inr,
       AVG(transaction_amount_inr) AS average_value_inr,
       MIN(transaction_amount_inr) AS minimum_value_inr,
       MAX(transaction_amount_inr) AS maximum_value_inr
FROM bank_transactions;

-- 14. Median and percentile profile
SELECT PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY transaction_amount_inr) AS p25,
       PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY transaction_amount_inr) AS p50,
       PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY transaction_amount_inr) AS p75,
       PERCENTILE_CONT(0.90) WITHIN GROUP (ORDER BY transaction_amount_inr) AS p90,
       PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY transaction_amount_inr) AS p95,
       PERCENTILE_CONT(0.99) WITHIN GROUP (ORDER BY transaction_amount_inr) AS p99
FROM bank_transactions;

-- 15. Customers above the average customer value
WITH customer_totals AS (
    SELECT customer_id, SUM(transaction_amount_inr) AS customer_value_inr
    FROM bank_transactions GROUP BY customer_id
)
SELECT customer_id, customer_value_inr
FROM customer_totals
WHERE customer_value_inr > (SELECT AVG(customer_value_inr) FROM customer_totals)
ORDER BY customer_value_inr DESC;

-- 16. Rank customers by transaction frequency with deterministic tie-breaking
SELECT customer_id, COUNT(*) AS transaction_count,
       DENSE_RANK() OVER (ORDER BY COUNT(*) DESC) AS frequency_rank,
       ROW_NUMBER() OVER (ORDER BY COUNT(*) DESC, customer_id) AS row_number
FROM bank_transactions
GROUP BY customer_id ORDER BY frequency_rank, customer_id;

-- 17. Monthly growth versus the prior available month
WITH monthly AS (
    SELECT DATE_TRUNC('month', transaction_date) AS month,
           SUM(transaction_amount_inr) AS amount_inr
    FROM bank_transactions GROUP BY 1
)
SELECT month, amount_inr,
       LAG(amount_inr) OVER (ORDER BY month) AS previous_month_amount_inr,
       (amount_inr - LAG(amount_inr) OVER (ORDER BY month)) /
       NULLIF(LAG(amount_inr) OVER (ORDER BY month), 0) * 100 AS growth_percent
FROM monthly ORDER BY month;

-- 18. Monthly ranking by transaction value
WITH monthly AS (
    SELECT DATE_TRUNC('month', transaction_date) AS month,
           SUM(transaction_amount_inr) AS amount_inr
    FROM bank_transactions GROUP BY 1
)
SELECT month, amount_inr,
       RANK() OVER (ORDER BY amount_inr DESC) AS monthly_value_rank
FROM monthly ORDER BY monthly_value_rank;

-- 19. Account balance bands and transaction behavior
SELECT CASE WHEN customer_account_balance < 10000 THEN 'Under 10k'
            WHEN customer_account_balance < 100000 THEN '10k-100k'
            ELSE '100k+' END AS balance_band,
       COUNT(*) AS transaction_count,
       COUNT(DISTINCT customer_id) AS customer_count,
       AVG(transaction_amount_inr) AS average_transaction_inr
FROM bank_transactions
GROUP BY 1 ORDER BY 1;

-- 20. Top 10% customer concentration
WITH customer_totals AS (
    SELECT customer_id, SUM(transaction_amount_inr) AS customer_value_inr
    FROM bank_transactions GROUP BY customer_id
), ranked AS (
    SELECT *, NTILE(10) OVER (ORDER BY customer_value_inr DESC) AS value_decile
    FROM customer_totals
)
SELECT SUM(CASE WHEN value_decile = 1 THEN customer_value_inr ELSE 0 END) AS top_decile_value_inr,
       SUM(customer_value_inr) AS total_customer_value_inr,
       SUM(CASE WHEN value_decile = 1 THEN customer_value_inr ELSE 0 END) /
       NULLIF(SUM(customer_value_inr), 0) * 100 AS top_decile_contribution_percent
FROM ranked;
