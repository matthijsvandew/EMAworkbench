# Data for Model Generation of Simple Transport Model Demo in MESA

Created by: 
EPA1352-G13-A2

## Introduction

The data folder contains three different data files. the roads.csv data file and the BMMS_overview.xlsx data file form the basis of the used data for the model. These data files will be adjusted and finally merged into the input_data_n1.csv data file. 

The transport model for EPA1352 Advanced Simulation course Assignment 2, takes this `csv` input data file that specifies the infrastructure model components to be generated. The data format used by the model is described here. 

## Format

|     Column | Description                                              |
|-----------:|:---------------------------------------------------------|
|         id | **Unique ID** of the component                           |
|       road | On which road does the component belong to               |
|    LRPName | **Unique ID** of the component                           |
|     length | Length of the object in meters                           |
|   chainage | Exact location of the component whithin the road         |
|        lon | Longitude in Decimal Degrees                             |
|        lat | Latitude in Decimal Degrees                              |
| model_type | Type (i.e. class) of the model component to be generated |
|       name | Name of the object                                       |
|  condition | Name of the object                                       |


The column `road` is used by the model generation to classify model components by roads, i.e., on which road does a component belong to. The model generation assumes that the infrastructure model components of the same road is ordered sequentially. This means, e.g. in `demo-1.csv`, component `100000` is connected to component `100001`, that is connected to component `100002`, that is connected to component `100003`, etc., all of which are on road `N1`. 

The column `model_type` is used by the model generation to identify which class of components to be generated. The `model_type` labels used in this column must be consistent with the labels in the `generate_model` routine. 

The rest of the information is used to instantiate the components (objects). 

You may change the data format and structure if the model generation (`generate_model`) routine is adapted accordingly. 

All data files contained in this directory are used as demonstration for model generation. They are not based on real data. 
