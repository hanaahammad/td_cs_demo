CREATE MULTISET TABLE DEMO_USER.customer_features_rfm AS (
SELECT

customer_id,

SUM(amount) AS monetary,

COUNT(*) AS frequency,

(
MAX(tx_date) OVER()
-
MAX(tx_date)

) AS recency_days

FROM transactions

GROUP BY 1

) WITH DATA;