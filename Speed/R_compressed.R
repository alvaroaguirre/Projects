library(data.table)

colClasses=c(PERMNO="integer", date="integer", SHRCD="integer" ,EXCHCD="integer" 
             ,"TICKER"="character",  "COMNAM"="character",  "TRDSTAT"="character", "RET"="character")

# Loading - compressed

start <- Sys.time()
data <- fread("crsp_daily.gz", colClasses = colClasses)
load_comp <- difftime(Sys.time(), start, units = "secs")
cat("output,R,read_compressed,", load_comp, "\n", sep = "")