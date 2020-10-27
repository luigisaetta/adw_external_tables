import sys
import pandas as pd

# This is the dictionary of supported mappings
# (for now no DATE types)
dict_mappings = {}
dict_mappings['int32'] = 'NUMBER'
dict_mappings['int64'] = 'NUMBER'
dict_mappings['float32'] = 'NUMBER'
dict_mappings['float64'] = 'NUMBER'
dict_mappings['object'] = 'VARCHAR2(4000)'

#
# constants and parameters
#

# you should change here settings for your case
# for large files read from csv max_rows 
MAX_ROWS = 1000
# FILE_NAME can also be passed as command line param
FILE_NAME = 'test1.csv'

# This is the base_url for the region where the Object Storage bucket is
BASE_URL = 'https://objectstorage.eu-frankfurt-1.oraclecloud.com/n/'

# the name for the external table to be created
TABLE_NAME = 'TEST1_EXT'

# data for accessing Object Storage
NAMESPACE = 'emeaseitalyproxima'
BUCKET_NAME = 'datalake_in'
CREDENTIAL_NAME = 'ADWH2'

# for csv with delimiter ; you should add to format
# 'delimiter' value ';'

# end constant section

#
# functions
#

# function to generate ddl
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

# function to check params
def check_params():
    '''
    expect file_name, table_name
    return True if two params available
    '''
    n_params = len(sys.argv)

    if n_params > 2:
        return True
    else:
        return False

def print_usage():
    print()
    print('Not enough parameters found...')
    print()
    print('Usage: python generate_ddl.py <file_name> <table_name>')
    print('')

def info():
    print('Running with:') 
    print('file name: %s, table name: %s ' %(FILE_NAME, TABLE_NAME))
    print('Namespace: ', NAMESPACE)
    print('Bucket: ', BUCKET_NAME)
    print('Credential name: ', CREDENTIAL_NAME)

    print()

#
# main
#
if __name__ == "__main__":

    # check if command line parameters passed
    if(check_params()):
        # file name passed as first params
        FILE_NAME = sys.argv[1]
        TABLE_NAME = sys.argv[2]
    else:
        print_usage()
        sys.exit(-1)

    print()

    # print running info
    info()


    # read from csv file in DataFrame
    my_df = pd.read_csv(FILE_NAME, sep=';' , nrows=MAX_ROWS)

    print('Visualizing first rows...')
    print()
    print(my_df.head(5))
    print()

    generate_ddl(my_df)

    sys.exit(0)








