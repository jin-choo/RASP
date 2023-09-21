BinSizes = [0.015 0.025 0.04 0.06 0.085 0.15 0.25];
MaxLags = max(ceil(0.1 ./ BinSizes), 3);

alphs = [0.01];
% RecordingTimes = [1500 1000 500 300 200 100 50 30 20 10];
RecordingTimes = [1000 500 100 50 10];
NIDsMotifNeuronsNumbers = ["10000505", "05000505", "03000505", "02000505"];  % "1000505" "0750505" "0250505" "0500305" "0500405" "0500605" "0500705"
bgMtPpTjTws = ["2.00.405.001000" "2.00.201.000000"];
%"2.00.201.010000" "2.00.201.005000" "2.00.201.003000" "2.00.201.002000" "2.00.201.001000" "2.00.204.000000" "2.00.203.000000" "2.00.202.000000" "2.00.401.000000" "2.00.101.000000" "2.00.051.000000" "2.00.201.000000"
%"2.00.203.003000" "2.00.304.002000" "2.00.405.001000"
%"2.00.405.001000" "2.00.201.000000"
MotifTypeMotifMaxs = ["2100000"];  %"3100003" "2100000" "1000000"
seeds = [2 1 0];
Table = cartesian(alphs, RecordingTimes, NIDsMotifNeuronsNumbers, bgMtPpTjTws, MotifTypeMotifMaxs, seeds);

starttime = now;
for iMotifType=1:length(MotifTypeMotifMaxs)
    MotifTypeMotifMax = char(MotifTypeMotifMaxs(iMotifType));
    MotifType = str2double(MotifTypeMotifMax(1));
    fileID = fopen(sprintf('/home/dmlab/hyunjin/brainimage/cad_stat5/%d_time_%s.csv', MotifType, datestr(starttime, 'mm.dd_HH.MM')),'w');
    fprintf(fileID, 'type,nids,time,bgRate,pp,tj,tw,mtRate,mtNeuron,mtNumber,mtMaxLag,mtMaxSpikes,bin,maxLag,alpha,k,time,seed\n');
    fclose(fileID);
end

parfor iTable=1:height(Table)
    alph = Table{iTable, 1};
    RecordingTime = Table{iTable, 2};
    NIDMotifNeuronsNumber = char(Table{iTable, 3});
    NID = str2double(NIDMotifNeuronsNumber(1:4));
    MotifNeuron = str2double(NIDMotifNeuronsNumber(5:6));
    MotifNumber = str2double(NIDMotifNeuronsNumber(7:8));
    bgMtPpTjTw = char(Table{iTable, 4});
    BGFiringRate = str2double(bgMtPpTjTw(1:3));
    MTFiringRate = str2double(bgMtPpTjTw(4:7));
    pp = str2double(bgMtPpTjTw(8:10));
    tj = str2double(bgMtPpTjTw(11:13));
    tw = str2double(bgMtPpTjTw(14:15));
    MotifTypeMotifMax = char(Table{iTable, 5});
    MotifType = str2double(MotifTypeMotifMax(1));
    MotifMaxLag = str2double(MotifTypeMotifMax(2:4));
    MotifMaxSpi = str2double(MotifTypeMotifMax(5:7));
    seed = Table{iTable, 6};
        
    mat = load(sprintf("/home/dmlab/hyunjin/brainimage/generated_data/%d_NIDs_%d_time_%d_bg_%.2f_pp_%.1f_tj_%d_tw_%d_mt_%.2f_%d_%d_%d_%d_seed_%d.mat", MotifType, NID, RecordingTime, BGFiringRate, pp, tj, tw, MTFiringRate, MotifNeuron, MotifNumber, MotifMaxLag, MotifMaxSpi, seed));
    outputprint = sprintf("%d,%d,%d,%.2f,%.1f,%d,%d,%.2f,%d,%d,%d,%d", MotifType, NID, RecordingTime, BGFiringRate, pp, tj, tw, MTFiringRate, MotifNeuron, MotifNumber, MotifMaxLag, MotifMaxSpi);
    MotifTypeprint = sprintf("/home/dmlab/hyunjin/brainimage/cad_stat5/%d_time_%s.csv", MotifType, datestr(starttime, 'mm.dd_HH.MM'));
        
    [assembly]=Main_assemblies_detection_gt(mat.gt,MaxLags,BinSizes,[],alph,[],MotifNeuron,[],outputprint,MotifTypeprint,RecordingTime,seed);
    try
        [As_across_bins,As_across_bins_index]=assemblies_across_bins(assembly,BinSizes);
        for jj=1:length(BinSizes)
            int=BinSizes(jj);
            assemblybin = {};
            assemblybin_index = 1;
            for ii=1:length(As_across_bins)
                if As_across_bins{ii}.bin <= int
                    assemblybin(1, assemblybin_index) = {As_across_bins{ii}};
                    assemblybin_index = assemblybin_index + 1;
                end
            end
            fname = sprintf("/home/dmlab/hyunjin/brainimage/cad_stat5/%d/%d_NIDs_%d_time_%d_bg_%.2f_pp_%.1f_tj_%d_tw_%d_mt_%.2f_%d_%d_%d_%d_bin_%d_lag_%d_alpha_%.2f_%d_seed_%d.mat", MotifType, MotifType, NID, RecordingTime, BGFiringRate, pp, tj, tw, MTFiringRate, MotifNeuron, MotifNumber, MotifMaxLag, MotifMaxSpi, int * 1000, MaxLags(jj), alph, MotifNeuron, seed);
            parsave(fname,assemblybin);
        end
    catch
    end
end

function parsave(fname,aus)
    save(fname,'aus','-v7.3')
end