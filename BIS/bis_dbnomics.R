options(warn = -1)

cat("Checking if packages installed...", "\n")
pkg <- c("zoo", "lubridate", "rdbnomics", "countrycode")

installed <- pkg %in% installed.packages()[,1]
invisible(sapply(pkg[installed], suppressWarnings(suppressMessages(library)), character.only = TRUE))
if (sum(!installed) > 0) {
  cat("There are", sum(!installed), "packages not installed:", pkg[!installed])
  inst <- readline(prompt = "Install needed packages? [y/n]:")
  if (inst == "y") {
    invisible(sapply(pkg[!installed], suppressMessages(install.packages), character.only = TRUE))
    invisible(sapply(pkg[!installed], suppressWarnings(suppressMessages(library)), character.only = TRUE))
  } else {
    stop("bis_dbnomics requires the packages to be installed")
  }
} 



bis_dbnomics <- function(country, sector = "All issuers", international = "Y", currency = "USD") {
  country = countrycode(country, origin = "country.name", destination = "iso2c")
  if (sector == "All issuers") sec = "1"
  if (sector == "Central bank") sec = "7"
  if (sector == "Financial corporations") sec = "B"
  if (sector == "General government") sec = "2"
  if (sector == "International institutions") sec = "S"
  if (sector == "Non-financial corporations") sec = "J"
  if (sector == "Private banks") sec = "E"
  if (sector == "Private other financial institutions") sec = "G"
  if (sector == "Public banks") sec = "I"
  if (sector == "Public other financial institutions") sec = "K"
  
  if (international == "Y") {
    int <- "C"
    cur_group <- "F"
  }
  if (international == "N") {int = "A"
  cur_group <- "A"
  currency <- "TO1"
  }
  code <- paste0("BIS/debtsec/Q.", country, ".3P.", sec, ".1.", 
                int, ".A.", cur_group, ".", currency, ".A.A.A.A.A.I")
  
  out <- rdb(ids = code)
  out <- out[,c("period", "value")]
  out$value <- out$value
  names(out) <- c("date",country)
  out$date <- as.yearqtr(out$date)
  return(out)
}

cat("####################### Function bis_dbnomics() #######################", "\n",
    "Arguments:", "\n",
    "         * country: Use country code (e.g. BR for Brazil)", "\n",
    "         * sector: Select from the following (default is All issuers):", "\n",
    "                   - All isuers", "\n",
    "                   - Central bank", "\n",
    "                   - Financial corporations", "\n",
    "                   - General government", "\n",
    "                   - International institutions", "\n",
    "                   - Non-financial corporations", "\n",
    "                   - Private banks", "\n",
    "                   - Private other financial institutions", "\n",
    "                   - Public banks", "\n",
    "                   - Public other financial institutions", "\n",
    "         * international: Y or N (default is Y)", "\n",
    "         * currency: foreign currency for international (default is USD)")
    
    
options(warn = 0)
    
