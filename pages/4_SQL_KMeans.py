import streamlit as st
import pandas as pd
import plotly.express as px
import time

from teradataml import execute_sql


# =====================================================
# CONFIG
# =====================================================

DATABASE="DEMO_USER"


# =====================================================
# SAFE DROP
# =====================================================

def safe_drop(name):

    try:
        execute_sql(
        f"DROP TABLE {DATABASE}.{name};"
        )
    except:
        pass


# =====================================================
# HEADER
# =====================================================

st.title("🏦 SQL Machine Learning inside Teradata")


st.markdown("""

This page demonstrates:

• Native ML using TD_KMeans.

• Bring Your Own Model using PMML.

• SQL scoring using PMMLPredict.

All executed inside the database.

""")


# =====================================================
# DATASET
# =====================================================

table="segmentation_dataset_scaled"

features=[

"monetary_scaled",
"frequency_scaled",
"recency_scaled"

]

model="kmeans_sql"


st.info(

f"""

Training Table :

{DATABASE}.{table}

Features :

{features}

"""

)


k=st.slider(

"Clusters",

2,

8,

4

)


# =====================================================
# SQL KMEANS
# =====================================================

st.subheader("1️⃣ Native SQL KMeans")


if st.button("🚀 Train SQL KMeans"):

    try:

        safe_drop(model)

        target=",".join(

        [f"'{c}'" for c in features]

        )


        sql=f"""

SELECT *

FROM TD_KMeans(

ON {DATABASE}.{table} AS InputTable

OUT TABLE ModelTable({model})

USING

IdColumn('customer_id')

TargetColumns({target})

NumClusters({k})

OutputClusterAssignment('true')

MaxIterNum(100)

) AS dt;

"""


        st.code(sql,"sql")


        start=time.time()

        execute_sql(sql)

        dur=round(time.time()-start,2)


        st.success(

        f"KMeans completed in {dur}s"

        )

    except Exception as e:

        st.error(e)



# =====================================================
# DISTRIBUTION
# =====================================================

st.subheader("Cluster Distribution")


try:

 cur=execute_sql(

 f"""

SELECT

td_clusterid_kmeans,

COUNT(*)

FROM {DATABASE}.{model}

GROUP BY 1;

"""

 )

 rows=cur.fetchall()

 cols=[c[0] for c in cur.description]


 df=pd.DataFrame(rows,columns=cols)


 fig=px.bar(

 df,

 x=cols[0],

 y=cols[1],

 title="Customers per Cluster"

 )

 st.plotly_chart(fig,width="stretch")

except:

 st.info("Train SQL KMeans first.")



# =====================================================
# PMML IMPORT
# =====================================================

st.divider()

st.subheader("2️⃣ Import External Model (PMML BYOM)")


st.markdown("""

Example SQL to register a PMML model inside Teradata.

Model file must exist on database accessible location.

""")


pmml_sql=f"""

CREATE MULTISET TABLE {DATABASE}.pmml_models
(
model_id INTEGER,
model PMML
);

INSERT INTO {DATABASE}.pmml_models
SELECT
1,
NEW PMML('model.pmml');

"""


st.code(pmml_sql,"sql")



# =====================================================
# PMML PREDICT
# =====================================================

st.subheader("3️⃣ Score Using PMMLPredict")


pmml_predict=f"""

SELECT *

FROM PMMLPredict(

ON {DATABASE}.{table} AS InputTable

ON {DATABASE}.pmml_models AS ModelTable

DIMENSION USING

Accumulate('customer_id')

) AS dt;

"""


st.code(pmml_predict,"sql")


st.success("""

SQL Only Workflow:

Train Native Model.

OR

Import External Model.

Score directly inside Teradata.

""")