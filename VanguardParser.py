
import csv
from selenium import webdriver

# settings
download= False

# quarter end performance report
data= csv.reader(open('SymbolsandholdingsView.csv'))
# data= csv.reader(open('QuarterendperformanceNAVView.csv'))
# from Vanguard.com --> Investments -> List of Vanguard Products

# read the column names from the first line of the file
fields= data.next()

# ##### DEBUG
# print fields

# correct blank field
fields[1]= "Type"

# ##### DEBUG
# print len(fields)

# list of funds
funds= []

# cycle over rows in data
for row in data:
    
    # ##### DEBUG
    # print len(row)

    # Vanguard loves to stuff CSVs with useless lines; ignore them
    if len(row) == len(fields):
        
        # zip together the field names and values
        items= zip(fields, row)
        item= {}
        
        # add the value to the dictionsary
        for (name, value) in items:
            item[name]= value.strip()
        
        # add new fund to list of funds
        funds.append(item)

# specify save locations for files
path_save= "/Users/coryfrontin/Documents/Python/Investing/temp_files"
profile= webdriver.FirefoxProfile()
profile.set_preference('browser.download.folderList', 2)    # custom location
profile.set_preference('browser.download.manager.showWhenStarting',
        False)
profile.set_preference('browser.download.dir', path_save)
profile.set_preference('browser.download.downloadDir', path_save)

# fire up webdriver, tell it to wait for load before actions
br= webdriver.Firefox(profile)
br.implicitly_wait(1000)

# print output data
print "Now downloading data for the funds:\n\n"
print "%-12s%72.72s\t%-4s" % ("#", "Fund name", "Fund No.")

fund_counter= 0
fund_downloads= 0
fund_derps= 0

# loop over the funds and print the name
for fund in funds:
    
    fund_counter+= 1

    # print portfolio data
    print "%3.3d of %3.3d: %72.72s\t%-4s\t%-10s" \
            % (fund_counter, len(funds), fund["Name"],
                    fund["Fund number"], fund["Symbol"])
    
    # cook up URL for dataset
    # this is coming from deconstructing one of Vanguard's pages, such as:
    # https://advisors.vanguard.com/VGApp/iip/site/advisor/investments/portfoliodetails?fundId=0870
    prefix= "ProductDetailsHoldings_"       # a prefix. who knows why
    name= prefix + fund["Name"].replace(" ", "_")
    
    if download:

        try:
            
            # for each fund get its portfolio details page
            url_portfoliodetails_prefix= ("https://advisors.vanguard.com/"
                    + "VGApp/iip/site/advisor/investments/portfoliodetails" + 
                    "?fundId=")
            url_portfoliodetails_suffix= "&compositionTabBox=1#hold"
            url_portfoliodetails= url_portfoliodetails_prefix \
                    + fund["Fund number"] + url_portfoliodetails_suffix
            
            # open that page
            br.get(url_portfoliodetails)
            
            # click the download button
            br.find_element_by_id('portfolioForm:compTabBox' 
                    + ':downloadHoldings').click()
            
            # # run the javascript executable we want
            # argstr= "fasAdobe.adobeTrack.events.track('" + name
            #     + "','CSV');"
            # # argstr= ("adobeTracker('" + prefix + "', '" + fund["Name"]
            #     + "', this);")
            # 
            # ##### DEBUG
            # print "\tExecuting javascript: %s" % argstr
            # 
            # br.execute_script(argstr)
            
            fund_downloads+= 1

        except:

            # didn't work
            print "Fund download failed..."
            
            fund_derps+= 1

# # print the first fund for validation
# print funds[0]

# close up shop
br.close()

# print final numbers
print ""
print "Total number of funds:\t\t%d" % fund_counter
print "Number of funds downloaded:\t%d" % fund_downloads
print "Funds that failed to download:\t%d" % fund_derps

