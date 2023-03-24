# Readme Group 13

Created by: EPA1352 Group 13 

| Name    | Student Number |
|:-------:|:--------|
| Thomas Sandbergen  | 4720814 | 
| Thomas Rous | 4963946 |
| Matthijs van de Wiel | 4896947 |
| Yassine Mouhdad | 5879566 |
| Tom Hillenaar | 4861973 |

### Getting started

First setup a new virtual environement in **Python 3.10**

Install the requirements:

`````shell
 pip install -r requirements.txt 
`````


## Introduction

This Readme file contains an explanation on a high aggregration level  of how the model for assignment 
3 in the course EPA1352 is structured. This is a general description of the model and more detailed information about 
the model could be found in the README files within the folders of the assignment. Furthermore, the README files contain 
information about the usage of the dedicated part of the model, 
but the coding section is explained with markdown lines in between the lines of codes.

## How to Use
The assignment is structured in such a way that the model files are combined in the folder `model`, 
the input data that is being used by the model in the folder `data` and the results of the experiments and the
experimental setup are given in the folder `experiment`. The report pdf is stored as 
`Advanced_Simulation_assignment_3.pdf`

In order to run the model, one should open and run the `model_run.py` file. This file is connected with other 
files containing data, model information etc. While running the model_run file, the other files are being activated 
as well and, therefore, their information is used in the model run. 

In order to visualize the model, one should open and  run the `model_viz.py` file. Just as the model_run file, 
this model_viz file is connected with underlying files and, therefore, uses their information. 

Note that `model_viz.py` and `model_run.py` use the same input data and same underlying files. However, `model_run.py` 
uses scenario's and replications to gain experimental output. Therefore it is particularly useful retrieve data 
which can be analysed by statistics. `model_viz.py` on the other hand is only useful for visualising model behavior
and gaining insights into model operation.

Whenever one would like to understand the structure and behavior of the model in a more detailed way, 
the `components.py`, `road_graph_nx.py` and `model.py` files could be seen in order to understand the model in a 
more proper way. 
The input data creation could be seen in the `create_input_data_n1.py` file and which uses the file `_roads3.csv`, 
`BMMS_overview.xlsx` files in the data folder. 
These three files will create the `input_data.csv` file which is being used in the model. 

Finally, the file `visuals.py` is used to analyse the data which is being created. It is interesting to 
extend this analysis by implementing more statistical measures.

## File-structure

**Advanced_Simulation_assignment_3.pdf**
This file is the report for assignment 3

**data**
Used for input data for the model.
- `_roads3.csv`
- `BMMS_overview.xlsx`
- `demo-4.csv`
- `Overview_intersections.xlsx`
- `Overview_intersections2.xlsx`

**Experiment** 
Used to design experimental input and store the experimental output.
- `base_case_results.csv`
- `experimental_input.csv`
- `scenario1_results.csv`
- `scenario2_results.csv`
- `scenario3_results.csv`
- `scenario4_results.csv`
- `visuals.py`

**model**
- ContinuousSpace folder: `simple_continuous_canvas.js` `SimpleContinuousModule.py`
- `components.py`
- `create_input_data_roads.py`
- `model.py`
- `model_run.py`
- `model_viz.py`
- `road_graph_nx.py`

**bonus**
Contains the files for the bonus assignment
`assignment3_bonus_intersections_roads_conclusion.ipynb`
`intersections_roads_bonus_assingment3_input_file.ipynb`

**img**
Shows some pictures which visualises how the model works.
- `demo-4.png`
- `N1.png`
- `N1N2.png`