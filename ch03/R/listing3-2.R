setwd("~/Documents/DataDrivenSecurity-Excercises/ch03")

# URL for the AlienVault IP Reputation Database (OSSIM format)
# storing the URL in a variable makes it easier to modify later
# if it changes. NOTE: we are using a specific version of the data 
# in these examples, so we are pulling it from an alternate
# book-specific location.
avURL <- "http://datadrivensecurity.info/book/ch03/data/reputation.data"

# use relative path for the downloaded data
avRep <- "data/reputation2.data"

# using an if{}-wrapped test with download.file() vs read.xxx() 
# directly avoids having to re-download a 16MB file every time 
# we run the script
if (file.access(avRep)) {download.file(avURL, avRep)}

# read in the IP reputation db into a data frame
# this data file has no header, so set header=FALSE 
av <- read.csv(avRep,sep="#", header=FALSE)
# assign more readable column names since we didn't pick 
# any up from the header
colnames(av) <- c("IP", "Reliability", "Risk", "Type", "Country", "Locale", "Coords", "x")

str(av) # get an overview of the data frame

