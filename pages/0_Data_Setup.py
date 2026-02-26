import streamlit as st
import os
import pandas as pd
import sys


# ---------- FIX IMPORT PATH ----------

BASE_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        ".."
    )
)

sys.path.append(BASE_DIR)

from util.load_data import load_tables


st.title("🏦 Banking Demo — Data Setup")


st.markdown("""

This demo simulates EDW ingestion:

• Transactions → Core Banking Activity

• Demographics → Customer Master

• Risk → Bureau Exposure

""")


DATA_PATH=os.path.join(
BASE_DIR,
"data"
)


# --------------------
# SHOW FILES
# --------------------

if "show" not in st.session_state:

    st.session_state.show=False


if st.button("📂 Show Data Files"):

    st.session_state.show=True



if st.session_state.show:

    files=[

        f for f in os.listdir(DATA_PATH)

        if f.endswith(".csv")

    ]


    col1,col2=st.columns([1,2])


    with col1:

        st.subheader("Files")

        for f in files:

            size=os.path.getsize(

                os.path.join(DATA_PATH,f)

            )/1024/1024

            st.write(
                f"✅ {f} — {size:.2f} MB"
            )


    with col2:

        selected=st.selectbox(
            "Preview dataset",
            files
        )

        df=pd.read_csv(

            os.path.join(
                DATA_PATH,
                selected
            ),

            nrows=100
        )

        st.dataframe(
            df,
            use_container_width=True
        )


# --------------------
# LOAD SECTION
# --------------------

st.divider()

st.subheader("Load Into Teradata")


host=st.text_input("Host")

user=st.text_input("User")

password=st.text_input(
"Password",
type="password"
)


progress=st.progress(0)

status=st.empty()


def update_progress(value,table):

    progress.progress(value)

    status.write(
        f"Loading {table}"
    )

progress_bar=st.progress(0)

status=st.empty()



def update_progress(value,message):

    progress_bar.progress(value)

    status.write(message)



if st.button("🚀 Load Data Into Teradata"):

    with st.spinner("Uploading tables..."):

        load_tables(

            host,

            user,

            password,

            update_progress

        )

    st.success(
        "Tables Loaded Successfully!"
    )


