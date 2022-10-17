import os
import pymysql
import sqlalchemy
from sqlalchemy import Table, Column, Text, DateTime
from sqlalchemy_utils import database_exists, create_database
from Bio import Entrez
from dateutil.parser import parse
import time

import a_global_variable as a_var
#import jellyfish

# Prevent Error : Python http.client.Incomplete Read(0 bytes read) error
import http.client
http.client.HTTPConnection._http_vsn = 10
http.client.HTTPConnection._http_vsn_str = 'HTTP/1.0'

### get_start_point
# Input 
#   - text : Content of download_info.txt file.
# Output : Latest start point for crawling
def get_start_point(text):
    text.readline()
    line = text.readline()
    lists = line.split("\t")
    return int(lists[2]) + int(lists[5])

def get_accessCode(start_point, date_start, date_end):
    Entrez.email = a_var.mail_address
    search = Entrez.esearch(db=a_var.db_type,
                            term=a_var.keyword_virus,
                            Retmax=a_var.data_size,
                            Retmode="xml",
                            mindate=date_start,
                            maxdate=date_end,
                            datetype=a_var.date_type,
                            Retstart=start_point)
    record = Entrez.read(search)

    print("[get_accessCode] read ", flush=True)
    return record


def fetch_record_xml(record):
    # time.sleep(5)
    Entrez.email = a_var.mail_address
    handle = Entrez.efetch(db=a_var.db_type,
                           id=record["IdList"],
                           rettype="gb",
                           retmode="xml",
                           retmax=a_var.data_size)
    records = Entrez.read(handle)
    
    print("[fetch_record_xml] read ", flush=True)
    return records


### connect_db
# input :
#   db_name, table_name
#   ( Use global variable : db_username, db_password, db_host, charset )
# output :
#   engine.connect()
def connect_db(db_name):
    pymysql.install_as_MySQLdb()

    engine = sqlalchemy.create_engine('mysql+pymysql://{0}:{1}@{2}/{3}?{4}'.format(
        a_var.db_username, a_var.db_password, a_var.db_host, db_name, a_var.charset))

    if not database_exists(engine.url):
        create_database(engine.url)

    db_conn = engine.connect()
    meta = sqlalchemy.MetaData()

    """
    print("[DB] Create Table ...", flush = True)
    query = "show tables like '{0}'".format(table_name)
    result = db_conn.execute(query)
    exist_table = result.fetchall()

    if exist_table:
        print("exist!!!", flush=True)
    else:
        print("not exist!!!", flush=True)
        virus_table = Table(
                    table_name, meta,
                    Column("protein_name", Text),
                    Column("country", Text),
                    Column("date", DateTime),
                    Column("definition", Text),
                    Column("accession_version", sqlalchemy.CHAR(100), primary_key=True),
                    Column("organism", Text),
                    Column("taxonomy", Text),
                    Column("sequence", Text),
        )
        meta.create_all(engine)

    db_table = sqlalchemy.Table(table_name, meta, autoload=True, autoload_with=engine)
    """
    if db_conn.closed:  # check_connect_db(db_conn)==False
        print('[connect_db] ' + db_name + ' connection failed.', flush=True)
        return()
    else:
        print('[connect_db] ' + db_name + ' connection established. ', flush=True)
        return db_conn

### insert_data
# input :
#   - conn : pymysql's engine.connect()
#   - table : sqlalchemy.Table
#   - rows : target data for inserting
def insert_data(conn, table, rows):
    rows.append("NULL")
    query = sqlalchemy.insert(table).values(rows).prefix_with('IGNORE')
    result_proxy = conn.execute(query)
    result_proxy.close()

