# Canadian National Collision Database (2017) Analysis

---

This repo contains my work on identifying data issues in the 2017 Canadian Collissions dataset, my recommendations, and analysis of contributing factors to collissions.

## Introduction

The Canadian National Collision Database (NCDB) contains all police-reported motor vehicle collisions on public roads in Canada that result in death or injury, and includes all vehicles and persons involved in these collisions. The data is collected by the Traffic Injury Research Foundation (TIRF) and is provided to the public through the [Open Government Portal](https://open.canada.ca/data/en/dataset/1f1c0d0a-1d4c-4b55-8c2c-ec53b08df7d3).

The 2017 dataset and the data dictionary is included in this repository [here](https://github.com/pokwir)

## Data Issues

The approach to identifying data issues was based on the seven dimensions of quality data including: — 1. **Accuracy** (the degree to which the data values are correct). 2. **Completeness** (the the degree to which all expected records in a dataset are present). 3.**Validity** (degree to which the values in a data element are valid). 4. **Uniqueness** (degree to which the records in a dataset are not duplicated). 5. **Timeliness** (degree to which a dataset is available when expected and depends on service level agreements being set up). 6. **Consistency** (degree to which a dataset is consistent internally and with other datasets). 7. **Relevance** (degree to which a dataset meets the requirements for the intended use).

The following is a high-level summary of the issues identified in the dataset:
<br>

|   Quality dimension |   Verdict |   Observation |
|--- |--- |--- |
|  Completeness  |   Passed |    No missing values or missed data records.   |
|  Validity  |   Failed |   At least 20 records with seven features (Columns) as ‘Unknown’ — including month, day, hour, and vehicle. All are assigned to the same case number. |
|  Timeliness  |   Passed |    No missing values or missed data records.   |
|  Uniqueness  |   Failed |    Duplicate records present.   |
|  Consistency  |   Passed |    Data format was as expected, is reference-able with the data keys.   |
|  Accuracy  |   Passed |    Without domain knowledge, findings were inconclusive.   |
|  Relevance |   Passed |    Dataset generally meets the requirements for the intended use.   |

## Recommendations

The following recommendations are made to improve the quality of the dataset or simmilar datasets:

- Rigorous data profiling and control of incoming data. The data seems to be coming from different jurisdictions and aggregated for distribution. Therefore, data quality from sources cannot be guaranteed. A good data profiling tool should be able to check the following aspects of the data. Format, patterns, consistency on each record, data value distributions, anomalies, and completeness.
- Data pipeline design to avoid duplicate data. This can be achieved through a centralized data management system, which is reviewed and quality control checks are conducted regularly.
- Accurate gathering of data requirements. This must include clear documentation of requirements and capturing all data conditions and scenarios.
- Integration of data lineage traceability system. Unique keys or unique sequence numbers. Add a timestamp (or version) to each data record to indicate when it is added or changed.
- Capable data quality control system. This system should be able to check the following aspects of the data. Format, patterns, consistency on each record, data value distributions, anomalies, and completeness.

## Analysis

Ananalysis of the dataset was performed in Python using the Pandas, Numpy, and ggplot libraries. The code notebook can be found **here.** The analysis focused on answering the following questions:
2.1. What age range and which sex are more likely to be associated with a collision?
2.2 What time(s) of days are most associated with a relatively high fatality rate?
2.3 What type(s) of weather are most associated with a relatively high fatality rate?
2.4 What is the effect of using a Safety device on the fatality rate?
2.5 Use the previous charts/reports and perform additional ad hoc analysis of the dataset to outline the key contributing factors to Canadian collisions.

**2.1 What age range and which sex are more likely to be associated with a collision?**\
Since the dataset and data dictionary didnt have the age group classification structure, I adopted government of Canada structure that can be found **here**
```python
age_ranges = [(0, 14), (15, 24), (25, 34), (35, 44), (45, 54), (55, 64), (65, 74), (75, 100)]
age_range_labels = ['0-14', '15-24', '25-34', '35-44', '45-54', '55-64', '65-74', '75+']

| Index |  Age  |   Female  |   Male    |
|-------|-------|-----------|-----------|
| 0     | 0-14  | 0.081847  | 0.071099  |
| 1     | 15-24 | 0.221457  | 0.213721  |
| 2     | 25-34 | 0.183045  | 0.185339  |
| 3     | 35-44 | 0.155892  | 0.153019  |
| 4     | 45-54 | 0.145812  | 0.153636  |
| 5     | 55-64 | 0.110213  | 0.122564  |
| 6     | 65-74 | 0.063627  | 0.063949  |
| 7     | 75+   | 0.038107  | 0.036673  |

The age range and sex more likely to be associated with a collision:
Age Range: 15-24, Sex: Female
Collision Proportion: 22.15%
```

![Alt text](images/gender-age-collision.png)

**Observation**
In general, there doesn't seem to be a significant difference in collision proportions between males and females across different age groups. The proportion values between the two genders are relatively close for most age categories.There isn't a strong or consistent pattern indicating a significant difference in collision rates based solely on gender or age

The age group "15-24" has the largest difference in collision proportions between males and females, with a slightly higher proportion for females. This suggest that young adult females have a slightly higher likelihood of being involved in collisions compared to their male counterparts.
<br>

**2.2 What time(s) of days are most associated with a relatively high fatality rate?**\
In analyzing fatality rate the subset of records with a fatality (3) divided by all colissions and expressed as a percentage. The following chart shows the fatality rate by time of day.

```python
fatality_df = df[df['P_ISEV'] == 3]
fatality_rate_by_hour = fatality_df.groupby('C_HOUR').size() / df.groupby('C_HOUR').size()
fatality_rate_by_hour.head()

| index | 0       | 1       | 2       | 3       | 4       | 5       | 6       | 7       | 8       | 9       | 10      | 11      | 12      | 13      | 14      | 15      | 16      | 17      | 18      | 19      | 20      | 21      | 22      | 23      |
|-------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|
| HOUR  | 0.000000| 1.000000| 2.000000| 3.000000| 4.000000| 5.000000| 6.000000| 7.000000| 8.000000| 9.000000|10.000000|11.000000|12.000000|13.000000|14.000000|15.000000|16.000000|17.000000|18.000000|19.000000|20.000000|21.000000|22.000000|23.000000|
|Fat_Rte| 0.019541| 0.021089| 0.018909| 0.028208| 0.020680| 0.018479| 0.011550| 0.006664| 0.003976| 0.005108| 0.006721| 0.005594| 0.005919| 0.005488| 0.005276| 0.004784| 0.004805| 0.003947| 0.006483| 0.007749| 0.007419| 0.009256| 0.010598| 0.013012|

Time of Day Most Associated with High Fatality Rate:
Hour: 3.0, Fatality Rate: 2.82%

```

![Alt text](images/fatality_rate_hour.png)

**Observation**:
The fatality rate of collisions tends to have relatively higher values during the early morning hours (around 3 AM) and late evening hours (around 8 PM to 11 PM). These times show slightly higher fatalities compared to other hours of the day. This suggests that collisions during these periods have a higher likelihood of resulting in fatalities.

The time period with the highest number of fatalities is between 1 am and 4 am, with the peak occurring at 3 am (2.82%). The lowest rates occur during the daytime between 8 am (0.4%) and 5 pm (0.39%), followed by a five-fold increase between 5 pm and midnight.

**2.3 What type(s) of weather are most associated with a relatively high fatality rate?**\
In analyzing fatality rate by weather type, the subset of records with a fatality (3) divided by all colissions aggregated by weather type and expressed as a percentage. The following chart shows the fatality rate by weather type.

```python
fatality_df = df[df['P_ISEV'] == 3]
fatality_rate_by_weather = fatality_df.groupby('C_WTHR').size() / df.groupby('C_WTHR').size()

|  C_WTHR  |  Dry      |  Wet      |  Snow     |  Slush    |  Icy      |  Sand/gravel |  Muddy    |  other    |  Unknown  |
|---------:|----------:|----------:|----------:|----------:|----------:|-------------:|----------:|----------:|----------:|
| fat_rte  |  0.006321 |  0.006669 |  0.005563 |  0.006545 |  0.004231 |    0.011474 |  0.004020 |  0.010417 |  0.011333 |


Weather Type Most Associated with High Fatality Rate:
Weather: Sand/gravel, Fatality Rate: 1.15%
```

![Alt text](images/fatality-rate-weather.png)

**Observations**

The fatality rates of collisions vary across different weather conditions. The highest fatality rate is associated with "Sand/gravel," followed by "Unknown" and "other" weather conditions. "Icy" and "Muddy" conditions have relatively lower fatality rates compared to other conditions.

Overall, adverse weather conditions, such as "Sand/gravel," "Unknown," and "other," pose a higher risk of fatal collisions. Conversely, weather conditions like "Dry," "Wet," "Snow", and "slush" have moderate fatality rates. It's important to consider these trends when evaluating road safety measures and strategies.

**2.4 What is the effect of using a Safety device on the fatality rate?**\
In analyzing fatality rate by safety device, the subset of records with a fatality (3) divided by all colissions aggregated by safety device and expressed as a percentage. The following chart shows the fatality rate by safety device.

```python
fatality_df = df[df['P_ISEV'] == 3]
fatality_rate_by_safety = fatality_df.groupby('P_SAFE').size() / df.groupby('P_SAFE').size()
fatality_rate_by_safety

|  i| P_SAFE                        |  fat_rte |
|---|-------------------------------|---------:|
|  0| No safety device              | 0.047818 |
|  1| Safety device used            | 0.003761 |
|  2| Helmet                        | 0.027932 |
|  3| Reflective clothing           | 0.126582 |
|  4| Other safety device           | 0.005171 |
|  5| No safety device used — buses | 0.007900 |
|  6| Not applicable                | 0.005010 |
|  7| Other                         | 0.014073 |
|  8| Unknown                       | 0.009238 |

Safety Device Most Associated with High Fatality Rate:
Safety Device: 'Reflective clothing', Fatality Rate: 12.66%
```

![Alt text](images/fatality-rate-safety-device.png)

**Observations**
It can be inferred that overall physical protective safety devices like helmets tend to reduce fatality in the event of a collision, while preventive safety devices like reflective clothing may not have the same level of impact in reducing fatality rates in the event of a collision.

Collisions where safety devices were used have the lowest fatality rate, indicating that the use of safety devices is associated with a lower risk of fatal outcomes.

Collisions involving individuals wearing reflective clothing have the highest fatality rate. Reflective clothing enhances visibility and might not provide physical protection in the event of a collision. 


**2.5 Use the previous charts/reports and perform additional ad hoc analysis of the dataset to outline the key contributing factors to Canadian collisions.**\

**Road Alignment & Collision Configuration**
I investigated road alignment and collision configuration to determine if there is a relationship between these factors and the number of colissions. The following chart shows the collision configuration by road alignment.

```python
# Prepare the dataset
df1 = df.loc[:,['C_RALN','C_CONF']]
df1.C_RALN = df1.C_RALN.replace({'Q':7,'U':8}).astype(int)
df1.C_CONF = df1.C_CONF.replace({'QQ':42,'UU':43,'XX':43}).astype(int)

# Separate different collision config.
df6 = []
df6.append( df1[df1.C_CONF < 10] )
df6.append( df1[(df1.C_CONF > 20)&(df1.C_CONF < 30)] )
df6.append( df1[(df1.C_CONF > 30)&(df1.C_CONF < 40)] )
df6.append( df1[df1.C_CONF > 40] )

# Summarize the collision numbers
se6 = []; df7 = []
for i in range(0,4):
    se6.append( df6[i].groupby(['C_RALN','C_CONF']).size() )
    se6[i].name = 'collision'
    df7.append( pd.DataFrame(se6[i]).reset_index() )

# plot using ggplot
```

![Alt text](images/Collision-config.png)

**Observations**

Most collision for one car accident is hitting a stationary object, followed closely by right and left roll on to shoulder.

For two veichles moving in same direction, most accidents are rear-end collision, which increase along road-alignment.

For two veichles traveling in opposite direction, right-angle collision is the largest, this is probably happening at intersections. Left turn conflic also poses a huge risk, but right-turn is minimal, lower than head-on collisions.

Most collisions happens on a level and aligned road. Drivers must pay close attention when driving on good road condition, following the traffic rules and regulations, and avoiding distractions.

