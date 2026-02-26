import streamlit as st

st.set_page_config(

    layout="wide",
    page_title="ClearScape ML Workbench",
    initial_sidebar_state="expanded"
)

st.title("🏦 ClearScape ML Workbench")

st.write("""

SQL In-Database ML + BYOM + Monitoring Demo

Workflow:

1. Data
2. Feature Engineering
3. SQL KMeans
4. BYOM DBSCAN
5. Deployment
6. Monitoring
7. Business Insights

""")
