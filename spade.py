import neo, numpy as np, quantities as pq, matplotlib.pyplot as plt, yaml  #, elephant.conversion as conv
from elephant.spade import spade, concepts_mining, _build_context, pvalue_spectrum
from itertools import combinations, permutations
from sklearn import metrics
from SimulMotif.motif_gen import *
from tqdm import tqdm
# from elephant.spike_train_generation import compound_poisson_process
# from viziphant.rasterplot import eventplot, rasterplot_rates
# from viziphant.events import add_event
# from viziphant.spade import plot_patterns, plot_patterns_statistics

def itemset_to_number(max_neuron: int, k_tuple: int, itemset: list):
    return sum((itemset[k] - 1) * pow(max_neuron, k_tuple - 1 - k) for k in range(k_tuple))

def itemset_tuple_to_number(max_neuron: int, k_tuple: int, itemset: tuple):
    return sum((itemset[k] - 1) * pow(max_neuron, k_tuple - 1 - k) for k in range(k_tuple))

def spade_read(k_tuples: int, file_path: str, winlen:int, probabilistic_participation: int):
    # np.random.seed(1)
    # spiketrains = compound_poisson_process(rate=2*pq.Hz, amplitude_distribution=[0, 0.95, 0, 0, 0, 0, 0.05], t_stop=5*pq.s)
    # print(spiketrains)

    # activity_list = []
    # for i_activity, line in enumerate(open(f'{file_path}.txt', 'r')):
    #     # if i_activity >= 5000:
    #     #     break
    #     activity_list_i = np.where(np.array(list(map(int, line.strip().split(',')))) == 1)[0] + 1  # spiking neurons
    #     for spiking_neuron in activity_list_i:
    #         try:
    #             activity_list[spiking_neuron - 1].append(i_activity / 100)
    #         except:
    #             len_activity_list = len(activity_list)
    #             for i in range(spiking_neuron - len_activity_list):
    #                 activity_list.append([])
    #             activity_list[spiking_neuron - 1].append(i_activity / 100)
    # spiketrains = [neo.core.SpikeTrain(activity_list_i*pq.s, t_stop=500*pq.s) for activity_list_i in activity_list]

    # fig, axes = plt.subplots(2, 1, sharex=True, sharey='row')
    # #event = neo.Event([0.5, 8]*pq.s, labels=['trig0', 'trig1'])
    # eventplot(spiketrains, histogram_bins=5000, linelengths=0.75, linewidths=1)
    # #eventplot(spiketrains, linelengths=0.75, linewidths=1)
    # #add_event(axes[:, 0], event)
    # plt.savefig(f"./figure/spade/spiketrains_eventplot.png", bbox_inches='tight')
    # rasterplot_rates(spiketrains)
    # plt.savefig(f"./figure/spade/spiketrains_rasterplot.png", bbox_inches='tight')

    # concepts_mining(spiketrains, bin_size=10*pq.ms, winlen=30, min_occ=1, min_neu=2)[0]

    # context, transactions, rel_matrix = _build_context(conv.BinnedSpikeTrain(spiketrains, bin_size=10*pq.ms, tolerance=None).to_sparse_bool_array().tocoo(copy=False), 10)
    # pv_spec = pvalue_spectrum(spiketrains, bin_size=10*pq.ms, winlen=30, dither=5*pq.ms, n_surr=100)
    # print(pv_spec)

    bin_size = 10

    if file_path[:2] == 'gt':
        # Load simulation parameters
        with open("params.yaml") as f:
            params = yaml.load(f, Loader=yaml.FullLoader)

        if probabilistic_participation > 1:
            params["noise"]["probabilistic_participation"] = 1 - 1 / probabilistic_participation

        # Genereate non-motif activity
        # spike_time: list containing every spikes
        # spike_time_motif: list containing spikes induced by motifs
        spike_time, spike_time_motif = non_motif_gen(params, seed=0)

        motif_type = int(file_path[-1])
        # Generate motif activity
        gts = motif_gen(spike_time, spike_time_motif, motif_type, params, seed=motif_type)

        motif_neuron = []
        motif_neuron_num = []
        for gt in gts:
            NIDs = gt['NIDs'] + 1
            motif_neuron.append(NIDs)
            NIDs_size = NIDs.size
            motif_neuron_num.append(NIDs_size)

        motif_neuron = np.array(motif_neuron, dtype=object)
        motif_neuron_num = np.array(motif_neuron_num)

        recording_time = params["recording"]["recording_time"]
        spiketrains = [neo.core.SpikeTrain(np.clip(np.array(x) * 1000, 0, recording_time * 1000) * pq.ms, units='ms', t_stop=recording_time * 1000 * pq.ms) for x in spike_time]

        dithering = 15

        patterns = spade(spiketrains, bin_size=bin_size*pq.ms, winlen=winlen, min_occ=1, min_neu=2, alpha=1, n_surr=50, dither=dithering*pq.ms, output_format='patterns')['patterns']  #, psr_param=[0, 2, 0]

        max_neuron = params["NIDs"]

        # axes = plot_patterns(spiketrains, patterns)
        # plt.savefig(f"./figure/spade/spiketrains_spade_{dithering}.png", bbox_inches='tight')
        # plot_patterns_statistics(patterns)
        # plt.savefig(f"./figure/spade/spiketrains_spade_{dithering}_stat.png", bbox_inches='tight')

        for k_tuple in tqdm(range(1, k_tuples)):
            itemset_number_list = []
            support_list = []
            pvalue_list = []
            for pattern in patterns:
                support = pattern['signature'][1]
                pvalue = pattern['pvalue']
                for combination in combinations(range(pattern['signature'][0]), k_tuple + 1):
                    itemset = [pattern['neurons'][combination_] + 1 for combination_ in combination]
                    itemset_number = itemset_to_number(max_neuron, k_tuple + 1, itemset)
                    itemset_number_list.append(itemset_number)
                    support_list.append(support)
                    pvalue_list.append(pvalue)

            motif_neuron_k = motif_neuron[motif_neuron_num > k_tuple]
            condition_positive_set = [set(itemset_tuple_to_number(max_neuron, k_tuple + 1, condition_positive_tuple) for condition_positive_tuple in permutations(motif_neuron_k_combination)) for motif_neuron_k_i in motif_neuron_k for motif_neuron_k_combination in combinations(motif_neuron_k_i, k_tuple + 1)]
            condition_positive = len(condition_positive_set)

            condition_negative_set = set(itemset_number_list) - set(itemset_tuple_to_number(max_neuron, k_tuple + 1, motif_neuron_k_permutation) for i, motif_neuron_k_i in enumerate(motif_neuron_k) for motif_neuron_k_permutation in permutations(motif_neuron_k_i, k_tuple + 1))
            condition_negative = len(condition_negative_set)

            fpr = [1]
            tpr = [1]
            f = open(f"./txt/spade/{file_path}_{winlen}_{probabilistic_participation}_{k_tuple + 1}_support_acc.txt", 'w')
            f.write(f"threshold, recall, precision, f1_score\n")

            enumerate_support_list = enumerate(support_list)
            for threshold in np.unique(support_list):
                enumerate_support_list = [(support_index, support) for support_index, support in enumerate_support_list if support >= threshold]
                threshold_tuple_set = set(itemset_number_list[support_index] for support_index, support in enumerate_support_list)
                true_positive = 0
                for condition_positive_set_ in condition_positive_set:
                    if any(condition_positive_tuple in threshold_tuple_set for condition_positive_tuple in condition_positive_set_):
                        true_positive += 1
                false_positive = len(threshold_tuple_set & condition_negative_set)
                fpr.append(false_positive / condition_negative)
                tpr_value = true_positive / condition_positive
                tpr.append(tpr_value)
                try:
                    precision = 1 - false_positive / len(threshold_tuple_set)
                    f.write(f"{threshold}, {tpr_value}, {precision}, {2 * precision * tpr_value / (precision + tpr_value)}\n")
                except:
                    precision = 0
                    f.write(f"{threshold}, {tpr_value}, {precision}, 0\n")
                    pass

            fpr.append(0)
            tpr.append(0)
            auroc = metrics.auc(fpr, tpr)
            f.write(f"auroc, {auroc}")
            f.close()

            plt.figure(figsize=(6.5, 5.5))
            plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (area = {auroc:.2f})')
            plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
            plt.tick_params(axis='both', labelsize=15)
            plt.xlabel('False Positive Rate', fontsize=23)
            plt.ylabel('True Positive Rate', fontsize=23)
            plt.title(f"{k_tuple + 1}-Tuple Count ROC Curve", fontsize=23)
            plt.legend(fontsize=15)
            plt.savefig(f"./figure/spade/{file_path}/{file_path}_{winlen}_{probabilistic_participation}_{k_tuple + 1}_support.png", bbox_inches='tight')
            plt.close()

            fpr = [1]
            tpr = [1]
            f = open(f"./txt/spade/{file_path}_{winlen}_{probabilistic_participation}_{k_tuple + 1}_pvalue_acc.txt", 'w')
            f.write(f"threshold, recall, precision, f1_score\n")

            enumerate_pvalue_list = enumerate(pvalue_list)
            for threshold in np.unique(pvalue_list)[::-1]:
                enumerate_pvalue_list = [(pvalue_index, pvalue) for pvalue_index, pvalue in enumerate_pvalue_list if pvalue <= threshold]
                threshold_tuple_set = set(itemset_number_list[pvalue_index] for pvalue_index, pvalue in enumerate_pvalue_list)
                true_positive = 0
                for condition_positive_set_ in condition_positive_set:
                    if any(condition_positive_tuple in threshold_tuple_set for condition_positive_tuple in condition_positive_set_):
                        true_positive += 1
                false_positive = len(threshold_tuple_set & condition_negative_set)
                fpr.append(false_positive / condition_negative)
                tpr_value = true_positive / condition_positive
                tpr.append(tpr_value)
                try:
                    precision = 1 - false_positive / len(threshold_tuple_set)
                    f.write(f"{threshold}, {tpr_value}, {precision}, {2 * precision * tpr_value / (precision + tpr_value)}\n")
                except:
                    precision = 0
                    f.write(f"{threshold}, {tpr_value}, {precision}, 0\n")
                    pass

            fpr.append(0)
            tpr.append(0)
            auroc = metrics.auc(fpr, tpr)
            f.close()

            plt.figure(figsize=(6.5, 5.5))
            plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (area = {auroc:.2f})')
            plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
            plt.tick_params(axis='both', labelsize=15)
            plt.xlabel('False Positive Rate', fontsize=23)
            plt.ylabel('True Positive Rate', fontsize=23)
            plt.title(f"{k_tuple + 1}-Tuple Count ROC Curve", fontsize=23)
            plt.legend(fontsize=15)
            plt.savefig(f"./figure/spade/{file_path}/{file_path}_{winlen}_{probabilistic_participation}_{k_tuple + 1}_pvalue.png", bbox_inches='tight')
            plt.close()


        # for dithering in [20, 30]:
        #     patterns = spade(spiketrains, bin_size=bin_size*pq.ms, winlen=winlen, min_occ=1, min_neu=2, alpha=1, n_surr=100, dither=dithering*pq.ms, output_format='patterns')['patterns']  #, psr_param=[0, 2, 0]
        #
        #     # axes = plot_patterns(spiketrains, patterns)
        #     # plt.savefig(f"./figure/spade/spiketrains_spade_{dithering}.png", bbox_inches='tight')
        #     # plot_patterns_statistics(patterns)
        #     # plt.savefig(f"./figure/spade/spiketrains_spade_{dithering}_stat.png", bbox_inches='tight')
        #
        #     for k_tuple in range(1, k_tuples):
        #         # itemset_index_dict = dict()
        #         # itemset_index = 0
        #         itemset_number_list = []
        #         pvalue_list = []
        #         for pattern in patterns:
        #             # lags = np.insert(pattern['lags'].magnitude / bin_size, 0, 0)
        #             pvalue = pattern['pvalue']
        #             for combination in combinations(range(pattern['signature'][0]), k_tuple + 1):
        #                 itemset = [pattern['neurons'][combination_] + 1 for combination_ in combination]
        #                 itemset_number = itemset_to_number(max_neuron, k_tuple + 1, itemset)
        #                 itemset_number_list.append(itemset_number)
        #                 # interneuron = [lags[combination[i_combination + 1]] - lags[combination[i_combination]] for i_combination in range(len(combination) - 1)]
        #                 # itemset_index_dict[itemset_interneuron_to_number(max_neuron, k_tuple + 1, itemset, winlen, interneuron)] = itemset_index
        #                 # itemset_index += 1
        #                 pvalue_list.append(pvalue)
        #
        #         motif_neuron_k = motif_neuron[motif_neuron_num > k_tuple]
        #         condition_positive_set = set(motif_neuron_k_combination for i, motif_neuron_k_i in enumerate(motif_neuron_k) for motif_neuron_k_combination in combinations(motif_neuron_k_i, k_tuple + 1))
        #         condition_positive = len(condition_positive_set)
        #
        #         condition_negative_set = set(itemset_number_list) - set(itemset_tuple_to_number(max_neuron, k_tuple + 1, motif_neuron_k_permutation) for i, motif_neuron_k_i in enumerate(motif_neuron_k) for motif_neuron_k_permutation in permutations(motif_neuron_k_i, k_tuple + 1))
        #         condition_negative = len(condition_negative_set)
        #
        #         fpr = []
        #         tpr = []
        #         f = open(f"./txt/spade/{file_path}_{winlen}_{probabilistic_participation}_{k_tuple + 1}_pvalue_acc.txt", 'w')
        #         f.write(f"threshold, recall, precision, f1_score\n")
        #
        #         enumerate_pvalue_list = enumerate(pvalue_list)
        #         for threshold in np.unique(pvalue_list)[::-1]:
        #             enumerate_pvalue_list = [(pvalue_index, pvalue) for pvalue_index, pvalue in enumerate_pvalue_list if pvalue <= threshold]
        #             threshold_tuple_set = set(itemset_number_list[pvalue_index] for pvalue_index, pvalue in enumerate_pvalue_list)
        #             true_positive = 0
        #             for condition_positive_tuple in condition_positive_set:
        #                 for condition_positive_tuple_permutations in permutations(condition_positive_tuple):
        #                     if itemset_tuple_to_number(max_neuron, k_tuple + 1, condition_positive_tuple_permutations) in threshold_tuple_set:
        #                         true_positive += 1
        #                         break
        #             false_positive = len(threshold_tuple_set & condition_negative_set)
        #             fpr.append(false_positive / condition_negative)
        #             tpr_value = true_positive / condition_positive
        #             tpr.append(tpr_value)
        #             try:
        #                 precision = 1 - false_positive / len(threshold_tuple_set)
        #                 f.write(f"{threshold}, {tpr_value}, {precision}, {2 * precision * tpr_value / (precision + tpr_value)}\n")
        #             except:
        #                 precision = 0
        #                 f.write(f"{threshold}, {tpr_value}, {precision}, 0\n")
        #                 pass
        #         auroc = metrics.auc(fpr, tpr)
        #         f.write(f"auroc, {auroc}")
        #         f.close()
        #
        #         plt.figure(figsize=(6.5, 5.5))
        #         plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (area = {auroc:.2f})')
        #         plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
        #         plt.tick_params(axis='both', labelsize=15)
        #         plt.xlabel('False Positive Rate', fontsize=23)
        #         plt.ylabel('True Positive Rate', fontsize=23)
        #         plt.title(f"{k_tuple + 1}-Tuple Count ROC Curve", fontsize=23)
        #         plt.legend(fontsize=15)
        #         plt.savefig(f"./figure/spade/{file_path}_{winlen}_{probabilistic_participation}_{k_tuple + 1}_pvalue.png")
        #         plt.close()