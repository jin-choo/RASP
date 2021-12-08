import argparse
from algorithms import *
from algorithms_prev import *
from spade import *
from cad import *
from asset import *

if __name__ == "__main__":
    # Parse the arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-a",
        "--algorithm",
        action="store",
        default="apriori",
        type=str,
        help="Select the algorithm",
    )
    parser.add_argument(
        "-t",
        "--time-interval",
        action="store",
        default="1",
        type=int,
        help="Select the half-overlapped time interval",
    )
    parser.add_argument(
        "-k",
        "--k-tuples",
        action="store",
        default="2",
        type=int,
        help="Select the maximum size of candidate k-tuples",
    )
    parser.add_argument(
        "-w",
        "--winlen",
        action="store",
        default="30",
        type=int,
        help="Select the window length",
    )
    parser.add_argument(
        "-c",
        "--count",
        action="store",
        default="1",
        type=int,
        help="Select the threshold of count",
    )
    parser.add_argument(
        "-f",
        "--file-path",
        action="store",
        default="oasis_noisy",
        type=str,
        help="Select the filepath",
    )
    parser.add_argument(
        "-p",
        "--probabilistic-participation",
        action="store",
        default="1",
        type=int,
        help="Select the probabilistic participation",
    )
    parser.add_argument(
        "-e",
        "--epsilon",
        action="store",
        default="0",
        type=int,
        help="Select the epsilon (noise thresholds)",
    )

    args = parser.parse_args()

    # Run the frequent itemsets mining algorithm
    if args.algorithm.rstrip() == 'prev':
        apriori_prev(args.algorithm.rstrip(), args.time_interval, args.k_tuples, args.winlen, args.count, args.file_path.rstrip(), args.probabilistic_participation, args.epsilon)
    elif args.algorithm.rstrip() == 'read':
        apriori_read(args.time_interval, args.k_tuples, args.winlen, args.count, args.file_path.rstrip(), args.probabilistic_participation, args.epsilon)
    elif args.algorithm.rstrip() == 'spade':
        spade_read(args.k_tuples, args.file_path.rstrip(), args.winlen, args.probabilistic_participation)
    elif args.algorithm.rstrip() == 'cad':
        cad_read(args.k_tuples, args.file_path.rstrip(), args.count, args.probabilistic_participation)
    elif args.algorithm.rstrip() == 'asset':
        asset_read(args.k_tuples, args.file_path.rstrip(), args.count, args.probabilistic_participation)
    else:
        apriori(args.algorithm.rstrip(), args.time_interval, args.k_tuples, args.winlen, args.count, args.file_path.rstrip(), args.probabilistic_participation, args.epsilon)