# EventLogImputation

The provided code offers an implementation of the approaches presented in the following paper: 
**Data Imputation for Business Process Event Logs** by Konstantinos Varvoutas and Anastasios Gounaris. *Preprint submitted to Journal of Business Analytics*.

## Introduction

This repository contains the code for data imputation in business process event logs, implemented using the `pm4py` Python library.

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
