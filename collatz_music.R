# Code that turns the first 200 integers' Collatz's stopping times into music and plays it

# install.packages("music")
library(music)

# Create system of notes
notes <- c("C", "C#", "D", "Eb", "E", "F", "F#", "G", "G#", "A", "Bb", "B")
allnotes <- character()
for (i in 3:8) {
  for (j in 1:length(notes)) {
    allnotes = c(allnotes, paste0(notes[j],i))
  }
}

# Adding Collatz numbers
collatz_stop <- function(N) {
  # Returns steps needed for the series to reach 1
  steps = 0
  while (N != 1) {
    if (N %% 2 == 0) {
      N = N/2
    } else {
      N = 3 * N + 1
    }
    steps = steps + 1
  }
  return(steps)
}

collatz <- numeric()
for (i in 2:200) {
  collatz[i-1] = collatz_stop(i)
}

length(unique(collatz))
keys <- sort(unique(collatz))
 
 # Transform collatz into notes
collatz_notes <- numeric()
 
for (i in 1:length(collatz)) {
   collatz_notes[i] <- allnotes[match(collatz[i], keys)]
 }
 
 # Create durations
 
 durations <- function(x) {
   tmp_seq <- sequence(rle(as.character(x))$lengths)
   tmp_new <- numeric()
   for (i in 1:length(tmp_seq)) {
     if (tmp_seq[i+1] != 1  & i < length(tmp_seq)) {
       tmp_new[i] <- NA
     } else {
       tmp_new[i] <- tmp_seq[i]
     }
   }
   music <- matrix(NA, nrow = length(x), ncol = 2)
   music[,1] <- x
   music[,2] <- tmp_new
   music <- music[which(!is.na(music[,2])),]
   return(music)
 }
 
# Get the matrix for Collatz
collatz_music <- durations(collatz_notes)
collatz_music

# Play it!
bpm <- 300
for (i in 1:dim(collatz_music)[1]) {
  playNote(collatz_music[i,1], duration = as.integer(collatz_music[i,2]), BPM = bpm)
  Sys.sleep(60*as.integer(collatz_music[i,2])/bpm)
}