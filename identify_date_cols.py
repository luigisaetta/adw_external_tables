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

def identify_dates(df):

    print('*** List of possible columns of type: DATE, DATETIME')
    print()

    # get list of columns
    l_columns = list(df.columns)
    
    # needed to handle last comma (not to be printed)
    n_columns = len(l_columns)
    
    for i in range(n_columns):
        column = l_columns[i]
        
        # column names changed to uppercase
        if 'datetime' in str(df[column].dtype):
            print(column)
    print()
    return

def check_params():
    '''
    expect file_name, table_name
    return True if two params available
    '''
    n_params = len(sys.argv)

    if n_params > 1:
        return True
    else:
        return False

def print_usage():
    print()
    print('Not enough parameters found...')
    print()
    print('Usage: python identify_date_cols.py <file_name>')
    print('')

def info():
    print('Running with:') 
    print('file name: %s ' %(FILE_NAME))

    print()

if __name__ == "__main__":
    
    # check if command line parameters passed
    if(check_params()):
        # file name passed as first params
        FILE_NAME = sys.argv[1]
    else:
        print_usage()
        sys.exit(-1)

    print()

    info()

    # read from csv file in DataFrame
    my_df = pd.read_csv(FILE_NAME, sep=',' , nrows=MAX_ROWS)

    print('Visualizing first rows...')
    print()
    print(my_df.head(5))
    print()

    # questa linea di codice prova ad identificare le colonne di tipo date (ma potrebbe fallire per alcuni formati)
    my_df = my_df.apply(lambda col: pd.to_datetime(col, errors='ignore') 
              if col.dtypes == object 
              else col, 
              axis=0)
    
    identify_dates(my_df)

