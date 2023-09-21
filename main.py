import argparse
from itertools import product
from algorithms import *
from spade import *
from cad import *
from miper import *
from case import *

if __name__ == "__main__":
    # Parse the arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-a",
        "--algorithm",
        action="store",
        default="read",
        type=str,
        help="Select the algorithm",
    )
    args = parser.parse_args()

    motif_type_max = (2, 100, 0)
    seed_list = [0, 1, 2]
    recording_time_list = [10, 50, 100, 500, 1000]
    bin_size_list = [15, 25, 40]
    events_tsps_events_list_list = [[(50, 5, 5)], [(50, 5, 5)], [(100, 5, 5), (200, 5, 5), (300, 5, 5), (500, 5, 5), (1000, 5, 5)], [(50, 3, 5), (50, 4, 5), (50, 5, 5), (50, 6, 5), (50, 7, 5)]]
    bg_mt_pp_tj_tw_rb_list = [[(2.0, 0.2, 1, 0, 0), (2.0, 0.05, 1, 0, 0), (2.0, 0.1, 1, 0, 0), (2.0, 0.4, 1, 0, 0), (2.0, 0.2, 2, 0, 0), (2.0, 0.2, 3, 0, 0), (2.0, 0.2, 4, 0, 0), (2.0, 0.2, 1, 10, 0), (2.0, 0.2, 1, 20, 0), (2.0, 0.2, 1, 30, 0), (2.0, 0.2, 1, 50, 0), (2.0, 0.2, 1, 100, 0)], [(2.0, 0.4, 5, 10, 0), (2.0, 0.3, 4, 20, 0), (2.0, 0.2, 3, 30, 0)], [(2.0, 0.2, 1, 0, 0), (2.0, 0.4, 5, 10, 0)], [(2.0, 0.2, 1, 0, 0), (2.0, 0.4, 5, 10, 0)]]

    option_list = ['RASP']  #, 'RASP_o'
    memory_list = ['_1']  #'_5', '_1', '_0.5', '_0.1', '_0.05', '_0.01'
    top_K_list = [5, 10, 20, 100]

    # cad
    bin_size_list_cad = [15, 25, 40, 60, 85, 150, 250]
    alpha_list = [0.01, 0.05, 0.1, 0.2, 1.0]

    # spade
    dithering_list = [20, 50, 100]

    start_time = time.localtime()  # 시작 시간 저장

    # Run the frequent itemsets mining algorithm
    if args.algorithm.rstrip() == 'data':
        for i_list, events_tsps_events_list in enumerate(events_tsps_events_list_list):
            for seed, events_tsps_events, recording_time, bg_mt_pp_tj_tw_rb, bin_size in product(seed_list, events_tsps_events_list, recording_time_list, bg_mt_pp_tj_tw_rb_list[i_list], bin_size_list):
                try:
                    data(motif_type_max[0], events_tsps_events[0], recording_time, bg_mt_pp_tj_tw_rb[0], bg_mt_pp_tj_tw_rb[1], bg_mt_pp_tj_tw_rb[2], bg_mt_pp_tj_tw_rb[3], bg_mt_pp_tj_tw_rb[4], events_tsps_events[1:], motif_type_max[1], motif_type_max[2], bin_size, seed)
                except Exception as e:
                    print(e)
                    pass

    elif args.algorithm.rstrip() == 'read_ndcg_rc_exp':
        os.makedirs(f"./txt", exist_ok=True)
        for option in option_list:
            for memory in memory_list:
                if os.path.exists(f"/data/hyunjin/brainimage_java/neurons/{motif_type_max[0]}_{option}{memory}_"):
                    for i_list, events_tsps_events_list in enumerate(events_tsps_events_list_list):
                        f_ndcg = open(f"./txt/{motif_type_max[0]}_{option}_ndcg_exp_{i_list + 1}{memory}.csv", 'w')
                        f_ndcg.write(f'type,NIDs,time,bgRate,pp,tj,tw,mtRate,mtNeurons,mtNumbers,mtMaxLag,mtMaxSpikes,bin,win,inter,range,k,topk,ndcg,seed\n')
                        f_ndcg.close()

                        f_rc = open(f"./txt/{motif_type_max[0]}_{option}_rc_exp_{i_list + 1}{memory}.csv", 'w')
                        f_rc.write(f'type,NIDs,time,bgRate,pp,tj,tw,mtRate,mtNeurons,mtNumbers,mtMaxLag,mtMaxSpikes,bin,win,inter,range,k,topk,rc,seed\n')
                        f_rc.close()

                        for events_tsps_events, recording_time, bg_mt_pp_tj_tw_rb, bin_size, seed in product(events_tsps_events_list, recording_time_list, bg_mt_pp_tj_tw_rb_list[i_list], bin_size_list, seed_list):
                            try:
                                read_ndcg_rc_exp(motif_type_max[0], events_tsps_events[0], recording_time, bg_mt_pp_tj_tw_rb[0], bg_mt_pp_tj_tw_rb[1], bg_mt_pp_tj_tw_rb[2], bg_mt_pp_tj_tw_rb[3], bg_mt_pp_tj_tw_rb[4], events_tsps_events[1:], motif_type_max[1], motif_type_max[2], bin_size, bg_mt_pp_tj_tw_rb[5], option, seed, top_K_list, i_list + 1, memory)
                            except Exception as e:
                                print(e)
                                pass

    elif args.algorithm.rstrip() == 'cad_data':
        for i_list, events_tsps_events_list in enumerate(events_tsps_events_list_list):
            for seed, events_tsps_events, recording_time, bg_mt_pp_tj_tw_rb in product(seed_list, events_tsps_events_list, recording_time_list, bg_mt_pp_tj_tw_rb_list[i_list]):
                try:
                    cad_data(motif_type_max[0], events_tsps_events[0], recording_time, bg_mt_pp_tj_tw_rb[0], bg_mt_pp_tj_tw_rb[1], bg_mt_pp_tj_tw_rb[2], bg_mt_pp_tj_tw_rb[3], bg_mt_pp_tj_tw_rb[4], events_tsps_events[1:], motif_type_max[1], motif_type_max[2], seed)
                except Exception as e:
                    print(e)
                    pass
    
    elif args.algorithm.rstrip() == 'cad_read_ndcg_rc':
        for option in [2, 3, 4, 5]:
            if os.path.exists(f"/home/dmlab/hyunjin/brainimage/cad_stat{option}"):
                os.makedirs(f"./txt/cad_stat{option}", exist_ok=True)
                for i_list, events_tsps_events_list in enumerate(events_tsps_events_list_list):
                    f_ndcg = open(f"./txt/cad_stat{option}/{motif_type_max[0]}_cad_stat{option}_ndcg_{i_list + 1}.csv", 'w')
                    f_ndcg.write(f'type,NIDs,time,bgRate,pp,tj,tw,mtRate,mtNeurons,mtNumbers,mtMaxLag,mtMaxSpikes,bin,maxLag,alpha,k,topk,ndcg,seed\n')
                    f_ndcg.close()

                    f_rc = open(f"./txt/cad_stat{option}/{motif_type_max[0]}_cad_stat{option}_rc_{i_list + 1}.csv", 'w')
                    f_rc.write(f'type,NIDs,time,bgRate,pp,tj,tw,mtRate,mtNeurons,mtNumbers,mtMaxLag,mtMaxSpikes,bin,maxLag,alpha,k,topk,rc,seed\n')
                    f_rc.close()

                    for events_tsps_events, recording_time, bg_mt_pp_tj_tw_rb, alpha, bin_size, seed in product(events_tsps_events_list, recording_time_list, bg_mt_pp_tj_tw_rb_list[i_list], alpha_list, bin_size_list_cad, seed_list):
                        try:
                            cad_read_ndcg_rc(motif_type_max[0], events_tsps_events[0], recording_time, bg_mt_pp_tj_tw_rb[0], bg_mt_pp_tj_tw_rb[1], bg_mt_pp_tj_tw_rb[2], bg_mt_pp_tj_tw_rb[3], bg_mt_pp_tj_tw_rb[4], events_tsps_events[1:], motif_type_max[1], motif_type_max[2], bin_size, alpha, option, seed, top_K_list, i_list + 1)
                        except Exception as e:
                            print(e)
                            pass

    elif args.algorithm.rstrip() == 'cad_data_case':
        cad_data_case()

    elif args.algorithm.rstrip() == 'cad_read_case':
        for option in [2, 3, 4, 5]:
            for binSize in [60, 30, 20, 15, 10, 5, 3, 2, 1]:
                if os.path.exists(f"/home/dmlab/hyunjin/brainimage/cad_stat{option}"):
                    os.makedirs(f"./txt/cad_stat{option}", exist_ok=True)
                    for alpha in alpha_list:
                        cad_read_case(binSize, alpha, option)

    elif args.algorithm.rstrip() == 'spade_ndcg_rc':
        os.makedirs(f"./txt/spade", exist_ok=True)
        f = open(f"./txt/spade/{motif_type_max[0]}_spade_time_{time.strftime('%m.%d_%H.%M.%S', start_time)}.csv", 'w')
        f.write(f"type,NIDs,time,bgRate,pp,tj,tw,mtRate,mtNeurons,mtNumbers,mtMaxLag,mtMaxSpikes,bin,win,dither,k,time,seed\n")
        f.close()

        f_ndcg = open(f"./txt/spade/{motif_type_max[0]}_spade_ndcg_{time.strftime('%m.%d_%H.%M.%S', start_time)}.csv", 'w')
        f_ndcg.write(f'type,NIDs,time,bgRate,pp,tj,tw,mtRate,mtNeurons,mtNumbers,mtMaxLag,mtMaxSpikes,bin,win,dither,k,topk,ndcg,seed\n')
        f_ndcg.close()

        f_rc = open(f"./txt/spade/{motif_type_max[0]}_spade_rc_{time.strftime('%m.%d_%H.%M.%S', start_time)}.csv", 'w')
        f_rc.write(f'type,NIDs,time,bgRate,pp,tj,tw,mtRate,mtNeurons,mtNumbers,mtMaxLag,mtMaxSpikes,bin,win,dither,k,topk,rc,seed\n')
        f_rc.close()

        for i_list, events_tsps_events_list in enumerate(events_tsps_events_list_list):
            for dithering, bin_size, events_tsps_events, recording_time, bg_mt_pp_tj_tw_rb, seed in product(dithering_list, bin_size_list, events_tsps_events_list, recording_time_list, bg_mt_pp_tj_tw_rb_list, seed_list):
                try:
                    spade_ndcg_rc(motif_type_max[0], events_tsps_events[0], recording_time, bg_mt_pp_tj_tw_rb[0], bg_mt_pp_tj_tw_rb[1], bg_mt_pp_tj_tw_rb[2], bg_mt_pp_tj_tw_rb[3], bg_mt_pp_tj_tw_rb[4], events_tsps_events[1:], motif_type_max[1], motif_type_max[2], bin_size, dithering, start_time, seed, top_K_list)
                except Exception as e:
                    print(e)
                    pass

    elif args.algorithm.rstrip() == 'spade_read_ndcg_rc':
        os.makedirs(f"./txt/spade", exist_ok=True)
        for i_list, events_tsps_events_list in enumerate(events_tsps_events_list_list):
            f_ndcg = open(f"./txt/spade/{motif_type_max[0]}_spade_ndcg_{i_list + 1}.csv", 'w')
            f_ndcg.write(f'type,NIDs,time,bgRate,pp,tj,tw,mtRate,mtNeurons,mtNumbers,mtMaxLag,mtMaxSpikes,bin,win,dither,k,topk,ndcg,seed\n')
            f_ndcg.close()

            f_rc = open(f"./txt/spade/{motif_type_max[0]}_spade_rc_{i_list + 1}.csv", 'w')
            f_rc.write(f'type,NIDs,time,bgRate,pp,tj,tw,mtRate,mtNeurons,mtNumbers,mtMaxLag,mtMaxSpikes,bin,win,dither,k,topk,rc,seed\n')
            f_rc.close()

            for events_tsps_events, recording_time, bg_mt_pp_tj_tw_rb, dithering, bin_size, seed in product(events_tsps_events_list, recording_time_list, bg_mt_pp_tj_tw_rb_list[i_list], dithering_list, bin_size_list, seed_list):
                try:
                    spade_read_ndcg_rc(motif_type_max[0], events_tsps_events[0], recording_time, bg_mt_pp_tj_tw_rb[0], bg_mt_pp_tj_tw_rb[1], bg_mt_pp_tj_tw_rb[2], bg_mt_pp_tj_tw_rb[3], bg_mt_pp_tj_tw_rb[4], events_tsps_events[1:], motif_type_max[1], motif_type_max[2], bin_size, dithering, start_time, seed, top_K_list, i_list + 1)
                except Exception as e:
                    print(e)
                    pass

    elif args.algorithm.rstrip() == 'spade_case':
        os.makedirs(f"./txt/spade/yoochoose-clicks_crop", exist_ok=True)
        f = open(f"./txt/spade/yoochoose-clicks_crop_time_{time.strftime('%m.%d_%H.%M.%S', start_time)}.csv", 'w')
        f.write(f"time,item,length,bin,win,dither,time\n")
        f.close()

        for dithering in dithering_list:
            spade_case(dithering, start_time)

    elif args.algorithm.rstrip() == 'miper_read_ndcg_rc':
        os.makedirs(f"./txt/miper", exist_ok=True)
        if os.path.exists(f"/data/hyunjin/MIPER/txt"):
            for i_list, events_tsps_events_list in enumerate(events_tsps_events_list_list):
                f_ndcg = open(f"./txt/miper/miper_{motif_type_max[0]}_ndcg_{i_list + 1}.csv", 'w')
                f_ndcg.write(f'type,NIDs,time,bgRate,pp,tj,tw,mtRate,mtNeurons,mtNumbers,mtMaxLag,mtMaxSpikes,bin,win,inter,k,topk,ndcg,seed\n')
                f_ndcg.close()

                f_rc = open(f"./txt/miper/miper_{motif_type_max[0]}_rc_{i_list + 1}.csv", 'w')
                f_rc.write(f'type,NIDs,time,bgRate,pp,tj,tw,mtRate,mtNeurons,mtNumbers,mtMaxLag,mtMaxSpikes,bin,win,inter,k,topk,rc,seed\n')
                f_rc.close()

                for events_tsps_events, recording_time, bg_mt_pp_tj_tw_rb, bin_size, seed in product(events_tsps_events_list, recording_time_list, bg_mt_pp_tj_tw_rb_list[i_list], bin_size_list, seed_list):
                    try:
                        miper_read_ndcg_rc(motif_type_max[0], events_tsps_events[0], recording_time, bg_mt_pp_tj_tw_rb[0], bg_mt_pp_tj_tw_rb[1], bg_mt_pp_tj_tw_rb[2], bg_mt_pp_tj_tw_rb[3], bg_mt_pp_tj_tw_rb[4], events_tsps_events[1:], motif_type_max[1], motif_type_max[2], bin_size, seed, top_K_list, i_list + 1)
                    except Exception as e:
                        print(e)
                        pass

    elif args.algorithm.rstrip() == 'miper_read_case':
        os.makedirs(f"./txt/miper", exist_ok=True)
        miper_read_case()

    elif args.algorithm.rstrip() == 'case_data':
        os.makedirs(f"./txt", exist_ok=True)
        case_data()

    elif args.algorithm.rstrip() == 'case_data_crop':
        os.makedirs(f"./txt", exist_ok=True)
        case_data_crop()

    elif args.algorithm.rstrip() == 'case_read':
        os.makedirs(f"./txt", exist_ok=True)
        case_read()

    elif args.algorithm.rstrip() == 'case_random':
        os.makedirs(f"./txt", exist_ok=True)
        case_random()