# Example README File

Created by: EPA1352 Group 13 

| Name    | Student Number |
|:-------:|:--------|
| Thomas Sandbergen  | 4720814 | 
| Thomas Rous | 4963946 |
| Matthijs van de Wiel | 4896947 |
| Yassine Mouhdad | 5879566 |
| Tom Hillenaar | 4861973 |


## Introduction

This Readme file contains an explanation on a high aggregration level  of how the model for assignment 2 in the course EPA1352 is structured. This is a general description of the model and more detailed information about the model could be found in the README files within the folders of the assignment. Furthermore, the README files contain information about the usage of the dedicated part of the model, but the coding section is explained with markdown lines in between the lines of codes.

## How to Use
The assignment is structured in such a way that the model files are combined in the folder `model`, the data implemented in the model in the folder `data` and the results of the experiments are given in the folder `experiment`. 

In order to run the model, one should open and run the `model_run.py` file. This file is connected with other files containing data, model information etc. While running the model_run file, the other files are being activated as well and, therefore, their information is used in the model run. 

In order to visualize the model, one should open and  run the `model_viz.py` file. Just as the model_run file, this model_viz file is connected with underlying files and, therefore, uses their information. 

Whenever one would like to understand the structure and behavior of the model in a more detailed way, the `components.py` and `model.py` files could be seen in order to understand the model in a more proper way. The data section could be seen in the `create_input_data_n1.py` file and the `_roads3.csv`, `BMMS_overview.xlsx`files in the data folder. These three files will create the `input_data_n1.csv` file which is being used in the model. 

Finally, there are also files in the model folder which focus on the data collection for the bridges in the model. In this way there are two ways to run the model: with or without data collection for the bridges. The decision to split these models is made in order to have a model that runs relatively fast (model without bridge data collection) and a model which takes longer to run, since it collects data for all the bridges implemented in the model. 