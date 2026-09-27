# Business Insights

These findings are calculated from the cleaned transaction table, not assumed in advance.

## Transaction value distribution

The average transaction is INR 1,574.34 while the median is INR 459.03. This gap indicates a right-skewed distribution in which larger transactions pull the mean above the typical transaction. Percentiles and IQR outlier counts are generated in `quality_report.json`; the dashboard includes the distribution bands and percentile profile.

## Geographic performance

MUMBAI is the highest-value location in the current extract, with INR 179,689,117 in transaction value. This is a descriptive result for the available period, not a causal conclusion about customer quality or branch performance.

## Transaction timing

20:00 is the peak transaction hour by transaction count, with 97,053 transactions. This can guide further investigation of service capacity and digital-channel activity.

## Customer concentration

The top customer contributes 0.09% of total transaction value. Customer measures are derived from transaction records, so this should be described as transaction-derived customer behavior rather than a complete customer-master analysis.

## Data quality

There are 174,917 suspicious DOB values that were converted to missing. This is an important limitation for age analysis and is surfaced rather than hidden.

## Period caveat

The dataset covers roughly two and a half months. The October total is partial through October 21, so month-to-month comparisons should not be framed as annual performance or a confirmed trend reversal.
