
# Speed -------------------------------------------------------------------

library(svglite)
library(data.table)
library(RColorBrewer)
col_wb <- '#F6F7EB'
co <- brewer.pal(7, "Set1")[2]
co2 <- brewer.pal(7, "Set1")[1]

data <- fread("../code/x.csv")
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
  par(bg=NA, col.axis = col_wb, col.lab = col_wb, col.main = col_wb, col.sub = col_wb)
  x <- barplot(dt$Median, names.arg = dt$language, main = title, yaxt = "n", 
               col = co, ylim = c(0,ceiling(max(dt$Median, na.rm = TRUE))), border = F)
  axis(2, seq(0,ceiling(max(dt$Median, na.rm = TRUE))), las = 1)
  text(x, dt$Median + 0.1, labels = format(round(dt$Median,2), nsmall = 2), col = col_wb)
  if (is.na(dt$Median[length(dt$Median)])) text(x[length(x)], 1.5, "Matlab \n cannot \n read \n compressed \n files", srt=0, col = col_wb)
}

# Plotting both running times
loading <- rbind(R[operation == "read_uncompressed", c("language", "Median")][order(language)]$Median,
                 R[operation == "read_compressed", c("language","Median")][order(language)]$Median)
loading <- loading/min(loading, na.rm = TRUE)
rownames(loading) <- c("Uncompressed", "Compressed")
colnames(loading) <- sort(unique(R$language))
loading <- loading[,names(sort(loading[1,]))]

plot_two <- function(){
  par(mar = c(2,2,2,0))
  par(bg=NA, col.axis = col_wb, col.lab = col_wb, col.main = col_wb, col.sub = col_wb)
  x <- barplot(loading, main = "Loading time relative to fastest", yaxt = "n", beside = TRUE,
               col = c(co,co2), ylim = c(0,ceiling(max(loading, na.rm = TRUE))), border = F)
  axis(2, seq(0,ceiling(max(loading, na.rm = TRUE))), las = 1)
  text(x, loading + 0.1, labels = format(round(loading,2), nsmall = 2), col = col_wb)
  legend("topleft", col = c(co, co2), legend = c("Uncompressed", "Compressed"),
         pch = 15, bty = "n", text.col = col_wb)
  if (is.na(loading["Compressed", "Matlab"])) text(x[length(x)]+0.2, 2, "Matlab \n cannot \n read \n compressed \n files", srt=0, cex = 0.8, col = col_wb)
} 


# GARCH -------------------------------------------------------------------

garch <- fread("../garch/x.csv")
garch$time <- garch$time/min(garch$time)
garch <- garch[order(time), c("language", "time")]
garch$language <- c("C", "Rcpp", "Numba", "Julia", "Matlab", "R", "Python")

plot_garch <- function() {
  par(mar = c(2.5,3.5,2,0))
  par(bg=NA, col.axis = col_wb, col.lab = col_wb, col.main = col_wb, col.sub = col_wb)
  x <- barplot(garch$time, names.arg = garch$language,  log = "y",
               col = co, border = F, yaxt = "n", las = 1, ylim = c(0.5, 500),
               main = "Calculation of GARCH log likelihood \n Relative to C")
  offset <- rep(0.1,length(garch$time))
  offset[length(garch$time)] <- 0
  text(x-offset, garch$time*1.2, labels = format(round(garch$time,2), nsmall = 2), col = col_wb)
  Ticks<-c(1,2,5,10, 20, 50, 100, 250, 500)
  axis(2,at = Ticks, las = 1)
}

# Saving ------------------------------------------------------------------


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
    units = "px", pointsize = 12)
plot_two()
dev.off()

png("png_small/garch.png", width = wid, height = hei,
    units = "px", pointsize = 12)
plot_garch()
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

png("png_large/garch.png", width = wid*2, height = hei*2,
    units = "px", pointsize = 20)
plot_garch()
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

svglite("svg/garch.svg")
plot_garch()
dev.off()


