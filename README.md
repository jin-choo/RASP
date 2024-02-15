# RASP: Robust Mining of Frequent Temporal Sequential Patterns under Temporal Variations

This repository contains the source code for the paper [RASP: Robust Mining of Frequent Temporal Sequential Patterns under Temporal Variations](https://).

In this work, we propose RASP, an algorithm for **R**obust and resource-**A**daptive mining of temporal **S**equential **P**atterns.
RASP is built upon the following  ideas, each devised to address the above limitations: 
* **Relaxed TSPs and Duplicated Pattern Matching**: For robustness against temporal variation, RASP enables multiple TSPs to share the same instance based on the novel concept of a relaxed TSP, which permits a predefined level of time gap deviation.
* **Resource-Adaptive Automatic Hyperparameter Tuning**: RASP gradually increases the sizes of TSPs to detect larger TSPs. In order to maintain a proper number of TSPs of each size, \method adaptively adjusts thresholds based on the available resources, enhancing its usability.
* **Tree-based Concise Data Structure**: RASP employs a tree-based compact data structure to efficiently manage the increasing number of TSPs, improving both speed and space efficiency.

## Datasets

E-commerce dataset used in additional experiment obtained from YOOCHOOSE Gmbh [source](https://www.kaggle.com/datasets/chadgostopp/recsys-challenge-2015) is available at this [link](https://www.dropbox.com/scl/fo/xqamn47x7ybsnww3fgmyf/h?rlkey=mzdfrn5ncaq9696ju8botp73m&dl=0).

## Requirements

To install requirements, run the following command on your terminal:
```setup
pip install -r requirements.txt
```

## RASP on Neuron Activity Datasets

To perform RASP on neuron activity datasets, run this command:

```
./run.sh
```

## RASP on an E-commerce Dataset

To perform RASP on an e-commerce dataset, run this command:

```
./run_case.sh
```

## Evaluation

To evaluate the result TSPs, run this command:

```
python main.py -a read_ndcg_rc_exp
```

## Reference

This code is free and open source for only academic/research purposes (non-commercial). If you use this code as part of any published research, please acknowledge the following paper.
```

```
