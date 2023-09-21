import csv, datetime, os, random
from itertools import combinations

binSize_list = [60, 1]
rangebins_list = [5, 1]

time_min = datetime.datetime(2014, 4, 27, 0, 0, 0, 0)
time_max = datetime.datetime(2014, 4, 28, 0, 0, 0, 0)

# 100
item_list = [214821410, 214826610, 214826563, 214695399, 214829752, 214835002, 214834877, 214684108, 214829660, 214826589, 214828974, 214711280, 214829865, 214829387, 214833755, 214829396, 214829392, 214829366, 214826711, 214829852, 214834880, 214828976, 214834875, 214829810, 214835750, 214829385, 214709792, 214826994, 214829666, 214587028, 214684093, 214584969, 214554277, 214531151, 214829657, 214832717, 214821407, 214829664, 214712132, 214829820, 214832720, 214829747, 214828970, 214829861, 214826705, 214826709, 214820394, 214821332, 214840421, 214821294, 214743493, 214829850, 214835021, 214834873, 214832722, 214587266, 214835752, 214829390, 214743495, 214826666, 214831931, 214836330, 214828959, 214820392, 214826561, 214718210, 214821412, 214706432, 214821320, 214706460, 214828963, 214821350, 214826996, 214826670, 214826936, 214712229, 214821309, 214829034, 214834871, 214829715, 214826874, 214821317, 214712124, 214826992, 214829846, 214712126, 214829822, 214826664, 214744779, 214826805, 214829857, 214829368, 214834997, 214753515, 214840762, 214828965, 214705740, 214821399, 214829379, 214710152]
item_index = len(item_list)


def neurons_to_number(neurons, max_neuron, k_tuple):
    number = neurons[0] * pow(max_neuron, k_tuple)
    for k_neurons in range(1, k_tuple + 1):
        number += neurons[k_neurons] * pow(max_neuron, k_tuple - k_neurons)
    return number


def neurons_number_to_neurons(number, max_neuron, k_tuple):
    q, mod = divmod(number, pow(max_neuron, k_tuple))
    neurons = [q]
    for k_neurons in range(1, k_tuple + 1):
        q, mod = divmod(mod, pow(max_neuron, k_tuple - k_neurons))
        neurons.append(q)
    return neurons


def check_order_preserved(sublist, full_list):
    sub_len = len(sublist)
    # Initialize indices for both lists
    sub_index = 0
    full_index = 0
    # Iterate over both lists
    while sub_index < sub_len and full_index < len(full_list):
        if sublist[sub_index] == full_list[full_index]:
            sub_index += 1
        full_index += 1
    return sub_index == sub_len


