% Loading - Uncompressed
tic
data = readtable('crsp_daily');
load_time = toc;
fprintf("output,Matlab,read_uncompressed," + load_time + "\n")

% Processing
data = data(~ismissing(data(:,'RET')),:);
data.year = round(data.date/10000);

tic
statarray = grpstats(data, {'PERMNO', 'year'}, {'mean', 'std'}, 'DataVars', 'RET');
process_time = toc;
fprintf("output,Matlab,process," + process_time + "\n")