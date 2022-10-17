### DB server (local)
# db_username = 'root'
# db_password = '1234'
# db_host = '127.0.0.1'
# charset = 'utf-8'

### DB server (Igugana) 
db_username = 'iguana'
db_password = 'mlmobiis!'
db_host = '192.168.100.189'
charset = 'utf-8'

db_name = 'MTV'
#db_tb = 'junetest' #TODO virus_index

### eSearch variable
mail_address = 'gubon119@mobiis.com'
db_type = "protein"
keyword_virus = "viruses"
date_type = "PDAT"

data_size = 1000 ### retmax (10,000 까지 괜찮은 듯)

### Data info
index_column = ['GBSeq_locus', 'GBSeq_length', 'GBSeq_topology', 'GBSeq_division', 'GBSeq_update-date', 'GBSeq_create-date',
                'GBSeq_definition', 'GBSeq_accession-version', 'GBSeq_source', 'GBSeq_organism', 'GBSeq_taxonomy',  'GBSeq_sequence']
index_coulumn_name = ['locus', 'length', 'topology', 'division', 'date_modified', 'date_published',
                        'definition', 'accession_version', 'source', 'organism', 'taxonomy',  'sequence']
index_sep = ','

### outout file
folder_path = './mtv_test/'
