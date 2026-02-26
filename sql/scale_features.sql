CREATE MULTISET TABLE segmentation_dataset_scaled AS (

SELECT

customer_id,

(monetary-MIN(monetary) OVER())
/
NULLIFZERO(MAX(monetary) OVER()-MIN(monetary) OVER())
AS monetary_scaled,


(frequency-MIN(frequency) OVER())
/
NULLIFZERO(MAX(frequency) OVER()-MIN(frequency) OVER())
AS frequency_scaled,


(recency_days-MIN(recency_days) OVER())
/
NULLIFZERO(MAX(recency_days) OVER()-MIN(recency_days) OVER())
AS recency_scaled,


(credit_score-MIN(credit_score) OVER())
/
NULLIFZERO(MAX(credit_score) OVER()-MIN(credit_score) OVER())
AS credit_score_scaled

FROM segmentation_dataset

) WITH DATA;