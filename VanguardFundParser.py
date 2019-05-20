
import csv
from selenium import webdriver

# settings
download= False

# quarter end performance report
data= csv.reader(open('temp_files/ProductDetailsHoldings_500_Index_' \
        + 'Fund_Admiral_Shares.csv'))
# data= csv.reader(open('QuarterendperformanceNAVView.csv'))
# from Vanguard.com --> Investments -> List of Vanguard Products

# read the column names from the first non-singleton line of the file
fields= data.next()

# the first few lines might contain metadata, which we don't care about here...
# luckily the metadata is usually less than two elements so we can parse it out
while len(fields) <= 2:
    fields= data.next()

##### DEBUG
print fields

# # correct blank field
# fields[1]= "Type"

##### DEBUG
print len(fields)

# list of stocks
stocks= []

# loop over rows in data file
for row in data:
    
    # Vanguard loves to stuff CSVs with useless lines; ignore them
    if len(row) == len(fields):
        
        # zip together the field names and values
        items= zip(fields, row)
        item= {}

        # add the value to the dictionsary
        for (name, value) in items:
            item[name]= value.strip()    
        
        # add stock to list of stocks
        stocks.append(item)
    
# checksum for accuracy
pct_sum= 0

# loop over stocks
for stock in stocks:

    print "%5s\t%-36.36s" % (stock["Ticker"], stock["Holding name"])
    
    pct_sum+= float(stock["% of fund*"])
    
print "Total percentage: %f" % pct_sum

