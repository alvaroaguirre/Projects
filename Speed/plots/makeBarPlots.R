library(svglite)
library(data.table)
library(RColorBrewer)
co <- brewer.pal(7, "Set1")[2]
co2 <- brewer.pal(7, "Set1")[1]

data <- fread("../speed/x.csv")
R <- data[,list(min(time), mean(time), median(time),
           max(time)), keyby = list(language, operation)]

cols <-  c("Min", "Mean", "Median", "Max")
colnames(R)[3:6] <- cols
R <- R[,(cols) := round(.SD,1), .SDcols=cols]
extra_row <- data.frame("Matlab", "read_compressed", NA, NA, NA, NA)
names(extra_row) <- names(R)
R <- rbind(R, extra_row)
R[order(operation, Median)]

compressed <- R[operation == "read_compressed", c("language", "Median")]
compressed$Median <- compressed$Median/min(compressed$Median, na.rm = TRUE)
compressed <- compressed[order(Median)]

uncompressed <- R[operation == "read_uncompressed", c("language", "Median")]
uncompressed$Median <- uncompressed$Median/min(uncompressed$Median, na.rm = TRUE)
uncompressed <- uncompressed[order(Median)]

process <- R[operation == "process", c("language", "Median")]
process$Median <- process$Median/min(process$Median, na.rm = TRUE)
process <- process[order(Median)]

plot_vox <- function(dt, title) {
  par(mar = c(2,2,2,0))
  x <- barplot(dt$Median, names.arg = dt$language, main = title, yaxt = "n", 
               col = co, ylim = c(0,ceiling(max(dt$Median, na.rm = TRUE))), border = F)
  axis(2, seq(0,ceiling(max(dt$Median, na.rm = TRUE))), las = 1)
  text(x, dt$Median + 0.1, labels = format(round(dt$Median,2), nsmall = 2))
  if (is.na(dt$Median[length(dt$Median)])) text(x[length(x)], 1.5, "Matlab \n cannot \n read \n compressed \n files", srt=0)
}

# Plotting both running times
loading <- R[operation %in% c("read_uncompressed", "read_compressed"), c("language", "operation", "Median")]
loading$Median <- loading$Median/min(loading$Median, na.rm = TRUE)
loading$language <- as.factor(loading$language)
desired_order <- c("R", "Python", "Julia", "Matlab")
loading$language <- factor(as.character(loading$language), levels = desired_order)
loading <- loading[order(language, Median)]

plot_two <- function(){
  par(mar = c(2,2,2,0))
  cols <- ifelse(loading$operation == "read_compressed", co, co2)
  x <- barplot(loading$Median, main = "Loading time relative to fastest", yaxt = "n", 
               col = cols, ylim = c(0,ceiling(max(loading$Median, na.rm = TRUE))), border = F)
  
  posit <- rep(NA,4)
  for(i in seq(1,4)){
    posit[i] <- mean(c(x[(i*2)-1], x[i*2]))
  }
  
  axis(1, posit, labels = unique(loading$language), tick = 0)
  axis(2, seq(0,ceiling(max(loading$Median, na.rm = TRUE))), las = 1)
  text(x, loading$Median + 0.1, labels = format(round(loading$Median,2), nsmall = 2))
  legend("topleft", col = c(co2, co), legend = c("Uncompressed", "Compressed"),
         pch = 15, bty = "n")
  if (is.na(loading$Median[length(loading$Median)])) text(x[length(x)], 2, "Matlab \n cannot \n read \n compressed \n files", srt=0)
}
plot_two()

# Parameters size
wid = 500
hei = 350

# Saving small png
png("png_small/uncompressed.png", width = wid, height = hei, 
    units = "px", pointsize = 14)
plot_vox(uncompressed, "Loading time relative to fastest - Uncompressed")
dev.off()

png("png_small/compressed.png", width = wid, height = hei,
    units = "px", pointsize = 14)
plot_vox(compressed, "Loading time relative to fastest - Compressed")
dev.off()

png("png_small/processing.png", width = wid, height = hei,
    units = "px", pointsize = 14)
plot_vox(process, paste("Annual mean and sd by year and firm", "\n", "Processing time relative to fastest"))
dev.off()

png("png_small/reading_time.png", width = wid, height = hei,
    units = "px", pointsize = 14)
plot_two()
dev.off()

# Large png
png("png_large/uncompressed.png", width = wid*2, height = hei*2,
    units = "px", pointsize = 20)
plot_vox(uncompressed, "Loading time relative to fastest - Uncompressed")
dev.off()

png("png_large/compressed.png", width = wid*2, height = hei*2,
    units = "px", pointsize = 20)
plot_vox(compressed, "Loading time relative to fastest - Compressed")
dev.off()

png("png_large/processing.png", width = wid*2, height = hei*2,
    units = "px", pointsize = 20)
plot_vox(process, paste("Annual mean and sd by year and firm", "\n", "Relative processing time"))
dev.off()

png("png_large/reading_time.png", width = wid*2, height = hei*2,
    units = "px", pointsize = 20)
plot_two()
dev.off()

# Svg
svglite("svg/uncompressed.svg")
plot_vox(uncompressed, "Loading time relative to fastest - Uncompressed")
dev.off()

svglite("svg/compressed.svg")
plot_vox(compressed, "Loading time relative to fastest - Compressed")
dev.off()

svglite("svg/processing.svg")
plot_vox(process, paste("Annual mean and sd by year and firm", "\n", "Relative processing time"))
dev.off()

svglite("svg/reading_time.svg")
plot_two()
dev.off()

