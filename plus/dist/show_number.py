import gc
gc.collect()

from microbit import display

def show_bin(bin_string, row_index):
    bin_string = '' + '0' * (5 - len(bin_string)) + bin_string
    for col in range(5):
        display.set_pixel(col, row_index, int(bin_string[col]) * 9)
    

def show_number(n):
    n = int(n)
    if n < 0:
        return
    
    string = '' + '0' * (3 - len(str(n)))
    string += str(n)
    print('string', n, string)
    c, d, u = [int(x) for x in string]
    cbin, dbin, ubin = [str(bin(x)).split('0b')[1] for x in [c,d,u]]
    
    for row, bin_string in enumerate([cbin, dbin, ubin]):
        show_bin(bin_string, row)