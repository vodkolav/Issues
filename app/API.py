# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'

import os, sys
import pandas as pd
import pathlib
import mysql.connector
from datetime  import datetime 
from pprint import pprint


# Parameters

db = 'issues'
DataPath = './Data'

host = 'localhost'
user = 'jira'
password = 'jira'
port = '3306'

# files = pathlib.Path(DataPath)# + '/*.csv', recursive=False)
# list(files.glob('*.*'))




con = mysql.connector.connect(
      host=host,
      user=user,
      passwd=password,
      database=db
    )



def GetIssueAtTime(issueid, AtTime):

    # fetch all changes for given issue, before the given time
    # the descending order is principal for the correct work of loop below
    changes = pd.read_sql( f"""
    select * 
    from changegroup_changeitem 
    where issueid ={issueid} and CREATED < {AtTime}
    order by groupid desc; """,con)

    #fetch when the issue was last closed
    issueclosed = pd.read_sql(f"""select  CREATED
    from changegroup_changeitem 
    where issueid = {issueid} and FIELD = 'status' and NEWSTRING = 'Closed'
    ORDER by CREATED DESC 
    limit 1""", con)

    #fetch the issue
    issue = pd.read_sql(f"""
    select i.*, t.pname as issue_type 
    from jiraissue i
    join issuetype t on i.issuetype = t.ID 
    where i.ID = {issueid} """,con)
    
    now = pd.DataFrame(data=None, columns=changes.columns)
    req_fields = {'status':1, 'priority':1,'assignee':1,'reporter':1,'issuetype':1,'summary':1,'description':1}

    # go from latest change to ealiest and harvest (into 'now' variable) only the last change in each of the fields of interest
    for _, row in changes.iterrows():

        #if req_fields becomes empty before the loop end, then we've found all the interesting fields. no point continuing.
        if not req_fields:
            break
            
        if row.FIELD.lower() in req_fields:
            now = now.append(row)
            del req_fields[row.FIELD]

    result = {'created': issue.CREATED[0], 'closed':issueclosed.CREATED[0],'updated':now.CREATED.max()
              ,'summary':None, 'description':None, 'closed_date':issue.RESOLUTIONDATE[0], 'status':None, 
              'priority':None,'assignee':None,'reporter':None,'issuetype':issue.issue_type[0]}

    #put the harvested fields into dict for json serialization down the line
    for _, row in now.iterrows():
        result[row.FIELD] = row.NEWSTRING if not None else  row.NEWVALUE
    return result

