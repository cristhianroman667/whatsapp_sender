import re
import urllib.parse
import pandas as pd

__all__ = ['message', 'read_csv']

def _print_columns(columns):
    basics = ['nombre', 'celular']
    for basic in basics:
        if basic not in columns:
            raise ValueError("There is no '%s' column" % basic)

    print("You have the following columns:\n\t", list(columns))

def message(row, text):
    pattern = r'\$\{([0-9a-z]{1,})\}'
    
    while re.search(pattern, text):
        col = re.search(pattern, text).group(1)
        if col not in row.index:
            raise ValueError("There is no column %s" % col)
        
        text = re.sub(pattern, row[col], text, count=1)
        
    return urllib.parse.quote(text)

def read_csv(filename):
    df = pd.read_csv(filename)
    df.columns = [x.lower() for x in df.columns]
    _print_columns(df.columns)
    return df