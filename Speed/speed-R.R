library(data.table)

colClasses=c(PERMNO="integer", date="integer", SHRCD="integer" ,EXCHCD="integer" 
             ,"TICKER"="character",  "COMNAM"="character",  "TRDSTAT"="character", "RET"="character")

start <- Sys.time()
data <- fread("crsp_daily.gz", colClasses = colClasses)
cat("Loading:", "\n", difftime(Sys.time(), start, units = "secs"), "\n")


start <- Sys.time()

data$RET <- as.numeric(data$RET)
data$y <- round(data$date/10000)
data <- data[!is.na(RET)]
R = data[,list(length(RET), mean(RET), sd(RET)), keyby = list(y, PERMNO)]

cat("Processing:", "\n", difftime(Sys.time(), start, units = "secs"), "\n")