def case_data():
    time_min = datetime.datetime(2014, 4, 27, 0, 0, 0, 0)
    time_max = datetime.datetime(2014, 4, 28, 0, 0, 0, 0)

    item_list = [214821410, 214826610, 214826563, 214695399, 214829752, 214835002, 214834877, 214684108, 214829660, 214826589, 214828974, 214711280, 214829865, 214829387, 214833755, 214829396, 214829392, 214829366, 214826711, 214829852, 214834880, 214828976, 214834875, 214829810, 214835750, 214829385, 214709792, 214826994, 214829666, 214587028, 214684093, 214584969, 214554277, 214531151, 214829657, 214832717, 214821407, 214829664, 214712132, 214829820, 214832720, 214829747, 214828970, 214829861, 214826705, 214826709, 214820394, 214821332, 214840421, 214821294, 214743493, 214829850, 214835021, 214834873, 214832722, 214587266, 214835752, 214829390, 214743495, 214826666, 214831931, 214836330, 214828959, 214820392, 214826561, 214718210, 214821412, 214706432, 214821320, 214706460, 214828963, 214821350, 214826996, 214826670, 214826936, 214712229, 214821309, 214829034, 214834871, 214829715, 214826874, 214821317, 214712124, 214826992, 214829846, 214712126, 214829822, 214826664, 214744779, 214826805, 214829857, 214829368, 214834997, 214753515, 214840762, 214828965, 214705740, 214821399, 214829379, 214710152]

    for binSize in [60, 30, 20, 15, 10, 5, 3, 2, 1]:
        item_ids = [set()]
        max_time = 0

        with open('../brainimage_java/txt/datasets/ecommerce/yoochoose-clicks_crop.dat', 'r') as input_file:
            reader = csv.reader(input_file, delimiter=',')
            for row in reader:
                time = datetime.datetime.strptime(row[1], "%Y-%m-%dT%H:%M:%S.%fZ").replace(microsecond=0)
                if time < time_min or time >= time_max:
                    continue
                item = int(row[2])
                if item in item_list:
                    time = int((time - time_min).total_seconds() // binSize)
                    if time > max_time:
                        for i in range(time - max_time):
                            item_ids.append(set())
                        item_ids[time].add(item)
                        max_time = time
                    else:
                        item_ids[time].add(item)

        item_dict = {item: i_item for i_item, item in enumerate(sorted(item_list))}

        for time, item_id in enumerate(item_ids):
            if item_id:
                item_ids[time] = sorted([item_dict[item] for item in item_id])
            else:
                item_ids[time] = []

        time_span = int(((time_max - time_min).total_seconds() + binSize - 0.000001) // binSize)

        os.makedirs(f"/data/hyunjin/MIPER/txt/datasets/ecommerce/", exist_ok=True)
        winlen = 600 // binSize
        with open(f'/data/hyunjin/MIPER/txt/datasets/ecommerce/yoochoose-clicks_crop_time_{time_span}_item_{len(item_list)}_bin_{binSize}_winlen_{winlen}.txt', 'w', newline='') as miper_file, open(f'../brainimage_java/txt/datasets/ecommerce/yoochoose-clicks_crop_time_{time_span}_item_{len(item_list)}_bin_{binSize}_winlen_{winlen}.txt', 'w', newline='') as output_file:
            writer_miper = csv.writer(miper_file, delimiter=' ')
            writer = csv.writer(output_file, delimiter=' ')
            for time, item_id in enumerate(item_ids):
                if item_id:
                    item_id_win = [item * winlen for item in item_id]
                    for win_idx in range(1, winlen):
                        try:
                            item_id_win.extend([item * winlen + win_idx for item in item_ids[time + win_idx]])
                        except:
                            break
                else:
                    item_id_win = []
                writer_miper.writerow(item_id)
                writer.writerow(item_id_win)


def case_data_crop():
    with open('../brainimage_java/txt/datasets/ecommerce/yoochoose-clicks.dat', 'r') as input_file, open('../brainimage_java/txt/datasets/ecommerce/yoochoose-clicks_crop.dat', 'w', newline='') as output_file:
        reader = csv.reader(input_file, delimiter=',')
        writer = csv.writer(output_file, delimiter=',')
        for row in reader:
            if time_min <= datetime.datetime.strptime(row[1], "%Y-%m-%dT%H:%M:%S.%fZ") < time_max:
                writer.writerow(row)


def case_read():
    for binSize in binSize_list:
        session_dict = dict()
        items_in_session = list()
        times_in_session = list()
        time_dict = dict()
        time_count_dict = dict()
        item_ids = list()
        with open('../brainimage_java/txt/datasets/ecommerce/yoochoose-clicks_crop.dat', 'r') as input_file:
            reader = csv.reader(input_file, delimiter=',')
            session_count = 0
            time_count = 0
            for row in reader:
                time = datetime.datetime.strptime(row[1], "%Y-%m-%dT%H:%M:%S.%fZ").replace(microsecond=0)
                if time < time_min or time >= time_max:
                    continue
                time = int((time - time_min).total_seconds() // binSize)
                item = int(row[2])
                if item in item_list:
                    session = int(row[0])
                    if session in session_dict:
                        item_indices = [index for index in range(len(items_in_session[session_dict[session]])) if items_in_session[session_dict[session]][index] == item]
                        time_indices = [index for index in range(len(times_in_session[session_dict[session]])) if times_in_session[session_dict[session]][index] == time]
                        if not (item in items_in_session[session_dict[session]] and time in times_in_session[session_dict[session]] and any(index in item_indices for index in time_indices)):
                            items_in_session[session_dict[session]].append(item)
                            times_in_session[session_dict[session]].append(time)
                    else:
                        session_dict[session] = session_count
                        session_count += 1
                        items_in_session.append([item])
                        times_in_session.append([time])
                    try:
                        item_ids[time_dict[time]].add(item)
                    except:
                        time_dict[time] = time_count
                        time_count_dict[time_count] = time
                        time_count += 1
                        item_ids.append({item})

        item_dict = {item: i_item for i_item, item in enumerate(sorted(item_list))}

        item_count_dict = dict()
        for item_id in item_ids:
            for item in item_id:
                try:
                    item_count_dict[item] += 1
                except:
                    item_count_dict[item] = 1

        times_list = list()
        for times in times_in_session:
            times_list.append(max(times) - min(times))

        max_pattern = 3
        pattern_count_dict = dict()
        pattern_time_dict = dict()
        for session_count, items_in_a_session in enumerate(items_in_session):
            if len(items_in_a_session) >= max_pattern:
                items_in_session[session_count] = [item_dict[item] for item in items_in_a_session]
                for comb in combinations(range(len(items_in_session[session_count])), max_pattern):
                    items_in_a_pattern_comb = [items_in_session[session_count][i_comb] for i_comb in comb]
                    if len(set(items_in_a_pattern_comb)) == len(items_in_a_pattern_comb):
                        times_diff_in_a_pattern = list(times_in_session[session_count][i_comb] - times_in_session[session_count][comb[0]] for i_comb in comb[1:])
                        if times_diff_in_a_pattern[-1] < 600:
                            times_diff_number = neurons_to_number(times_diff_in_a_pattern, 600, max_pattern - 2)
                            neurons_number = neurons_to_number(items_in_a_pattern_comb, item_index, max_pattern - 1)
                            if neurons_number in pattern_time_dict:
                                try:
                                    pattern_count_dict[neurons_number][times_diff_number] += 1
                                except:
                                    pattern_count_dict[neurons_number][times_diff_number] = 1
                                pattern_time_dict[neurons_number].add(times_in_session[session_count][comb[0]])
                            else:
                                pattern_count_dict[neurons_number] = {times_diff_number: 1}
                                pattern_time_dict[neurons_number] = {times_in_session[session_count][comb[0]]}

        item_count_dict = dict()
        for item_id in item_ids:
            if item_id:
                for item in [item_dict[item] for item in item_id]:
                    try:
                        item_count_dict[item] += 1
                    except:
                        item_count_dict[item] = 1

        items_in_times = [[] for _ in range(max(time_dict.keys()) + 1)]
        for time_count, item_id in enumerate(item_ids):
            if len(item_id) >= max_pattern:
                items_in_times[time_count_dict[time_count]] = sorted([item_dict[item] for item in item_id])

        times_items = [set() for _ in range(len(item_list))]
        for time, item_id in enumerate(items_in_times):
            if item_id:
                for item in item_id:
                    times_items[item].add(time)

        times_items = [sorted(times_item) for times_item in times_items]

        time_span = int(((time_max - time_min).total_seconds() + binSize - 0.000001) // binSize)
        winlen = 600 // binSize
        max_time_in_session = winlen - 1
        for rangebins in rangebins_list:
            neurons_support_sum_dict = dict()
            neurons_support_max_dict = dict()
            if os.path.exists(f'/data/hyunjin/brainimage_java/neurons/yoochoose-clicks_crop_tree_tid_1/yoochoose-clicks_crop_time_{time_span}_item_{item_index}_length_{3}_bin_{binSize}_winlen_{winlen}_interlen_{max_time_in_session}_rangebins_{rangebins}_{max_pattern}.txt'):
                for line in open(f'/data/hyunjin/brainimage_java/neurons/yoochoose-clicks_crop_tree_tid_1/yoochoose-clicks_crop_time_{time_span}_item_{item_index}_length_{3}_bin_{binSize}_winlen_{winlen}_interlen_{max_time_in_session}_rangebins_{rangebins}_{max_pattern}.txt', 'r'):
                    line_split = line.rstrip('\n').split()
                    neurons_number = int(line_split[0])
                    support = int(line_split[2])
                    try:
                        neurons_support_sum_dict[neurons_number] += support
                        if support > neurons_support_max_dict[neurons_number]:
                            neurons_support_max_dict[neurons_number] = support
                    except:
                        neurons_support_sum_dict[neurons_number] = support
                        neurons_support_max_dict[neurons_number] = support

                print()
                print(time_span, binSize, winlen, rangebins)

                neurons_support_sum_count = sorted(neurons_support_sum_dict.items(), key=lambda x: x[1], reverse=True)
                neurons_support_max_count = sorted(neurons_support_max_dict.items(), key=lambda x: x[1], reverse=True)

                neurons_dict = dict()

                print("neurons_support_sum_count")
                for neurons_number, count in neurons_support_sum_count[:100]:
                    if neurons_number not in neurons_dict:
                        neurons_first_time = set()
                        neurons = neurons_number_to_neurons(neurons_number, item_index, max_pattern - 1)
                        neurons = neurons
                        for first_time in times_items[neurons[0]]:
                            for second_time in [time for time in times_items[neurons[1]] if first_time <= time <= first_time + winlen - 1]:
                                if any(second_time <= time <= first_time + winlen for time in times_items[neurons[2]]):
                                    neurons_first_time.add(first_time)
                                    break
                        try:
                            pattern_time_len = len(pattern_time_dict[neurons_number])
                        except:
                            pattern_time_len = 0
                        neurons_dict[neurons_number] = f"{neurons}/{len(neurons_first_time)}/{pattern_time_len}/{len(neurons_first_time) - pattern_time_len}"
                    print(neurons_dict[neurons_number])

                print("neurons_support_max_count")
                for neurons_number, count in neurons_support_max_count[:100]:
                    if neurons_number not in neurons_dict:
                        neurons_first_time = set()
                        neurons = neurons_number_to_neurons(neurons_number, item_index, max_pattern - 1)
                        neurons = neurons
                        for first_time in times_items[neurons[0]]:
                            for second_time in [time for time in times_items[neurons[1]] if first_time <= time <= first_time + winlen - 1]:
                                if any(second_time <= time <= first_time + winlen for time in times_items[neurons[2]]):
                                    neurons_first_time.add(first_time)
                                    break
                        try:
                            pattern_time_len = len(pattern_time_dict[neurons_number])
                        except:
                            pattern_time_len = 0
                        neurons_dict[neurons_number] = f"{neurons}/{len(neurons_first_time)}/{pattern_time_len}/{len(neurons_first_time) - pattern_time_len}"
                    print(neurons_dict[neurons_number])

def case_random():
    for binSize in binSize_list:
        session_dict = dict()
        items_in_session = list()
        times_in_session = list()
        time_dict = dict()
        time_count_dict = dict()
        item_ids = list()
        with open('../brainimage_java/txt/datasets/ecommerce/yoochoose-clicks_crop.dat', 'r') as input_file:
            reader = csv.reader(input_file, delimiter=',')
            session_count = 0
            time_count = 0
            for row in reader:
                time = datetime.datetime.strptime(row[1], "%Y-%m-%dT%H:%M:%S.%fZ").replace(microsecond=0)
                if time < time_min or time >= time_max:
                    continue
                time = int((time - time_min).total_seconds() // binSize)
                item = int(row[2])
                if item in item_list:
                    session = int(row[0])
                    if session in session_dict:
                        item_indices = [index for index in range(len(items_in_session[session_dict[session]])) if items_in_session[session_dict[session]][index] == item]
                        time_indices = [index for index in range(len(times_in_session[session_dict[session]])) if times_in_session[session_dict[session]][index] == time]
                        if not (item in items_in_session[session_dict[session]] and time in times_in_session[session_dict[session]] and any(index in item_indices for index in time_indices)):
                            items_in_session[session_dict[session]].append(item)
                            times_in_session[session_dict[session]].append(time)
                    else:
                        session_dict[session] = session_count
                        session_count += 1
                        items_in_session.append([item])
                        times_in_session.append([time])
                    try:
                        item_ids[time_dict[time]].add(item)
                    except:
                        time_dict[time] = time_count
                        time_count_dict[time_count] = time
                        time_count += 1
                        item_ids.append({item})

        item_dict = {item: i_item for i_item, item in enumerate(sorted(item_list))}

        item_count_dict = dict()
        for item_id in item_ids:
            for item in item_id:
                try:
                    item_count_dict[item] += 1
                except:
                    item_count_dict[item] = 1

        times_list = list()
        for times in times_in_session:
            times_list.append(max(times) - min(times))

        max_pattern = 3
        pattern_count_dict = dict()
        pattern_time_dict = dict()
        for session_count, items_in_a_session in enumerate(items_in_session):
            if len(items_in_a_session) >= max_pattern:
                items_in_session[session_count] = [item_dict[item] for item in items_in_a_session]
                for comb in combinations(range(len(items_in_session[session_count])), max_pattern):
                    items_in_a_pattern_comb = [items_in_session[session_count][i_comb] for i_comb in comb]
                    if len(set(items_in_a_pattern_comb)) == len(items_in_a_pattern_comb):
                        times_diff_in_a_pattern = list(times_in_session[session_count][i_comb] - times_in_session[session_count][comb[0]] for i_comb in comb[1:])
                        if times_diff_in_a_pattern[-1] < 600:
                            times_diff_number = neurons_to_number(times_diff_in_a_pattern, 600, max_pattern - 2)
                            neurons_number = neurons_to_number(items_in_a_pattern_comb, item_index, max_pattern - 1)
                            if neurons_number in pattern_time_dict:
                                try:
                                    pattern_count_dict[neurons_number][times_diff_number] += 1
                                except:
                                    pattern_count_dict[neurons_number][times_diff_number] = 1
                                pattern_time_dict[neurons_number].add(times_in_session[session_count][comb[0]])
                            else:
                                pattern_count_dict[neurons_number] = {times_diff_number: 1}
                                pattern_time_dict[neurons_number] = {times_in_session[session_count][comb[0]]}

        item_count_dict = dict()
        for item_id in item_ids:
            if item_id:
                for item in [item_dict[item] for item in item_id]:
                    try:
                        item_count_dict[item] += 1
                    except:
                        item_count_dict[item] = 1

        items_in_times = [[] for _ in range(max(time_dict.keys()) + 1)]
        for time_count, item_id in enumerate(item_ids):
            if len(item_id) >= max_pattern:
                items_in_times[time_count_dict[time_count]] = sorted([item_dict[item] for item in item_id])

        times_items = [set() for _ in range(len(item_list))]
        for time, item_id in enumerate(items_in_times):
            if item_id:
                for item in item_id:
                    times_items[item].add(time)

        times_items = [sorted(times_item) for times_item in times_items]

        time_span = int(((time_max - time_min).total_seconds() + binSize - 0.000001) // binSize)
        winlen = 600 // binSize

        print(time_span, binSize, winlen)

        random_iteration_number = 100
        neurons_dict = dict()
        for random_iteration in range(random_iteration_number):
            random.seed(random_iteration)
            neurons = random.sample(range(item_index), 3)
            neurons_number = neurons_to_number(neurons, item_index, max_pattern - 1)
            while neurons_number in neurons_dict:
                neurons = random.sample(range(item_index), 3)
                neurons_number = neurons_to_number(neurons, item_index, max_pattern - 1)
            if neurons_number not in neurons_dict:
                neurons_first_time = set()
                for first_time in times_items[neurons[0]]:
                    for second_time in [time for time in times_items[neurons[1]] if first_time <= time <= first_time + winlen - 1]:
                        if any(second_time <= time <= first_time + winlen for time in times_items[neurons[2]]):
                            neurons_first_time.add(first_time)
                            break
                try:
                    pattern_time_len = len(pattern_time_dict[neurons_number])
                except:
                    pattern_time_len = 0
                neurons_dict[neurons_number] = f"{neurons}/{len(neurons_first_time)}/{pattern_time_len}/{len(neurons_first_time) - pattern_time_len}"
            print(neurons_dict[neurons_number])