### get_protein
###    - Selecting target viruses
###    - target Viruses : influenza(Alpha, Beta, Gamma, Delta), Corona(Alpha, Beta, Gamma, Delta)
# input :
#   - definition_data : definition column in MutaVi DB.
#   - virus_type : target virus for selecting (influenza or corona)
# output :
#   - protein name
#      - influena : "hemagglutinin", "haemagglutinin", "ion channel", "neuraminidase"
#      - corona : "membrane", "envelope", "spike", "surface"
def get_protein(definition_data, virus_type):
    corona_name = ["membrane", "envelope", "spike", "surface"]
    influe_name = ["hemagglutinin", "haemagglutinin", "ion channel", "neuraminidase"] #ion channel은 바로 문자열 포함으로 탐색할 것

    #string list
    
    ### checking partial ###
    ### execpt word
    # partial, small, product, structural, putative,  truncated, 
    # accessory, multispanning, peptide, precursor, subunit, s1, s2
    # esterase, Chain, ha1, ha2, h5, Nonapeptide
    # tri-stalk, domain, incomplete,  Epitope, tran, like
    except_word = ["partial", "small", "product", "structural", "putative",  "truncated", \
                    "accessory", "multispanning", "peptide", "precursor", "subunit", "s1", \
                    "s2", "3c", "esterase", "chain", "ha1", "ha2", "h5", "tri-stalk", "domain", "incomplete",  "epitope", "tran", "like", "residues"]
    except_check = False
    for execpt_val in except_word:
        if execpt_val in definition_data.lower():
            except_check = True
            break
    if except_check:
        return ""
    else:
        if "-" in definition_data:
            defini_split = definition_data.lower().split("-")
        else:
            defini_split = definition_data.lower().split(" ")
        
        if virus_type == "corona":
            if corona_name[0] in defini_split:
                return corona_name[0]
            elif  "m" in defini_split:
                return corona_name[0]
            elif corona_name[1] in defini_split:
                return corona_name[1]
            elif "e" in defini_split:
                return corona_name[1]
            elif corona_name[2] in defini_split:
                return corona_name[2]
            elif corona_name[3] in defini_split:
                return corona_name[2]
            elif "s" in defini_split:
                return corona_name[2]
        elif virus_type == "influenza":
            if influe_name[0] in defini_split:
                return influe_name[0]
            elif influe_name[1] in defini_split:
                return influe_name[0]
            elif "ha" in defini_split:
                return influe_name[0]
            elif influe_name[2] in definition_data.lower():
                return influe_name[2]
            elif "m2" in defini_split:
                return influe_name[2]
            elif influe_name[3] in defini_split:
                return influe_name[3]
            elif "na" in defini_split:
                return influe_name[3]
    return ""

### get_featureData
# input :
#   - AScode : accession code
# output :
#   - feature data
def get_featureData(AScode):
    year = 2010
    feature_path = "../dataset/2021_renewal/"
    
    while True:
        if year > 2021:
            break
        #filepath = feature_path + str(year) + "/" + AScode
        filepath = feature_path + AScode
        if os.path.isfile(filepath):
            f = open(filepath, 'r')
            line = f.readline()
            return line
        else:
            year += 1
    
    print("Not -> ", filepath)
    return ""

### get_local
def get_local(feature_data):
    dict_list = eval(feature_data)
    local_data = "NULL"
    for f_dict in dict_list:
        if f_dict["GBFeature_key"] == "source":
            anno_list = f_dict["GBFeature_quals"]
            for anno_dict in anno_list:
                if anno_dict["GBQualifier_name"] == "country":
                    split_data = anno_dict["GBQualifier_value"].split(":")
                    if len(split_data) > 1:
                        local_data = split_data[0]
                    else:
                        local_data = anno_dict["GBQualifier_value"]
                    break
    return local_data


### get_date
def get_date(feature_data):
    dict_list = eval(feature_data)
    date_data = "NULL"
    for f_dict in dict_list:
        if f_dict["GBFeature_key"] == "source":
            anno_list = f_dict["GBFeature_quals"]
            for anno_dict in anno_list:
                if anno_dict["GBQualifier_name"] == "collection_date":
                    parse_date = parse(anno_dict["GBQualifier_value"])
                    if len(anno_dict["GBQualifier_value"]) <= 4:
                        date_data = parse_date.year
                    else:
                        date_data = parse_date.date()

                    """
                    split_data = anno_dict["GBQualifier_value"].split("-")
                    if len(split_data) < 2:
                        date_data = anno_dict["GBQualifier_value"]
                    elif len(split_data[0]) == 4:
                        date_data = f"{split_data[0]}-{split_data[1]}"
                    elif len(split_data) == 3 and len(split_data[2]) == 4:
                        date_data = f"{split_data[2]}-{split_data[1]}"
                    else:
                        date_data = anno_dict["GBQualifier_value"]
                    """
                    break
    
    return date_data

### get_organism
###     - when not have organism data, get organism data in feature data. 
# input :
#   - feature_data : feature data
# output:
#   - organism data
def get_organism(feature_data):
    dict_list = eval(feature_data)
    strain_data = ""
    serotype_data = ""
    for f_dict in dict_list:
        if f_dict["GBFeature_key"] == "source":
            anno_list = f_dict["GBFeature_quals"]
            for anno_dict in anno_list:
                if anno_dict["GBQualifier_name"] == "strain":
                    strain_data = anno_dict["GBQualifier_value"]
                if anno_dict["GBQualifier_name"] == "serotype":
                    serotype_data = anno_dict["GBQualifier_value"]
    return strain_data, serotype_data


