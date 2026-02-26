import pandas as pd
import numpy as np

np.random.seed(42)

print("Creating banking demo dataset...")

customers = 50000

transactions_per_customer = 25


# ---------- TRANSACTIONS ----------

customer_ids = np.repeat(

    np.arange(1,customers+1),

    transactions_per_customer

)

rows=len(customer_ids)

transactions=pd.DataFrame({

"customer_id":customer_ids,

"tx_date":

pd.to_datetime("2023-01-01")

+pd.to_timedelta(

np.random.randint(0,730,rows),

unit="D"

),

"amount":

np.random.gamma(

shape=2,

scale=120,

size=rows

)

})


transactions.to_csv(

"transactions.csv",

index=False

)

print("Transactions:",len(transactions))


# ---------- DEMOGRAPHICS ----------

demo=pd.DataFrame({

"customer_id":

np.arange(1,customers+1),

"age":

np.random.randint(

22,70,

customers

),

"income":

np.random.normal(

60000,

20000,

customers

),

"employment_years":

np.random.randint(

1,

30,

customers

)

})


demo.to_csv(

"customer_demographics.csv",

index=False

)

print("Demographics created")


# ---------- RISK ----------

risk=pd.DataFrame({

"customer_id":

np.arange(1,customers+1),

"credit_score":

np.random.randint(

400,

850,

customers

),

"loan_exposure":

np.random.gamma(

3,

6000,

customers

),

"late_payments":

np.random.randint(

0,

10,

customers

)

})


risk.to_csv(

"credit_risk.csv",

index=False

)

print("Risk table created")

print("DONE.")
