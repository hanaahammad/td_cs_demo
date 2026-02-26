CREATE MULTISET TABLE segmentation_dataset AS (

SELECT

r.customer_id,

r.monetary,

r.frequency,

r.recency_days,

d.age,

d.income,

d.employment_years,

cr.credit_score,

cr.loan_exposure,

cr.late_payments

FROM customer_features_rfm r

LEFT JOIN customer_demographics d
ON r.customer_id=d.customer_id

LEFT JOIN credit_risk cr
ON r.customer_id=cr.customer_id

) WITH DATA;