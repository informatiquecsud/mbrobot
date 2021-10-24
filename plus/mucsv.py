       
_default_sep = ';'

def csv_row(row, sep=None):
    sep = sep or _default_sep
    return sep.join([str(f) for f in row]) + '\n'

def set_default_sep(sep):
    global _default_sep
    _default_sep = sep

def write_data_to_csv(filename, data, headers=None, sep=None):
    sep = sep or _default_sep
    with open(filename, 'w') as csvfile:
        if headers:
            csvfile.write(csv_row(headers, sep))
            
        for row in data:
            if len(row) != len(headers):
                msg = "Row '{row}' does not contain as many elements as header '{header}'".format(
                    row=str(row), header=header)
                raise CSVRowError(msg)
            csvfile.write(csv_row(row, sep))
    