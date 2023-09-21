# RASP: Robust Mining of Frequent Temporal Sequential Patterns under Temporal Variations

This repository contains the source code for the paper [RASP: Robust Mining of Frequent Temporal Sequential Patterns under Temporal Variations](https://).

In this work, we empirically investigate the persistence of higher-order interactions (HOIs) in 13 real-world hypergraphs from 6 domains.
We define the measure of the persistence of HOIs, and using the measure, we closely examine the persistence at 3 different levels (hypergraphs, groups, and nodes), with a focus on patterns, predictability, and predictors.
* **Patterns**: We reveal power-laws in the persistence and examine how they vary depending on the size of HOIs. Then, we explore relations between the persistence and 16 group- or node-level structural features, and we find some (e.g., entropy in the sizes of hyperedges including them) closely related to the persistence.
* **Predictibility**: Based on the 16 structural features, we assess the predictability of the future persistence of HOIs. Additionally, we examine how the predictability varies depending on the sizes of HOIs and how long we observe HOIs.
* **Predictors**: We find strong group- and node-level predictors of the persistence of HOIs, through Gini importance-based feature selection. The strongest predictors are (a) the number of hyperedges containing the HOI and (b) the average (weighted) degree of the neighbors of each node in the HOIs.

In this work, we propose RASP, an algorithm for **R**obust and resource-**A**daptive mining of temporal **S**equential **P**atterns.
RASP is built upon the following  ideas, each devised to address the above limitations: 
* **Relaxed TSPs and Duplicated Pattern Matching**: For robustness against temporal variation, RASP enables multiple TSPs to share the same instance based on the novel concept of a relaxed TSP, which permits a predefined level of time gap deviation.
* **Resource-Adaptive Automatic Hyperparameter Tuning**: RASP gradually increases the sizes of TSPs to detect larger TSPs. In order to maintain a proper number of TSPs of each size, \method adaptively adjusts thresholds based on the available resources, enhancing its usability.
* **Tree-based Concise Data Structure**: RASP employs a tree-based compact data structure to efficiently manage the increasing number of TSPs, improving both speed and space efficiency.

## Supplementary Document

Please see [supplementary](./supplementary.pdf).

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
