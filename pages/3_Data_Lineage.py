import streamlit as st


st.title("🧬 Data Lineage Explorer")


st.markdown("""

Understand how datasets were produced.

Governance.

Transparency.

Reproducibility.

""")


# -----------------------------
# LINEAGE DICTIONARY
# -----------------------------

lineage={


"transactions":{

"sources":"External banking ingestion",

"sql":"Loaded during Data Setup.",

"explanation":"Raw banking transactions."


},


"customer_features_rfm":{

"sources":"""

transactions

""",

"sql":"""

SELECT

customer_id,

SUM(amount),

COUNT(*),

global_max_tx - last_tx

FROM transactions

GROUP BY customer_id

""",

"explanation":"Aggregation of behaviour."


},


"segmentation_dataset":{

"sources":"""

customer_features_rfm

customer_demographics

credit_risk

""",

"sql":"""

SELECT *

FROM customer_features_rfm r

LEFT JOIN customer_demographics d

LEFT JOIN credit_risk c

""",

"explanation":"Behaviour enriched with risk and demographics."


},


"segmentation_dataset_scaled":{

"sources":"segmentation_dataset",

"sql":"""

MIN MAX scaling applied.

(value - MIN)/(MAX-MIN)

""",

"explanation":"ML ready dataset."

}

}



# -----------------------------
# SELECT TABLE
# -----------------------------

table=st.selectbox(

"Choose Dataset",

list(lineage.keys())

)



info=lineage[table]


st.divider()

st.subheader("Upstream Sources")

st.code(info["sources"])



st.subheader("Transformation Logic")

st.code(

info["sql"],

language="sql"

)


st.subheader("Business Meaning")

st.info(

info["explanation"]

)