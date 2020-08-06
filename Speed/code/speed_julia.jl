using Statistics
using DataFrames
using CSV
using GZip

# Define functions

uncompressed() = CSV.read("crsp_daily")

function processing()
	R = by(data, [:year, :PERMNO]) do data
		DataFrame(m = mean(data.RET), s = std(data.RET), c = length(data.RET))
	end
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
