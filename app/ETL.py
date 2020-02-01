#Importing data from CSVs to DB
import os, sys
import pymysql
import pandas as pd
import pathlib

#Parameters

host = 'localhost'
port = '3306'
db = 'issues'
user = 'jira'
password = 'jira'
DataPath = pathlib.Path('Data')

files = list(DataPath.glob('*.csv'))


def run_query(query, host, user, password, database = None ):
    '''
    This function load a csv file to MySQL table according to
    the query statement.
    '''
    try:
        con = pymysql.connect(host=host,
                                user=user,
                                password=password,
                                autocommit=True,
                                local_infile=1, database = database)
        print('Connected to DB: {}'.format(host))
        # Create cursor and execute Load SQL
        cursor = con.cursor()
        cursor.execute(query)
        print('query run succuessfully.')
        con.close()
        return cursor.fetchall()
       
    except Exception as e:
        print('Error: {}'.format(str(e)))
        sys.exit(1)


query = f"drop database if exists {db};"
run_query(query, host, user, password, database='')
query = f"create database {db};"
run_query(query, host, user, password, database='')


def remove_bom(path):
    """there is  \ufeff (Byte order mark) char in he beginning of all csvs. it must be removed
    otherwise instead of ID column there will be \ufeffID column"""
    #not very effecient, but simple
    # the change is made directly on file
    data = path.read_text(encoding='utf-8-sig')   
    path.write_text(data)

for file in files:
    table = str(file.stem)    
    filepath = str(file)     
    folder = str(file.parent)
    try:
       
        remove_bom(file)
        
        command =  f'csvsql --dialect mysql --snifflimit 100000 {filepath} > {folder}/{table}.sql'
        print('>>>' + command)
        os.system(command)
        
        create_query = pathlib.Path(f'{folder}/{table}.sql').read_text(encoding='utf-8-sig')
        print('>>>' + create_query)
        run_query(create_query, host, user, password, db)
      
        load_query = f"LOAD DATA LOCAL INFILE '{filepath}' INTO TABLE {db}.{table} FIELDS TERMINATED BY ',' ENCLOSED BY '\"' IGNORE 1 LINES;"
        print('>>>' + load_query)
        run_query(load_query, host, user, password, db)
        
    except :
        print('skipping' + f'{folder}/{table}.sql')
