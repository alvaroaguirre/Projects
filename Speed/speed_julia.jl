using Statistics
using DataFrames
using CSV
using GZip

# Define functions

uncompressed() = CSV.read("crsp_daily")

function processing()
	gdf = groupby(data, [:PERMNO, :year]) 
	combine(gdf, [:RET => mean], [:RET => std], nrow)
end

# Loading - Uncompressed

load_uncomp = @elapsed data = uncompressed();
println("output,Julia,read_uncompressed,", load_uncomp)

# Processing

data = data[completecases(data),:];
data.year = Int32.(round.(data.date/10000));
data.RET = map(x -> (v = tryparse(Float64,x); isnothing(v) ? missing : v), data.RET);
data = data[completecases(data),:];

processing_time = @elapsed processing();
println("output,Julia,process,", processing_time)
