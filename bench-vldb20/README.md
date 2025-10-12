# Data Imputation for Business Process Event Logs

The provided code provides a slightly modified version of the code implemented originally in: "Khayati, M., Lerner, A., Tymchenko, Z., Cudr ́e-Mauroux, P.: Mind the gap: An experimental evaluation of imputation of missing values techniques in time series. Proc. VLDB Endow. 13(5), 768–782 (2020)" The original implementation was slightly modified to accomodate for the smaller length of business process event logs, also three new data sets (event log fragments used in the evaluation section of our work) were added.

## Prerequisites

- Ubuntu 16 or Ubuntu 18 (including Ubuntu derivatives, e.g., Xubuntu) or the same distribution under WSL.
- Clone this repository.
- Mono: Install mono from https://www.mono-project.com/download/stable/ and reboot your terminal.

___



## Build

- Build the Testing Framework using the installation script located in the root folder (takes several minutes)
```bash
    $ sh install_linux.sh
```
- To evaluate the recently added algorithms (SSA, MRNN and BRITS), please install the following packages (takes several minutes):
```bash
    $ sh install_extra.sh
```
___

## Execution


```bash
    $ cd TestingFramework/bin/Debug/
    $ mono TestingFramework.exe [arguments]
```
### Results
All results and plots will be added to `Results` folder. The accuracy results of all algorithms will be sequentially added for each scenario and dataset to: `Results/.../.../error/`. The runtime results of all algorithms will be added to: `Results/.../.../runtime/`. The plots of the recovered blocks will be added to the folder `Results/.../.../recovery/plots/`.


### Execution examples


1. Run cdrec on all datasets using the MCAR scenario
$ mono TestingFramework.exe -alg cdrec -d all -scen mcar

2. Run dynammo on all datasets using the MCAR scenario
$ mono TestingFramework.exe -alg dynammo -d all -scen mcar



(the argument -all is used because each dataset is split into fragments after using the pre-processing step, assuming that all fragments of e.g. BPI 2012 dataset using the trace variant of pre-processing step)
