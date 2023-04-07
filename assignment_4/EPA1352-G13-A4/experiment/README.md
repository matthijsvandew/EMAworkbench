# Simple Transport Model Demo in MESA

Created by: 
Yilin HUANG 

Adapted by EPA1352 Group 13

Email:
y.huang@tudelft.nl

Version:
1.1

## Introduction

A transport model in MESA for EPA1352 Advanced Simulation course Assignment 4. 

## How to Use

* Check the output from the model runs in the result_bridges folder.
```
    $ result_bridges
```

* Check the analysed output from the model runs in the Analysed_result_bridges folder.
```
    $ Analysed_result_bridges
```

## Files

* [analysis_ouptut.py](analysis_output.py): Contains the code to analyse the results from the model runs. 
For every scenario, the average caused delay time by a bridge over the different replications is gathered as well as the average number of vehicles that passed the bridge.
This file writes its results to the Analysed_result_bridges folder.
The file reads data in from the result_bridges folder.

* [Visuals.py](Visuals.py): Contains the code to create box-plots of delay caused by bridges, given the bridge broke down, for every scenario.
This file reads data in from the result_bridges folder.

* [experimental_input.csv](experimental_input.csv): Provides the different scenarios in which bridges break down due to, for example, flooding.
