BinSizes = [2.0 3.0 5.0 10.0 15.0 20.0 30.0 60.0];
MaxLags = max(ceil(600.0 ./ BinSizes), 3);

alphs = [0.01];
Times = [86400];
ItemsLength = ["1003"];
Table = cartesian(alphs, Times, ItemsLength);

starttime = now;
fileID = fopen(sprintf('/home/dmlab/hyunjin/brainimage/cad_stat3/yoochoose-clicks_crop_time_%s.csv', datestr(starttime, 'mm.dd_HH.MM')),'w');
fprintf(fileID, 'time,item,length,bin,maxLag,alpha,k,time\n');
fclose(fileID);

parfor iTable=1:height(Table)
    alph = Table{iTable, 1};
    Time = Table{iTable, 2};
    ItemLength = char(Table{iTable, 3});
    Item = str2double(ItemLength(1:3));
    Length = str2double(ItemLength(4:4));
        
    mat = load(sprintf("/home/dmlab/hyunjin/brainimage/generated_data/yoochoose-clicks_crop_time_%d_item_%d.mat", Time, Item));
    outputprint = sprintf("%d,%d,%d", Time, Item, Length);
    MotifTypeprint = sprintf("/home/dmlab/hyunjin/brainimage/cad_stat3/yoochoose-clicks_crop_time_%s.csv", datestr(starttime, 'mm.dd_HH.MM'));
        
    [assembly]=Main_assemblies_detection_real(mat.gt,MaxLags,BinSizes,[],alph,[],Length,[],outputprint,MotifTypeprint);
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
            fname = sprintf("/data/hyunjin/brainimage/cad_stat3/yoochoose-clicks_crop_time_%d_item_%d_length_%d_bin_%d_lag_%d_alpha_%.2f.mat", Time, Item, Length, int, MaxLags(jj), alph);
            parsave(fname,assemblybin);
        end
    catch
    end
end

function parsave(fname,aus)
    save(fname,'aus','-v7.3')
end