import streamlit as st
import time
import pandas as pd

from teradataml import (
create_context,
execute_sql,
DataFrame
)


# ====================================
# CONFIGURATION ⭐ CHANGE THIS
# ====================================

DATABASE="DEMO_USER"



# ====================================
# SAFE CONNECTION
# ====================================

def ensure_connection(host,user,password):

    try:

        execute_sql("SELECT 1;")

    except:

        create_context(

        host=host,
        username=user,
        password=password

        )



# ====================================
# SAFE DROP
# ====================================

def drop_table(name):

    try:

        execute_sql(

        f"DROP TABLE {DATABASE}.{name};"

        )

        st.write(f"Dropped {name}")

    except:

        pass



# ====================================
# HEADER
# ====================================

st.title("⚙ Feature Engineering SAFE Pipeline")


st.markdown("""

Transactions

↓

RFM Behaviour

↓

Segmentation Dataset

↓

Scaled ML Dataset

""")


# ====================================
# CONNECTION
# ====================================

host=st.text_input("Host")

user=st.text_input("User")

password=st.text_input(
"Password",
type="password"
)


if st.button("🔌 Connect"):

 create_context(

 host=host,
 username=user,
 password=password

 )

 st.session_state.connected=True

 st.success("Connected")


if "connected" not in st.session_state:

 st.stop()


ensure_connection(

host,

user,

password

)



# ====================================
# TX COUNT CHECK
# ====================================

st.divider()

st.subheader("Transactions Check")


try:

 tx=execute_sql(

 f"SELECT COUNT(*) FROM {DATABASE}.transactions;"

 )

 tx_count=tx.fetchall()[0][0]

 st.metric(

 "Transactions rows",

 tx_count

 )

except Exception as e:

 st.error(e)

 st.stop()



# ====================================
# STEP 1 RFM
# ====================================

st.divider()

st.subheader("Step 1 — Build RFM")


rfm_sql=f"""

CREATE MULTISET TABLE {DATABASE}.customer_features_rfm AS (

SELECT

t.customer_id,

SUM(t.amount) AS monetary,

COUNT(*) AS frequency,

g.max_tx_date
-
MAX(t.tx_date)

AS recency_days

FROM {DATABASE}.transactions t

CROSS JOIN (

SELECT

MAX(tx_date) AS max_tx_date

FROM {DATABASE}.transactions

) g

GROUP BY

t.customer_id,
g.max_tx_date

) WITH DATA;

"""


st.code(rfm_sql,"sql")


if st.button("🚀 Build RFM"):

 drop_table("customer_features_rfm")

 start=time.time()

 execute_sql(rfm_sql)

 duration=round(time.time()-start,2)


 verify=execute_sql(

 f"""

 SELECT COUNT(*)

 FROM {DATABASE}.customer_features_rfm;

 """

 )

 customers=verify.fetchall()[0][0]


 col1,col2=st.columns(2)

 col1.metric("Transactions",tx_count)

 col2.metric("Customers",customers)


 st.success(

 f"RFM created in {duration}s"

 )



# ====================================
# STEP 2 SEGMENTATION
# ====================================

st.divider()

st.subheader("Step 2 — Join Risk + Demographics")


seg_sql=f"""

CREATE MULTISET TABLE {DATABASE}.segmentation_dataset AS (

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

FROM {DATABASE}.customer_features_rfm r

LEFT JOIN {DATABASE}.customer_demographics d

ON r.customer_id=d.customer_id

LEFT JOIN {DATABASE}.credit_risk cr

ON r.customer_id=cr.customer_id

) WITH DATA;

"""


st.code(seg_sql,"sql")


if st.button("🚀 Build Segmentation Dataset"):

 drop_table("segmentation_dataset")

 execute_sql(seg_sql)

 st.success("Segmentation dataset ready")



# ====================================
# STEP 3 SCALE
# ====================================

st.divider()

st.subheader("Step 3 — ML Scaling")


scale_sql=f"""

CREATE MULTISET TABLE {DATABASE}.segmentation_dataset_scaled AS (

SELECT

customer_id,

(monetary-MIN(monetary) OVER())
/
NULLIFZERO(MAX(monetary) OVER()-MIN(monetary) OVER())
monetary_scaled,

(frequency-MIN(frequency) OVER())
/
NULLIFZERO(MAX(frequency) OVER()-MIN(frequency) OVER())
frequency_scaled,

(recency_days-MIN(recency_days) OVER())
/
NULLIFZERO(MAX(recency_days) OVER()-MIN(recency_days) OVER())
recency_scaled

FROM {DATABASE}.segmentation_dataset

) WITH DATA;

"""


st.code(scale_sql,"sql")


if st.button("🚀 Scale Dataset"):

 drop_table("segmentation_dataset_scaled")

 execute_sql(scale_sql)

 st.success("Scaled dataset created")



# ====================================
# PREVIEW
# ====================================

st.divider()

st.subheader("Preview Dataset")


try:

 df = DataFrame(
"segmentation_dataset"
)

 pdf=df.head(100).to_pandas()

 st.dataframe(

 pdf,

 width="stretch"

 )

except Exception as e:

 st.info(e)