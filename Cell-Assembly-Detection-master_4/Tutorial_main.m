%%%%%%%%%%%%%%%%%%%%%%%%%% TUTORIAL ON CELL ASSEMBLY DETECTION %%%%%%%%%%%%%%%%%%%%%%%%%

% LOAD DATA
load('C:\Users\Hyunjin\Desktop\20-brain-image\Cell-Assembly-Detection-master\Programs_and_data\test_data.mat');
spM = spM([1:15, 26:50],:);

starttime = now;
filepathprint = sprintf("C:/Users/Hyunjin/Desktop/20-brain-image/brainimage/cad_stat/cad_stat_time_%s.csv", datestr(starttime, 'mm.dd_HH.MM'));
fileID = fopen(filepathprint ,'w');
fprintf(fileID, 'RecordingTime,BinSize,alpha,k,RunningTime\n');
fclose(fileID);

BinSizes=[0.015 0.020];
MaxLags=[10 10];
RecordingTimes=[1400 1000 500];
alphs=[0.05 0.1 0.2];

% ASSEMBY DETECTION
for ll=1:length(RecordingTimes)
    RecordingTime=RecordingTimes(ll);
    spM(spM > RecordingTime) = NaN;
    for kk=1:length(alphs)
        alph = alphs(kk);
        for iO_th=2:5
            [assembly]=Main_assemblies_detection(spM,MaxLags,BinSizes,[],alph,[],iO_th,[],filepathprint,RecordingTime);
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
                fname = sprintf('C:/Users/Hyunjin/Desktop/20-brain-image/brainimage/cad_stat/%d_%d_%.2f_%d.mat', RecordingTime, int * 1000, alph, iO_th);
                parsave(fname,assemblybin);
            end
        end
    end
end

function parsave(fname,aus)
 save(fname,'aus','-v7.3')
end

% BinSizes=[0.015 0.020];
% MaxLags=[10 10];
% RecordingTime=1400;
% spM(spM > RecordingTime) = NaN;
% 
% O_th = 2;
% [assembly2]=Main_assemblies_detection(spM,MaxLags,BinSizes,[],[],[],O_th,[],filepathprint,RecordingTime);
% 
% O_th = 3;
% [assembly3]=Main_assemblies_detection(spM,MaxLags,BinSizes,[],[],[],O_th,[],filepathprint,RecordingTime);
% 
% O_th = 4;
% [assembly4]=Main_assemblies_detection(spM,MaxLags,BinSizes,[],[],[],O_th,[],filepathprint,RecordingTime);
% 
% O_th = 5;
% [assembly5]=Main_assemblies_detection(spM,MaxLags,BinSizes,[],[],[],O_th,[],filepathprint,RecordingTime);
% 
% [As_across_bins,As_across_bins_index]=assemblies_across_bins(assembly5,BinSizes);
% for jj=1:length(BinSizes)
%     int=BinSizes(jj);
%     assemblybin = {};
%     assemblybin_index = 1;
%     for ii=1:length(As_across_bins)
%         if As_across_bins{ii}.bin <= int
%             assemblybin(1, assemblybin_index) = {As_across_bins{ii}};
%             assemblybin_index = assemblybin_index + 1;
%         end
%     end
% end
% 
% assemblybin_load = load('C:/Users/Hyunjin/Desktop/20-brain-image/brainimage/cad/1400_15_0.05_5.mat').aus;

% %% %%%%%%%%%%%%%%%%%%%%%%%% VISUALIZATION %%%%%%%%%%%%%%%%%%%%%%%%
% nneu=size(spM,1);  % nneu is number of recorded units
% 
% % ASSEMBLY REORDERING
% [As_across_bins,As_across_bins_index]=assemblies_across_bins(assembly,BinSizes);
% 
% display='raw';
% % display='clustered';
% 
% % VISUALIZATION
% [Amatrix,Binvector,Unit_order,As_order]=assembly_assignment_matrix(As_across_bins, nneu, BinSizes, display);
% 
% %% %%%%%%%%%%%%%%%%%%%%%%%% PRUNING %%%%%%%%%%%%%%%%%%%%%%%%
% clf
% % PRUNING: criteria = 'biggest';
% criteria = 'biggest';
% [As_across_bins_pr,As_across_bins_index_pr]=pruning_across_bins(As_across_bins,As_across_bins_index,nneu,criteria);
% 
% display='raw';
% [Amatrix,Binvector,Unit_order,As_order]=assembly_assignment_matrix(As_across_bins_pr, nneu, BinSizes, display);
% 
% %%
% clf
% 
% % PRUNING: criteria = 'distance';
% criteria = 'distance';
% % th=0.7;
% th=0.3;
% 
% style='pvalue';
% % style='occ';
% 
% [As_across_bins_pr,As_across_bins_index_pr]=pruning_across_bins(As_across_bins,As_across_bins_index,nneu,criteria,th,style);
% display='raw';
% [Amatrix,Binvector,Unit_order,As_order]=assembly_assignment_matrix(As_across_bins_pr, nneu, BinSizes, display);
% 
% 
% %% %%%%%%%%%%%%%%%%%%%%%%%% ASSEMBLY ACTVATION %%%%%%%%%%%%%%%%%%%%%%%%
% clf
% 
% criteria = 'biggest';
% [As_across_bins_pr,As_across_bins_index_pr]=pruning_across_bins(As_across_bins,As_across_bins_index,nneu,criteria);
% 
% lagChoice = 'beginning';
% % lagChoice='duration';
% 
% act_count = 'full';
% [assembly_activity]=Assembly_activity_function(As_across_bins_pr,assembly,spM,BinSizes,lagChoice,act_count);
% 
% 
% for i=1:length(assembly_activity)
%     subplot(5,1,i)
%     plot(assembly_activity{i}(:,1),assembly_activity{i}(:,2));
%     hold on
% end