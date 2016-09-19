import os
stocks = open('stocks_copy.txt')
stock_data = stocks.read().split('\n')
current_dir = os.path.dirname(__file__)
print current_dir
for stock in stock_data:
    top_name = "%s_Top.csv" % (stock)
    rising_name = "%s_Rising.csv" % (stock)
    with open('New_Data/' + top_name, "w") as outfile:
        outfile.write("Year,Top_Search,Score,Ticker")
        outfile.write('\n')
        for year in xrange(2004, 2014):
            get = "%s_%s_top.csv" % (stock, year)
            folder = "Stock_Data/%s/top/" % (stock)
            with open(folder + get, 'rb') as infile:
                year_data = infile.read().split('\n')
                for line in year_data:
                    if line != '':
                        outfile.write("%s," % (year))
                        outfile.write(line)
                        outfile.write(",%s" % (stock))
                        outfile.write('\n')
