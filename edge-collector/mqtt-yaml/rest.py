import requests
import json
import pymysql
import sqlalchemy
import time
import pandas as pd
from sqlalchemy import Table, Column, Text
from sqlalchemy_utils import database_exists, create_database


url = "http://192.168.1.20:9443/sdt/default/test"
url_get = "http://127.0.0.1:8080/test"

headers = {
    "Content-Type": "application/json"
}

params = {
    "grant_type": "password",
    "username": "junesu@sdt.inc",
    "password": "Sdt251327!",
    "customerCode": "76U4-BE7I-Z3Z1"
}


params = {
    "namespace": "sklim"
}



data = json.dumps({
    "cmd": "ls /home"
})

data_rest = json.dumps({
    "edgemsg": "/home/sdt"
})
respeonse = requests.post(f"{url}", data=data)

print(respeonse.text, flush=True)


# db
pymysql.install_as_MySQLdb()
db_name = "edge_cmd"
engine = sqlalchemy.create_engine('mysql+pymysql://{0}:{1}@{2}/{3}?{4}'.format(
    "root", "root", "192.168.1.20:32355", "edge_cmd", "utf-8"))

if not database_exists(engine.url):
    create_database(engine.url)

db_conn = engine.connect()
meta = sqlalchemy.MetaData()

db_table = sqlalchemy.Table("cmd", meta, autoload=True, autoload_with=engine)

if db_conn.closed:  # check_connect_db(db_conn)==False
    print('[connect_db] ' + db_name + ' connection failed.', flush=True)
else:
    print('[connect_db] ' + db_name + ' connection established. ', flush=True)


query = str(f"SELECT *  FROM `{db_name}`.`cmd` where used like 0;")
result_df = pd.read_sql(query, db_conn)
time_out = 0
#print(result_df['used'][len(result_df) - 1])
while True:
    if len(result_df) != 0:
        print(result_df['result'][len(result_df) - 1])
        #query = str(f"UPDATE cmd SET used = 1 where used like 1;")
        #pd.read_sql(query, db_conn)
        break
    elif time_out > 10:
        break
    else:
        query = str(f"SELECT *  FROM `{db_name}`.`cmd` where used like 0;")
        result_df = pd.read_sql(query, db_conn)
        time_out = time_out + 1
    time.sleep(1)


