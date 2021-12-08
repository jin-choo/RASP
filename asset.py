import neo, numpy as np, quantities as pq, matplotlib.pyplot as plt, yaml, os
from elephant import asset
from itertools import combinations, permutations
from sklearn import metrics
from SimulMotif.motif_gen import *
from tqdm import tqdm

def itemset_tuple_to_number(max_neuron: int, k_tuple: int, itemset: tuple):
    return sum((itemset[k] - 1) * pow(max_neuron, k_tuple - 1 - k) for k in range(k_tuple))

def asset_read(k_tuples: int, file_path: str, count_threshold: int, probabilistic_participation: int):
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

        recording_time = params["recording"]["recording_time"]
        spiketrains = [neo.core.SpikeTrain(np.clip(np.array(x) * 1000, 0, recording_time * 1000) * pq.ms, units='ms', t_stop=recording_time * 1000 * pq.ms) for x in spike_time]

        asset_obj = asset.ASSET(spiketrains, bin_size=bin_size * pq.ms)
        imat = asset_obj.intersection_matrix()
        pmat = asset_obj.probability_matrix_analytical(imat, kernel_width=bin_size * 15 * pq.ms)
        os.environ['ELEPHANT_USE_OPENCL'] = '0'
        jmat = asset_obj.joint_probability_matrix(pmat, filter_shape=(7, 1), n_largest=1)

        motif_neuron = []
        motif_neuron_num = []
        # motif_loc = []
        for gt in gts:
            NIDs = gt['NIDs'] + 1
            motif_neuron.append(NIDs)
            NIDs_size = NIDs.size
            motif_neuron_num.append(NIDs_size)

        motif_neuron = np.array(motif_neuron, dtype=object)
        motif_neuron_num = np.array(motif_neuron_num)

        max_neuron = params["NIDs"]

        alpha_list = np.concatenate([np.linspace(0, 0.9, 10), np.linspace(0.91, 0.99, 9)])
        patterns_list = []
        for alpha in alpha_list:
            mmat = asset_obj.mask_matrices([pmat, jmat], [alpha, alpha])
            cmat = asset_obj.cluster_matrix_entries(mmat, max_distance=30, min_neighbors=2, stretch=5)
            patterns = asset_obj.extract_synchronous_events(cmat)
            patterns_list_append = []
            for pattern in patterns.values():
                pattern_values = set().union(*pattern.values())
                if len(pattern_values) > 1:
                    patterns_list_append.append(tuple(pattern_values_ + 1 for pattern_values_ in pattern_values))
            patterns_list.append(patterns_list_append)

        for k_tuple in tqdm(range(1, k_tuples)):
            itemset_number_list = []
            pvalue_list = []
            for i_patterns_list, patterns_list_ in enumerate(patterns_list):
                pvalue = round(alpha_list[i_patterns_list], 2)
                for pattern in patterns_list_:
                    for itemset in combinations(pattern, k_tuple + 1):
                        itemset_number = itemset_tuple_to_number(max_neuron, k_tuple + 1, itemset)
                        itemset_number_list.append(itemset_number)
                        pvalue_list.append(pvalue)

            motif_neuron_k = motif_neuron[motif_neuron_num > k_tuple]
            condition_positive_set = [set(itemset_tuple_to_number(max_neuron, k_tuple + 1, condition_positive_tuple) for condition_positive_tuple in permutations(motif_neuron_k_combination)) for motif_neuron_k_i in motif_neuron_k for motif_neuron_k_combination in combinations(motif_neuron_k_i, k_tuple + 1)]
            condition_positive = len(condition_positive_set)

            condition_negative_set = set(itemset_number_list) - set(itemset_tuple_to_number(max_neuron, k_tuple + 1, motif_neuron_k_permutation) for i, motif_neuron_k_i in enumerate(motif_neuron_k) for motif_neuron_k_permutation in permutations(motif_neuron_k_i, k_tuple + 1))
            condition_negative = len(condition_negative_set)

            fpr = [1]
            tpr = [1]
            f = open(f"./txt/asset/{file_path}_{probabilistic_participation}_{k_tuple + 1}_acc.txt", 'w')
            f.write(f"threshold, recall, precision, f1_score\n")

            enumerate_pvalue_list = enumerate(pvalue_list)
            for threshold in alpha_list:
                enumerate_pvalue_list = [(pvalue_index, pvalue) for pvalue_index, pvalue in enumerate_pvalue_list if pvalue <= threshold]
                threshold_tuple_set = set(itemset_number_list[pvalue_index] for pvalue_index, pvalue in enumerate_pvalue_list)
                true_positive = 0
                for condition_positive_set_ in condition_positive_set:
                    if any(condition_positive_tuple in threshold_tuple_set for condition_positive_tuple in condition_positive_set_):
                        true_positive += 1
                false_positive = len(threshold_tuple_set & condition_negative_set)
                try:
                    fpr.append(false_positive / condition_negative)
                except:
                    fpr.append(0)
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
            try:
                auroc = metrics.auc(fpr, tpr)
            except:
                auroc = 0
            f.close()

            plt.figure(figsize=(6.5, 5.5))
            plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (area = {auroc:.2f})')
            plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
            plt.tick_params(axis='both', labelsize=15)
            plt.xlabel('False Positive Rate', fontsize=23)
            plt.ylabel('True Positive Rate', fontsize=23)
            plt.title(f"{k_tuple + 1}-Tuple Count ROC Curve", fontsize=23)
            plt.legend(fontsize=15)
            plt.savefig(f"./figure/asset/{file_path}/{file_path}_{probabilistic_participation}_{k_tuple + 1}.png", bbox_inches='tight')
            plt.close()