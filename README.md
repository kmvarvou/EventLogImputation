# EventLogImputation

The provided code implements the **preprocessing step** presented in the paper:  
**“Data Imputation for Business Process Event Logs”**  
*Preprint submitted to SN Computer Science.*

## Introduction

This repository contains the code for the pre-processing step, of business process event log, that is required for the application of the examined data imputation techniques. The code has been implemented using the `pm4py` Python library.

Three preprocessing flavors are supported:
- `trace_based`
- `cluster_based`
- `length_based`


## Installation

Before running the code, please install the `pm4py` library using the following command:

```sh
pip install pm4py
```

## Execution
```
python LogPreprocessing.py log_file_name preprocesssing_flavor
```
-preprocessing_flavor: trace_based, cluster_based, length_based

## Examples

The folder `bench-vldb20` contains a slightly modified version of the code from:  
[https://github.com/eXascaleInfolab/bench-vldb20](https://github.com/eXascaleInfolab/bench-vldb20)

In the folder `Datasets` you may find datasets for logs BPI 2012, 2013, and 2017 for each of the three preprocessing flavors.  

To run the experiments for a respective dataset:

1. Copy the contents of the desired dataset folder from `Datasets` to:  
   `bench-vldb20/TestingFramework/bin/Debug/data`
2. Proceed with the experiment using the files now available in the `data` folder.







