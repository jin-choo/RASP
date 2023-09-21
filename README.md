# RASP: Robust Mining of Frequent Temporal Sequential Patterns under Temporal Variations

This repository contains the source code for the paper [RASP: Robust Mining of Frequent Temporal Sequential Patterns under Temporal Variations](https://).

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
