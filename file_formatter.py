import os
stocks = open('stocks_copy.txt')
stock_data = stocks.read().split('\n')
current_dir = os.path.dirname(__file__)
print current_dir

with open('New_Data/Top_Data.csv', "w") as outfile:
    outfile.write("Year,Top_Search,Score,Ticker")
    outfile.write('\n')
    for stock in stock_data:
        for year in xrange(2004, 2014):
            get = "%s_%s_top.csv" % (stock, year)
            folder = "Stock_Data/%s/top/" % (stock)
            try:
                with open(folder + get, 'rb') as infile:
                    year_data = infile.read().split('\n')
                    for line in year_data:
                        if line != '':
                            outfile.write("%s," % (year))
                            outfile.write(line)
                            outfile.write(",%s" % (stock))
                            outfile.write('\n')
            except IOError:
                print "%s not found" % (get)

with open('New_Data/Rising_Data.csv', "w") as outfile:
    outfile.write("Year,Rising_Search,Score,Ticker")
    outfile.write('\n')
    for stock in stock_data:
        for year in xrange(2004, 2014):
            get = "%s_%s_rising.csv" % (stock, year)
            folder = "Stock_Data/%s/rising/" % (stock)
            try:
                with open(folder + get, 'rb') as infile:
                    year_data = infile.read().split('\n')
                    for line in year_data:
                        if line != '':
                            outfile.write("%s," % (year))
                            data = line.split(',')
                            if len(data) > 2:
                                if data[-2][0] == '+':
                                    temp = data[-2] + data[-1]
                                    data[-2] = temp
                                    del data[-1]
                                    if len(data) > 2:
                                        other_temp = ''
                                        for i in xrange(0, len(data) - 1):
                                            other_temp += data[i]
                                        data[0] = other_temp
                                        data = [data[0], data[-1]]

                            outfile.write(','.join(data))
                            outfile.write(",%s" % (stock))
                            outfile.write('\n')
            except IOError:
                a =  "%s not found" % (get)
