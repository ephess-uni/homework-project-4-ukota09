# hp_4.py
#
from datetime import datetime, timedelta
from csv import DictReader, DictWriter
from collections import defaultdict

def reformat_dates(old_dates):
    """Accepts a list of date strings in format yyyy-mm-dd, re-formats each
    element to a format dd mmm yyyy--01 Jan 2001."""
    new_dates = list()
    formatstr = '%Y-%m-%d'
    for i in old_dates:
        start = datetime.strptime(i, formatstr)
        start = start.strftime('%d %b %Y')
        new_dates.append(str(start))
    return new_dates

def date_range(start, n):
    """For input date string `start`, with format 'yyyy-mm-dd', returns
    a list of of `n` datetime objects starting at `start` where each
    element in the list is one day after the previous."""
    if not isinstance(start, str):
        raise TypeError("Only string is valid input for start")
    if not isinstance(n, int):
        raise TypeError("Only int is valid input for n")
    added_dates = list()
    formatstr = "%Y-%m-%d"
    start = datetime.strptime(start, formatstr)
    for i in range(n):
        added_dates.append(start)
        start = start + timedelta(days=1)
    return added_dates

def add_date_range(values, start_date):
    """Adds a daily date range to the list `values` beginning with
    `start_date`.  The date, value pairs are returned as tuples
    in the returned list."""
    dates = date_range(start_date, len(values))
    con_dates = tuple(dates)
    con_values = tuple(values)
    return list(zip(con_dates, con_values))

def fees_report(infile, outfile):
    """Calculates late fees per patron id and writes a summary report to
    outfile."""
  
    with open(infile) as file:
        added_list=[]
        read_csv_obj = DictReader(file)
        for record in read_csv_obj:
            temp_dict={}
            late_fee_days=datetime.strptime(record['date_returned'],'%m/%d/%Y')- datetime.strptime(record['date_due'],'%m/%d/%Y') 
            if(late_fee_days.days>0):
                temp_dict["patron_id"]=record['patron_id']
                temp_dict["late_fees"]=round(late_fee_days.days*0.25, 2)
                added_list.append(temp_dict)
            else:
                temp_dict["patron_id"]=record['patron_id']
                temp_dict["late_fees"]=float(0)
                added_list.append(temp_dict)
                
        temp_dict_2 = {}
        for dict in added_list:
            key = (dict['patron_id'])
            temp_dict_2[key] = temp_dict_2.get(key, 0) + dict['late_fees']
        updated_list = [{'patron_id': key, 'late_fees': value} for key, value in temp_dict_2.items()]
        
        for dict in updated_list:
            for key,value in dict.items():
                if key == "late_fees":
                    if len(str(value).split('.')[-1]) != 2:
                        dict[key] = str(value)+"0"


   
    with open(outfile,"w", newline="") as file:
        col = ['patron_id', 'late_fees']
        writer = DictWriter(file, fieldnames=col)
        writer.writeheader()
        writer.writerows(updated_list)

# The following main selection block will only run when you choose
# "Run -> Module" in IDLE.  Use this section to run test code.  The
# template code below tests the fees_report function.
#
# Use the get_data_file_path function to get the full path of any file
# under the data directory.

if __name__ == '__main__':
   
    try:
        from src.util import get_data_file_path
    except ImportError:
        from util import get_data_file_path

    # BOOK_RETURNS_PATH = get_data_file_path('book_returns.csv')
    BOOK_RETURNS_PATH = get_data_file_path('book_returns_short.csv')

    OUTFILE = 'book_fees.csv'

    fees_report(BOOK_RETURNS_PATH, OUTFILE)

    # Print the data written to the outfile
    with open(OUTFILE) as f:
        print(f.read())
