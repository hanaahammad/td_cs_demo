import streamlit as st
import pandas as pd

from teradataml import (
create_context,
execute_sql,
DataFrame
)

import streamlit as st
import pandas as pd

from teradataml import (
create_context,
execute_sql,
DataFrame
)


# ----------------------------------
# SAFE CONNECTION MANAGER ⭐ ADD HERE
# ----------------------------------

def ensure_connection(host,user,password):

    try:

        # test if connection still alive
        execute_sql("SELECT 1;")

    except:

        create_context(

            host=host,
            username=user,
            password=password

        )
        
# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title("🛠 EDW Admin — Data Overview")

st.markdown("""

Inspect EDW tables and validate ingestion.

Tables:

• transactions

• customer_demographics

• credit_risk

""")


# --------------------------------------------------
# CONNECTION
# --------------------------------------------------

st.subheader("Connection")


host=st.text_input("Host")

user=st.text_input("User")

password=st.text_input(
"Password",
type="password"
)


if "connected" not in st.session_state:

 if st.button("🔌 Connect"):

  try:

   create_context(

    host=host,
    username=user,
    password=password

   )

   st.session_state.connected=True

   st.success("Connected")

  except Exception as e:

   st.error(e)


if "connected" not in st.session_state:

 st.stop()



# --------------------------------------------------
# TABLES TO MONITOR
# --------------------------------------------------

tables=[

"transactions",

"customer_demographics",

"credit_risk"

]


st.divider()

st.subheader("📊 Tables Statistics")


for table in tables:

 st.markdown(f"## {table}")


 # -----------------------
 # SQL CODE DISPLAY
 # -----------------------

 stats_sql=f"""

SELECT COUNT(*) AS row_count
FROM {table};

"""

 with st.expander(

 f"Show SQL used for {table}",

 expanded=False

 ):

  st.code(

  stats_sql,

  language="sql"

  )


 # -----------------------
 # EXECUTE SQL
 # -----------------------

 try:

  cursor=execute_sql(

  stats_sql

  )

  count=cursor.fetchall()[0][0]


  st.metric(

  f"{table} rows",

  count

  )

 except Exception as e:

  st.warning(e)



 # -----------------------
 # EXTRA STATS
 # -----------------------

 try:

  if table=="transactions":

   sql="""

   SELECT

   MIN(tx_date),

   MAX(tx_date),

   AVG(amount)

   FROM transactions;

   """

   cur=execute_sql(sql)

   row=cur.fetchall()[0]


   col1,col2,col3=st.columns(3)


   with col1:

    st.metric(

    "First Tx",

    str(row[0])

    )


   with col2:

    st.metric(

    "Last Tx",

    str(row[1])

    )


   with col3:

    st.metric(

    "Avg Amount",

    round(row[2],2)

    )


  if table=="credit_risk":

   sql="""

   SELECT

   AVG(credit_score),

   MAX(credit_score),

   MIN(credit_score)

   FROM credit_risk;

   """

   cur=execute_sql(sql)

   row=cur.fetchall()[0]


   col1,col2,col3=st.columns(3)


   with col1:

    st.metric(

    "Avg Score",

    round(row[0],1)

    )


   with col2:

    st.metric(

    "Max Score",

    row[1]

    )


   with col3:

    st.metric(

    "Min Score",

    row[2]

    )

 except:

  pass



 # -----------------------
 # PREVIEW
 # -----------------------

 st.subheader("Preview")


 try:

  df=DataFrame(

  table

  )

  preview=df.head(

  100

  ).to_pandas()


  st.dataframe(

  preview,

  width="stretch"

  )

 except Exception as e:

  st.warning(e)



 st.divider()