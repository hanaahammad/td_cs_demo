import pandas as pd
import os

from teradataml import create_context
from teradataml.dataframe.copy_to import copy_to_sql
from teradataml import execute_sql

host="clustering-z764gzg9wzv5yhec.env.clearscape.teradata.com"
username="demo_user"
password="Loula@1126@habibti"

def drop_if_exists(table):

    try:

        execute_sql(
            f"DROP TABLE {table};"
        )

    except Exception:

        # ignore if table doesn't exist
        pass



def load_tables(

host,
username,
password,
progress_callback=None

):

    create_context(

        host=host,
        username=username,
        password=password

    )

    base_dir=os.path.abspath(

        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )

    data_path=os.path.join(
        base_dir,
        "data"
    )

    tables={

    "transactions.csv":"transactions",

    "customer_demographics.csv":
    "customer_demographics",

    "credit_risk.csv":
    "credit_risk"

    }


    total_tables=len(tables)

    table_index=0


    for file,table in tables.items():

        if progress_callback:

            progress_callback(
                0,
                f"Dropping {table}"
            )

        # ⭐ DROP TABLE
        drop_if_exists(table)


        filepath=os.path.join(
            data_path,
            file
        )


        total_rows=sum(
            1 for _ in open(filepath)
        )-1


        processed=0

        first=True


        # ⭐ STREAM CSV
        for chunk in pd.read_csv(

            filepath,
            chunksize=100000

        ):

            copy_to_sql(

                chunk,

                table_name=table,

                if_exists=
                "replace" if first
                else "append"

            )

            first=False

            processed+=len(chunk)


            # ⭐ PROGRESS %

            percent=(
                processed/total_rows
            )

            overall=(
                table_index+
                percent
            )/total_tables


            if progress_callback:

                progress_callback(

                    overall,

                    f"Loading {table} : {processed}/{total_rows}"

                )


        table_index+=1


    if progress_callback:

        progress_callback(
            1,
            "Completed"
        )
