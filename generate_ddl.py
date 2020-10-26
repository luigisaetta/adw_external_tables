import sys
import pandas as pd

# This is the dictionary of supported mappings
dict_mappings = {}
dict_mappings['int32'] = 'NUMBER'
dict_mappings['int64'] = 'NUMBER'
dict_mappings['float32'] = 'NUMBER'
dict_mappings['float64'] = 'NUMBER'
dict_mappings['object'] = 'VARCHAR2(2000)'

#
# constants and parameters
#
FILE_NAME = 'movies.csv'

# This is the base_url for the region where the bucket is
BASE_URL = 'https://objectstorage.eu-frankfurt-1.oraclecloud.com/n/'

# the name for the external table
TABLE_NAME = 'MOVIES_EXT'

NAMESPACE = 'emease'
BUCKET_NAME = 'datalake_in'
CREDENTIAL_NAME = 'ADWH2'

# end constant sections

# functions

#
# function to generate ddl
#
def generate_ddl(df):
    '''
    df: Pandas DataFrame
    '''
    
    print('Generating DDL for table: ', TABLE_NAME)
    print()
    
    # const
    PART_INITIAL = "BEGIN\n \tDBMS_CLOUD.CREATE_EXTERNAL_TABLE("
    PART_END = "\t); \nEND; \n/"
    
    FORMAT_STRING = "format => json_object('type' value 'csv', 'skipheaders' value '1'),"
    FILE_URL = BASE_URL + NAMESPACE + '/b/' + BUCKET_NAME + '/o/' + FILE_NAME
    PART_TABLE_NAME = "table_name =>'" + TABLE_NAME + "',"
    PART_CREDENTIAL_NAME = "credential_name =>'" + CREDENTIAL_NAME + "',"
    PART_FILE_URI_LIST = "file_uri_list =>'" + FILE_URL + "',"
    
    # \t for pretty printing
    TAB2 = '\t\t'
    
    print(PART_INITIAL)
    print(TAB2 + PART_TABLE_NAME)
    print(TAB2 + PART_CREDENTIAL_NAME)
    print(TAB2 + PART_FILE_URI_LIST)
    print(TAB2 + FORMAT_STRING)
    
    # generate column list
    print(TAB2 + "column_list => '")
    
    # get list of columns
    l_columns = list(df.columns)
    
    # needed to handle last comma (not to be printed)
    n_columns = len(l_columns)
    COMMA = ","
    
    for i in range(n_columns):
        column = l_columns[i]
        
        # do not add last comma
        if i == n_columns - 1:
            COMMA = ""
        # column names changed to uppercase
        print(TAB2 + column.upper() + ' ' + dict_mappings[str(df[column].dtype)] + COMMA)
    
    # close column_list
    print(TAB2 + "'")
    
    # end of SQL
    print(PART_END)
    
    return

#
# main
#

# check if commad line parameters passed
n_params = len(sys.argv)
 
if(n_params > 1):
    # file name passed as params
    FILE_NAME = sys.argv[1]
else:
    print('Using internally defined file name!')
print()

print('File name is: ', FILE_NAME)

my_df = pd.read_csv(FILE_NAME, sep=',')

generate_ddl(my_df)







