using Statistics
using DataFrames
using CSV
using GZip

@time begin
        data = GZip.open("crsp_daily.gz","r") do io
                CSV.read(io)
        end
end

@time begin
        data = data[completecases(data),:];
        data.year = Int32.(round.(data.date/10000));
        data.RET = map(x -> (v = tryparse(Float64,x); isnothing(v) ? missing : v), data.RET);
        data = data[completecases(data),:];

        R = by(data, [:year, :PERMNO]) do data
                DataFrame(m = mean(data.RET),s = std(data.RET),c = length(data.RET))
        end
end