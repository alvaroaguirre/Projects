using Statistics
using DataFrames
using CSV
using GZip

# Define functions

compressed() = GZip.open("crsp_daily.gz","r") do io
                 CSV.read(io)
               end

# Loading - Compressed

load_comp = @elapsed data = compressed();
println("output,Julia,read_compressed,", load_comp)
