#workaround script to deal with the memory lack problem on small machines

mv Data/changegroup_changeitem.csv .

head -100000 changegroup_changeitem.csv  > Data/changegroup_changeitem.csv

cd app

python ETL.py 

cd ..

mv changegroup_changeitem.csv Data

usr=jira
pass=jira
db=issues

mysql -u$usr -p$pass -D$db -e "truncate table changegroup_changeitem;"

mysql -u$usr -p$pass -D$db -e "LOAD DATA LOCAL INFILE '/home/michael/Issues/Data/changegroup_changeitem.csv' INTO TABLE issues.changegroup_changeitem FIELDS TERMINATED BY ',' ENCLOSED BY '""' IGNORE 1 LINES;"

