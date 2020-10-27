## Utility for easy handling of ADWH external tables

26/10/2020

With this utility you can read a csv file and generate the DDL to create an Oracle external table
enabling to access the file, stored in OCI Object Storage, from Oracle Autonomous ADWH

If you want to use this utility locally, you must have a Python environment with Pandas installed
 
Then usage is:

python generate_ddl.py file.csv <table_name>

the DDL is printed on standard output.

#### This is an example of the output:

File name is:  movies.csv

Generating DDL for table:  MOVIES_EXT

BEGIN
 	DBMS_CLOUD.CREATE_EXTERNAL_TABLE(
		table_name =>'MOVIES_EXT',
		credential_name =>'ADWH2',
		file_uri_list =>'https://objectstorage.eu-frankfurt-1.oraclecloud.com/n/emease/b/datalake_in/o/movies.csv',
		format => json_object('type' value 'csv', 'skipheaders' value '1'),
		column_list => '
		MOVIEID NUMBER,
		TITLE VARCHAR2(2000),
		GENRES VARCHAR2(2000)
		'
	); 
END; 
/



