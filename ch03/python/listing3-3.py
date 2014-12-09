# URL for the AlienVault IP Reputation Database (OSSIM format)
# storing the URL in a variable makes it easier to modify later
# if it changes. NOTE: we are using a specific version of the data 
# in these examples, so we are pulling it from an alternate
# book-specific location.
import urllib
import os.path

avURL = "http://datadrivensecurity.info/book/ch03/data/reputation.data"

# relative path for the downloaded data
avRep = "data/reputation.data"

# using an if-wrapped test with urllib.urlretrieve() vs direct read 
# via panads avoids having to re-download a 16MB file every time we 
# run the script
if not os.path.isfile(avRep):
      urllib.urlretrieve(avURL, filename=avRep)
      
# first time using the pandas library so we need to import it
import pandas as pd
import sys

# read in the data into a pandas data frame
av = pd.read_csv(avRep,sep="#")

# make smarter column names
av.columns = ["IP","Reliability","Risk","Type","Country", "Locale","Coords","x"]
print(av) # take a quick look at the data structure

# take a look at the first 10 rows
print av.head().to_csv(sys.stdout)


# require object: av (3-5)
# See corresponding output in Figure 3-1
# import the capability to display Python objects as formatted HTML 
from IPython.display import HTML
# display the first 10 lines of the dataframe as formatted HTML 
print 
HTML(av.head(10).to_html())