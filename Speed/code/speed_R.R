library(data.table)

colClasses=c(PERMNO="integer", date="integer", SHRCD="integer" ,EXCHCD="integer" 
             ,"TICKER"="character",  "COMNAM"="character",  "TRDSTAT"="character", "RET"="character")

# Loading - Uncompressed

start <- Sys.time()
data <- fread("crsp_daily", colClasses = colClasses)
load_uncomp <- difftime(Sys.time(), start, units = "secs")
cat("output,R,read_uncompressed,", load_uncomp, "\n", sep = "")

# Processing

suppressWarnings(data$RET <- as.numeric(data$RET))
data$y <- round(data$date/10000)
data <- data[!is.na(RET)]

start <- Sys.time()
R <- data[,list(length(RET), mean(RET), sd(RET)), keyby = list(y, PERMNO)]
processing_time <- difftime(Sys.time(), start, units = "secs")
cat("output,R,process,", processing_time, "\n", sep = "")
