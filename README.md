# Canadian National Collision Database (2017) Analysis

This repo contains my work on identifying data issues in the 2017 Canadian Collissions dataset, my recommendations, and analysis of contributing factors to collissions. 
---
## Introduction
The Canadian National Collision Database (NCDB) contains all police-reported motor vehicle collisions on public roads in Canada that result in death or injury, and includes all vehicles and persons involved in these collisions. The data is collected by the Traffic Injury Research Foundation (TIRF) and is provided to the public through the [Open Government Portal](https://open.canada.ca/data/en/dataset/1f1c0d0a-1d4c-4b55-8c2c-ec53b08df7d3).

The 2017 dataset and the data dictionary is included in this repository [here](https://github.com/pokwir)

## Data Issues
The approach to identifying data issues was based on the seven dimensions of quality data including: — 1. **Accuracy** (the degree to which the data values are correct). 2. **Completeness** (the the degree to which all expected records in a dataset are present). 3.**Validity** (degree to which the values in a data element are valid). 4. **Uniqueness** (degree to which the records in a dataset are not duplicated). 5. **Timeliness** (degree to which a dataset is available when expected and depends on service level agreements being set up). 6. **Consistency** (degree to which a dataset is consistent internally and with other datasets). 7. **Relevance** (degree to which a dataset meets the requirements for the intended use).

The following is a high-level summary of the issues identified in the dataset:
<br>

|   Quality dimension	|   Verdict	|   Observation	|
|---	|---	|---	|
|  Completeness 	|   Passed	|    No missing values or missed data records.   |
|  Validity 	|   Failed	|    At least 20 records with seven features (Columns) as ‘Unknown’ — including month, day, hour, and vehicle. All are assigned to the same case number. 
   |
|  Timeliness 	|   Passed	|    No missing values or missed data records.   |
|  Completeness 	|   Passed	|    No missing values or missed data records.   |
|  Completeness 	|   Passed	|    No missing values or missed data records.   |
|  Completeness 	|   Passed	|    No missing values or missed data records.   |
|   	|   	|       |
