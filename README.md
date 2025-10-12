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





