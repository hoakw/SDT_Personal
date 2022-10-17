from datetime import date
import streamlit as st
import pandas as pd
import numpy as np
import time

from sqlalchemy_utils.functions.database import has_index
import json
import requests
import pymysql
import sqlalchemy
from sqlalchemy_utils import database_exists, create_database


#import a_global_variable as a_var
#import b_function_common as b_fun

class Calculation():

    def connect_db(self, db_name):
        pymysql.install_as_MySQLdb()
        engine = sqlalchemy.create_engine(
            "mysql+pymysql://{0}:{1}@{2}/{3}?{4}".format(
                "iguana", "mlmobiis!", "192.168.100.189", db_name, "utf-8"
            )
        )

        if not database_exists(engine.url):
            create_database(engine.url)

        db_conn = engine.connect()

        if db_conn.closed:
            print(f"[connect_db] {db_name} connection failed.", flush=True)
            return False
        else:
            return db_conn

    def kfserving(self, auth_key, target_gene, target_sequence, target_spacer, target_case):
        
        #print(f"Key = {auth_key}")
        h_header = {
            "Cookie": f"authservice_session={auth_key}", 
            "Host": "gene-kfserving.gene.example.com",
        }
        url_name = "http://192.168.100.186:30890/v1/models/gene-kfserving:predict"

        h_data = {
            'gene': target_gene,
            'sequence': target_sequence,
            'spacer' : target_spacer,
            'case': target_case
        }

        result = requests.post(url_name, headers=h_header, data=json.dumps(h_data)).json()
        result_df = pd.DataFrame(result)

        return result_df

    @st.cache
    def get_case_one(self, target_gene):
        start = time.time()
        db_name = "gnscs_web"
        tb_name = "AB"

        #result_df = self.kfserving()
        db_conn = self.connect_db(db_name)

        #target_gene = "RPL3"

        query = str(
            f"SELECT *  FROM `{db_name}`.`total_ngg_{tb_name}` WHERE LOWER(CONVERT(`Target_Gene` USING utf8mb4)) LIKE '{target_gene}' ;"
        )
        result_df = pd.read_sql(query, db_conn)
        print(f"[Case1] Finish!!! {time.time() - start}", flush=True)
        return result_df
    
    @st.cache
    def get_case_two(self, target_sequence):
        start = time.time()
        db_name = "gnscs_web"
        tb_name = "backward_ngg"
        db_conn = self.connect_db(db_name)

        #target_sequence = "GTGGTCTTTCTCTTGCTGTGGGG"

        query = str(
            f"SELECT *  FROM `{db_name}`.`{tb_name}` WHERE LOWER(CONVERT(`Target` USING utf8mb4)) LIKE '{target_sequence}' ;"
        )
        result_df = pd.read_sql(query, db_conn)
        print(f"[Case2] Finish!!! {time.time() - start}", flush=True)

        return result_df

    @st.cache
    def get_case_three(self, target_gene, target_sequence):
        db_name = "crispr_onoff"
        tb_name = "total_df_input"
        db_conn = self.connect_db(db_name)

        target_gene = "RPL3"
        target_sequence = "TGCCTGCTGCTGCGCTTCCG"

        query = str(
            f"SELECT Target_Gene, SPACER, TARGET, y_h  FROM `{db_name}`.`{tb_name}` WHERE LOWER(CONVERT(`Target` USING utf8mb4)) LIKE '{target_sequence}' AND LOWER(CONVERT(`Target_Gene` USING utf8mb4)) LIKE '{target_gene}' ;"
        )
        result_df = pd.read_sql(query, db_conn)

        return result_df
    