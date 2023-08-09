# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# %%
data = '/Users/patrickokwir/Desktop/Lighthouse-data-notes/National-Collision-Database-Analysis/dataset/y_2017_en.xlsx'
data = pd.read_excel(data)
data.head()

# %%
data.describe()

# %% [markdown]
# **Question 2: Using Excel (Pivot Tables/Charts), or any other analytical tool of your choice, generate reports/charts to answer the following questions:**
# 
# What age range and which sex are more likely to be associated with a collision?\
# What time(s) of days are most associated with a relatively high fatality rate?\
# What type(s) of weather are most associated with a relatively high fatality rate?\
# What is the effect of using a Safety device on the fatality rate?\
# Use the previous charts/reports and perform additional ad hoc analysis of the dataset to outline the key contributing factors to Canadian collisions.

# %% [markdown]
# **2.1 What age range and which sex are more likely to be associated with a collision?\**

# %%
import copy
df = copy.deepcopy(data)

# %%
df['P_SEX'].unique()

# %%
df['P_AGE'].unique()

# %%
df['C_SEV'].unique()

# %% [markdown]
# Classification structure
# Classification of age group - Classification structure\
# Code	Category\
# 1	15 to 24 years\
# 2	25 - 34 years\
# 3	35 - 44 years\
# 4	45 - 54 years\
# 5	55 - 64 years\
# 6	65 - 74 years\
# 7	75 years and over\
# 
# source: https://www23.statcan.gc.ca/imdb/p3VD.pl?Function=getVD&TVD=252430

# %%
# Filter out rows with 'Unknown' values in 'P_SEX' and convert non-numeric 'P_AGE' values to NaN
df = df[df['P_SEX'] != 'U']
df = df[df['P_SEX']!= 'N']
df = df[df['P_AGE']!= 'UU']
df = df[df['P_AGE']!= 'NN']
df['P_AGE'] = pd.to_numeric(df['P_AGE'], errors='coerce')

# Filter rows where collision severity is either 1 or 2
collision_df = df[df['C_SEV'].isin([1, 2])]


# Filter rows where collision severity is either 1 or 2
collision_df = df[df['C_SEV'].isin([1, 2])]
# Define Sex Labels for each P_SEX value and replace in df
collision_df['P_SEX'] = collision_df['P_SEX'].replace({'M': 'Male', 'F': 'Female'})
# Define Severity Labels for each C_SEV value and replace in collision_df
collision_df['C_SEV'] = collision_df['C_SEV'].replace({'1': 'At least one fatality', '2': 'Non-Fatal'})

# Define age ranges and corresponding labels
age_ranges = [(0, 14), (15, 24), (25, 34), (35, 44), (45, 54), (55, 64), (65, 74), (75, 100)]
age_range_labels = ['0-14', '15-24', '25-34', '35-44', '45-54', '55-64', '65-74', '75+']

# Calculate total collisions for each age range and sex combination
collision_counts = collision_df.groupby(['P_SEX', pd.cut(collision_df['P_AGE'], [age[0] for age in age_ranges] + [age_ranges[-1][1]], labels=age_range_labels)]).size().unstack().fillna(0)

# Calculate proportions of collisions for each age range and sex combination
collision_proportions = collision_counts.div(collision_counts.sum(axis=1), axis=0)

# Find the age range and sex with the highest collision proportion
max_collision_proportion = collision_proportions.stack().max()
max_collision_idx = collision_proportions.stack().idxmax()

print(f"The age range and sex more likely to be associated with a collision:")
print(f"Age Range: {max_collision_idx[1]}, Sex: {max_collision_idx[0]}")
print(f"Collision Proportion: {max_collision_proportion:.2%}")



# %%
from lets_plot import *
LetsPlot.setup_html()

# %%
# get data to plot 
plot_data = collision_proportions.transpose().reset_index(level=0)
plot_data

# %%
# plot plot_data using letsplot

# Create the ggplot visualization
p = ggplot(plot_data, aes(x='P_AGE', y='Female')) + geom_lollipop(stat='identity', shape = 1, color = 'red', size = 3, stroke = 2, linewidth=1, show_legend = True) + \
    geom_lollipop(aes(x='P_AGE', y='Male'), stat='identity', position='dodge', width=5, color = 'yellow', linewidth=1, offset= 10, show_legend = True) + \
        theme_classic() + \
            flavor_high_contrast_dark()
# Display legend 
p = p + labs(x = 'Age', y = 'Colission Proportion', title= 'Collision propotions by gender and age group') 
p

# %% [markdown]
# 2.2 What time(s) of days are most associated with a relatively high fatality rate?

# %%
df = copy.deepcopy(data)

# %%
# Convert 'C_HOUR' and 'P_ISEV' columns to numeric
df['C_HOUR'] = pd.to_numeric(df['C_HOUR'], errors='coerce')
df['P_ISEV'] = pd.to_numeric(df['P_ISEV'], errors='coerce')

# Filter out non-numeric values in 'C_HOUR' and 'P_ISEV'
df = df.dropna(subset=['C_HOUR', 'P_ISEV'])

# Filter rows where 'P_ISEV' indicates fatality (3)
fatality_df = df[df['P_ISEV'] == 3]

# Group by 'C_HOUR' and calculate the fatality rate for each hour
fatality_rate_by_hour = fatality_df.groupby('C_HOUR').size() / df.groupby('C_HOUR').size()

# Plot the fatality rate by hour
plt.bar(fatality_rate_by_hour.index, fatality_rate_by_hour.values)
plt.xlabel('Time of Day (Hour)')
plt.ylabel('Fatality Rate')
plt.title('Fatality Rate by Time of Day')
plt.xticks(fatality_rate_by_hour.index)

# Find the hour with the highest fatality rate
max_fatality_rate_hour = fatality_rate_by_hour.idxmax()
max_fatality_rate = fatality_rate_by_hour.max()

print(f"Time of Day Most Associated with High Fatality Rate:")
print(f"Hour: {max_fatality_rate_hour}, Fatality Rate: {max_fatality_rate:.2%}")

plt.show()

# %%
fatality_rate_by_hour

# %%
#numpy array to pandas dataframe
fatality_rate_by_hour = pd.DataFrame(fatality_rate_by_hour).reset_index()
fatality_rate_by_hour

# %%
# plot fatality_rate_by_hour using ggplot

X = fatality_rate_by_hour['C_HOUR']
Y = fatality_rate_by_hour[0]*100
p = ggplot(fatality_rate_by_hour, aes(x=X, y=Y)) + \
    geom_line(color = 'white') + \
    geom_point(color = 'red', size = 3) + \
    labs(x='Hour', y='Fatality rate (%)') + \
theme_classic() + \
    theme(
        axis_text_x = element_text(angle = 0, hjust = 1),
        axis_text_y = element_text(hjust = 1)
    ) + flavor_high_contrast_dark()
p

# %% [markdown]
# 2.3 What type(s) of weather are most associated with a relatively high fatality rate?

# %%
df = copy.deepcopy(data)

# %%
# Convert 'C_WTHR' and 'P_ISEV' columns to numeric
df['P_ISEV'] = pd.to_numeric(df['P_ISEV'], errors='coerce')

# Filter out rows where 'P_ISEV' indicates fatality (3)
fatality_df = df[df['P_ISEV'] == 3]
# fatality_df['C_WTHR'].replace({1 : 'Dry, normal', 2: 'Wet', 3: 'Snow', 4: 'Slush', 5: 'Icy', 6: 'Sand/gravel', 7: 'Muddy', 8: 'Oil', 9: 'Flooded', 'Q': 'other', 'U': 'Unknown'}, inplace=True)
# Group by 'C_WTHR' and calculate the fatality rate for each weather type
fatality_rate_by_weather = fatality_df.groupby('C_WTHR').size() / df.groupby('C_WTHR').size()

# Plot the fatality rate by weather type
# plt.figure(figsize=(10, 6))
# fatality_rate_by_weather.sort_values(ascending=False).plot(kind='bar')
# plt.xlabel('Weather Type')
# plt.ylabel('Fatality Rate')
# plt.title('Fatality Rate by Weather Type')
# plt.xticks(rotation=45)
# plt.tight_layout()

# Find the weather type with the highest fatality rate
max_fatality_rate_weather = fatality_rate_by_weather.idxmax()
max_fatality_rate = fatality_rate_by_weather.max()

print(f"Weather Type Most Associated with High Fatality Rate:")
print(f"Weather: {max_fatality_rate_weather}, Fatality Rate: {max_fatality_rate:.2%}")

# %%
fatality_rate_by_weather =  pd.DataFrame(fatality_rate_by_weather).reset_index()
fatality_rate_by_weather['C_WTHR'].replace({1 : 'Dry', 2: 'Wet', 3: 'Snow', 4: 'Slush', 5: 'Icy', 6: 'Sand/gravel', 7: 'Muddy', 8: 'Oil', 9: 'Flooded', 'Q': 'other', 'U': 'Unknown'}, inplace=True)
fatality_rate_by_weather

# %%
X = fatality_rate_by_weather['C_WTHR']
Y = fatality_rate_by_weather[0]*100
p = ggplot(fatality_rate_by_weather, aes(x=X, y=Y)) + \
    geom_lollipop(stat = 'identity', color = 'red', size = 2, fatten=3, stroke = 3, width = 0.1) + \
    labs(x='Weather', y='Fatality rate (%)') + \
theme_classic() + \
    theme(
        axis_text_x = element_text(angle = 0, hjust = 1),
        axis_text_y = element_text(hjust = 1), 
        axis_line_y= element_blank()
    ) + flavor_high_contrast_dark()
p

# %% [markdown]
# 2.3 What is the effect of using a Safety device on the fatality rate?

# %%
df = copy.deepcopy(data)

# %%
# Convert 'P_SAFE' and 'P_ISEV' columns to numeric
df['P_ISEV'] = pd.to_numeric(df['P_ISEV'], errors='coerce')

# Filter out rows where 'P_ISEV' indicates fatality (3)
fatality_df = df[df['P_ISEV'] == 3]

# Group by 'P_SAFE' and calculate the fatality rate for each safety device category
fatality_rate_by_safety = fatality_df.groupby('P_SAFE').size() / df.groupby('P_SAFE').size()

# Plot the fatality rate by safety device category
plt.figure(figsize=(10, 6))
fatality_rate_by_safety.sort_values(ascending=False).plot(kind='bar')
plt.xlabel('Safety Device')
plt.ylabel('Fatality Rate')
plt.title('Fatality Rate by Safety Device')
plt.xticks(rotation=45)
plt.tight_layout()

# Find the safety device with the highest fatality rate
max_fatality_rate_safety = fatality_rate_by_safety.idxmax()
max_fatality_rate = fatality_rate_by_safety.max()

print(f"Safety Device Most Associated with High Fatality Rate:")
print(f"Safety Device: {max_fatality_rate_safety}, Fatality Rate: {max_fatality_rate:.2%}")

plt.show()

# %%
fatality_rate_by_safety = pd.DataFrame(fatality_rate_by_safety).reset_index()
fatality_rate_by_safety['P_SAFE'].replace({1: 'No safety device', 
                                           2: 'Safety device used', 
                                           9: 'Helmet', 
                                           10: 'Reflective clothing', 
                                           11: 'Helmet & Reflective clothing', 
                                           12: 'Other safety device', 
                                           13: 'No safety device used  — buses', 
                                           'NN': 'Not applicable', 
                                           'QQ': 'Other', 
                                           'UU': 'Unknown',
                                           'XX': 'No data provided'
                                           }, inplace=True)
fatality_rate_by_safety

# %%
X = fatality_rate_by_safety['P_SAFE']
Y = fatality_rate_by_safety[0]*100
p = ggplot(fatality_rate_by_safety, aes(x=X, y=Y)) + \
    geom_lollipop(stat = 'identity', color = 'red', size = 2, fill = 'red', fatten=3, stroke = 3) + \
    labs(x='Safety Device', y='Fatality rate (%)') + \
theme_classic() + \
    theme(
        axis_text_x = element_text(angle = 90, hjust = 1),
        axis_text_y = element_text(hjust = 1), 
        axis_line_y=element_line(color='black', size=0.5)
    ) + flavor_high_contrast_dark() + ggsize(800, 600)
p

# %% [markdown]
# Road Alignment & Collision Configuration

# %%
df = copy.deepcopy(data)

# %%
#Prepare the dataset for analyse, replace non-numeric value into number to use in scatter plot.
df1 = df.loc[:,['C_RALN','C_CONF']]
df1.C_RALN = df1.C_RALN.replace({'Q':7,'U':8}).astype(int)
df1.C_CONF = df1.C_CONF.replace({'QQ':42,'UU':43,'XX':43}).astype(int)

# %%
#Too many collision configuration involved, iterate a list of dateframes to
# separate different collision config.
df6 = []
df6.append( df1[df1.C_CONF < 10] )
df6.append( df1[(df1.C_CONF > 20)&(df1.C_CONF < 30)] )
df6.append( df1[(df1.C_CONF > 30)&(df1.C_CONF < 40)] )
df6.append( df1[df1.C_CONF > 40] )


# %%
#Reformat the dataframe, to summarize the collision numbers in different situation,
# and store in another list of dataframe 'df7'

se6 = []; df7 = []
for i in range(0,4):
    se6.append( df6[i].groupby(['C_RALN','C_CONF']).size() )
    se6[i].name = 'collision'
    df7.append( pd.DataFrame(se6[i]).reset_index() )

df7[3]

# %%


# %%
#Draw four subplots to show the relation between the road alignment
# and different collision situations.

fig = plt.figure(figsize=(15, 10))
fig.suptitle("The Relation between Road-alignment and Collision-configuration",
             fontsize = 16)

#---------------------- Only one car involved in collision. ---------------------- 
ax1 = fig.add_subplot(2,2,1)
ax1.set_xticks(range(1,9))
ax1.set_xticklabels([1,2,3,4,5,6,'Q','U'])
ax1.set_xlabel("Road Alignment")

ax1.set_yticks(range(1,7))
ax1.set_yticklabels(['Person/animal','Station/tree','Left-roll',
                     'Right-roll','Rollover','Other'])
ax1.set_ylabel("Collision Configure")

ax1.set_title("Single Vehicle in Motion")
ax1.scatter(df7[0].C_RALN,df7[0].C_CONF,
            df7[0].collision*.01,
            alpha=0.5,color='r')
plt.grid(which='major')

#---------------------- Two car same direction. ---------------------- 
ax2 = fig.add_subplot(2,2,2)
ax2.set_xticks(range(1,9))
ax2.set_xticklabels([1,2,3,4,5,6,'Q','U'])
ax2.set_xlabel("Road Alignment")


ax2.set_ylim([19.5,25.5])
ax2.set_yticks(range(21,26))
ax2.set_yticklabels(['Rear-end','Side-swipe','Left-turn','Right-turn','Other'])
ax2.set_ylabel("Collision Configure")

ax2.set_title("Two Vehicle Same Direction")
ax2.scatter(df7[1].C_RALN,df7[1].C_CONF,
            df7[1].collision*.01,
            alpha=0.5,color='r')
plt.grid(which='major')

#---------------------- Two car different direction. ---------------------- 
ax3 = fig.add_subplot(2,2,3)
ax3.set_xticks(range(1,9))
# ax3.set_xticklabels(C_RALN,rotation=30,ha='right')
ax3.set_xlabel("Road Alignment")

ax3.set_ylim([30.5,37])
ax3.set_yticks(range(31,37))
ax3.set_yticklabels(['Head-on','Side-swipe','Left-turn','Right-turn',
                     'Right-angle','Other'])
ax3.set_ylabel("Collision Configure")

ax3.set_title("Two Vehicle Different Direction")
ax3.scatter(df7[2].C_RALN,df7[2].C_CONF,
            df7[2].collision*.01,
            alpha=0.5,color='r')
plt.grid(which='major')

#---------------------- Other situation. ---------------------- 
ax4 = fig.add_subplot(2,2,4)
ax4.set_xticks(range(1,9))
# ax4.set_xticklabels(C_RALN,rotation=30,ha='right')
ax4.set_xlabel("Road Alignment")

ax4.set_ylim([40.7,43.3])
ax4.set_yticks(range(41,44))
ax4.set_yticklabels(['Parked car','Other','Unknown'])
ax4.set_ylabel("Collision Configure")

ax4.set_title("Other Situation")
ax4.scatter(df7[3].C_RALN,df7[3].C_CONF,
            df7[3].collision*.01,
            alpha=0.5,color='r')
plt.grid(which='major');

# %% [markdown]
# Single Veichle in motion

# %%
# replace data labels with actual labels
df7[0]['C_CONF'].replace({1: 'moving object', 2: 'stationary object', 3: 'Ran off left', 4: 'Ran off right ', 5: 'Rollover', 6: 'other'}, inplace=True)
df7[0]['C_RALN'].replace({1: 'straight', 2: 'straight—gradient', 3: 'curve-level', 4: 'curved-gradient', 5: 'hill', 6: 'Sag', 7: 'other', 8: 'unknown'}, inplace=True)

# %%
# scatter plot of df7[0] using ggplot2
x = df7[0]['C_RALN']
y = df7[0]['C_CONF']
collisions = df7[0]['collision']
p = ggplot(df7[0], aes(x=x, y=y, size = collisions)) + geom_point(color = 'red') + scale_fill_gradient(low = "white", high = "red") + \
    theme_classic() + flavor_high_contrast_dark() +\
        scale_size_area(max_size=15) +theme(legend_position='none') + \
            labs(x = 'Road Alignment', y = 'Road Configuration', size = 'Collisions') + \
            ggtitle('Single Veichle in motion') + ggsize(800, 500)
p

# %% [markdown]
# Two car same direction.

# %%
#df7[1]

# %%
# replace data labels with actual labels
df7[1]['C_CONF'].replace({21: 'Rear-rendered', 22: 'Side swipe', 23: 'left turn conflict', 24: 'right turn conflict', 25: 'same direction '}, inplace=True)
df7[1]['C_RALN'].replace({1: 'straight', 2: 'straight—gradient', 3: 'curve-level', 4: 'curved-gradient', 5: 'hill', 6: 'Sag', 7: 'other', 8: 'unknown'}, inplace=True)

# %%
x = df7[1]['C_RALN']
y = df7[1]['C_CONF']
collisions = df7[1]['collision']
p = ggplot(df7[1], aes(x=x, y=y, size = collisions)) + geom_point(color = 'red') + scale_fill_gradient(low = "white", high = "red") + \
    theme_classic() + flavor_high_contrast_dark() +\
        scale_size_area(max_size=15) +theme(legend_position='none') + \
            labs(x = 'Road Alignment', y = 'Road Configuration', size = 'Collisions') + \
            ggtitle('Two Cars in the same direction') + ggsize(800, 500)
p

# %% [markdown]
# Two cars in different directions

# %%
# df7[2]

# %%
# replace data labels with actual labels
df7[2]['C_CONF'].replace({31: 'head-on', 32: 'side swipe', 33: 'left turn conflict', 34: 'right turn conflict', 35: 'right angle', 36: 'other'}, inplace=True)
df7[2]['C_RALN'].replace({1: 'straight', 2: 'straight—gradient', 3: 'curve-level', 4: 'curved-gradient', 5: 'hill', 6: 'Sag', 7: 'other', 8: 'unknown'}, inplace=True)

# %%
x = df7[2]['C_RALN']
y = df7[2]['C_CONF']
collisions = df7[2]['collision']
p = ggplot(df7[2], aes(x=x, y=y, size = collisions)) + geom_point(color = 'red') + scale_fill_gradient(low = "white", high = "red") + \
    theme_classic() + flavor_high_contrast_dark() +\
        scale_size_area(max_size=15) +theme(legend_position='none') + \
            labs(x = 'Road Alignment', y = 'Road Configuration', size = 'Collisions') + \
            ggtitle('Two cars in different directions') + ggsize(800, 500)
p

# %% [markdown]
# Other situations

# %%
# replace data labels with actual labels
df7[3]['C_CONF'].replace({41: 'parked motor vehicle', 42: 'other', 43: 'unknown', 44: 'not available'}, inplace=True)
df7[3]['C_RALN'].replace({1: 'straight', 2: 'straight—gradient', 3: 'curve-level', 4: 'curved-gradient', 5: 'hill', 6: 'Sag', 7: 'other', 8: 'unknown'}, inplace=True)

# %%
x = df7[3]['C_RALN']
y = df7[3]['C_CONF']
collisions = df7[3]['collision']
p = ggplot(df7[3], aes(x=x, y=y, size = collisions)) + geom_point(color = 'red') + scale_fill_gradient(low = "white", high = "red") + \
    theme_classic() + flavor_high_contrast_dark() +\
        scale_size_area(max_size=15) +theme(legend_position='none') + \
            labs(x = 'Road Alignment', y = 'Configuration', size = 'Collisions') + \
            ggtitle('Other situations') + ggsize(800, 500)

p

# %% [markdown]
# How fatality rates vary by weather conditions and time of day simultaneously,

# %%
df = copy.deepcopy(data)

# %%
df['C_HOUR'].unique()

# %%
df['P_ISEV'].unique()

# %%
df['P_AGE'].unique()

# %%
df = df[df['P_AGE']!= 'UU']
df = df[df['P_AGE']!= 'NN']
df = df[df['P_ISEV']!= 'U']
df = df[df['P_ISEV']!= 'N']
df = df[df['P_SEX']!= 'U']

# Convert columns to numeric
df['P_AGE'] = pd.to_numeric(df['P_AGE'])
df['P_ISEV'] = pd.to_numeric(df['P_ISEV'])

# Define age ranges
age_ranges = [(0, 14), (15, 24), (25, 34), (35, 44), (45, 54), (55, 64), (65, 74), (75, 100)]

# Create a new column 'AgeRange' based on age ranges
df['AgeRange'] = pd.cut(df['P_AGE'], bins=[age[0] for age in age_ranges] + [age_ranges[-1][1]], labels=[f'{age[0]}-{age[1]}' for age in age_ranges])

# Filter the DataFrame to consider only fatality cases (P_ISEV == 3)
fatality_df = df[df['P_ISEV'] == 3]

# Group by AgeRange and P_SEX, and calculate fatality rates
grouped = fatality_df.groupby(['AgeRange', 'P_SEX']).size().unstack(fill_value=0)
grouped = grouped.div(grouped.sum(axis=1), axis=0) * 100  # Convert to percentages

# Find the age range and sex with the highest fatality rate
max_fatality_rate = grouped.max().max()
max_fatality_idx = grouped.stack().idxmax()

print(f"The age range and sex more likely to be associated with high fatality:")
print(f"Age Range: {max_fatality_idx[0]}, Sex: {max_fatality_idx[1]}")
print(f"Fatality Rate: {max_fatality_rate:.2f}%")

# %%


# %%
grouped.reset_index(drop=False, inplace=True)

# %%
grouped.reset_index().melt(id_vars=['index', 'AgeRange'], var_name='Gender', value_name='Percentage')
grouped.head()

# %%
df_f = grouped[['AgeRange', 'F']].rename(columns={'F': 'Percentage', 'AgeRange': 'AgeRange', 'M': 'F'})
df_m = grouped[['AgeRange', 'M']].rename(columns={'M': 'Percentage', 'AgeRange': 'AgeRange', 'F': 'M'})


# %%
df_f['Gender'] = 'F'
df_m['Gender'] = 'M'

# %%
df = pd.concat([df_f, df_m])
df

# %%
p = ggplot(df, aes(x='AgeRange', y='Percentage', fill='Gender')) + \
    geom_bar(stat='identity', position='dodge') + \
    scale_fill_brewer(type='qual', palette='Set2') + \
    labs(x='Age Range', y='Fatality Rate (%)', title='Fatality Rates by Age Range and Sex') + \
    theme_classic() + flavor_high_contrast_dark() + \
        theme(
        axis_text_x = element_text(angle = 0, hjust = 1),
        axis_text_y = element_text(hjust = 1), 
        axis_line_y=element_line(color='black', size=0.5)
    )

# Show the plot
p

# %%
groupped

# %%
df = df[df['P_AGE']!= 'UU']
df = df[df['P_AGE']!= 'NN']
df = df[df['P_ISEV']!= 'U']
df = df[df['P_ISEV']!= 'N']
df = df[df['P_SEX']!= 'U']
df = df[df['C_HOUR']!= 'UU']

# Convert columns to numeric
df['P_AGE'] = pd.to_numeric(df['P_AGE'])
df['C_HOUR'] = pd.to_numeric(df['C_HOUR'])
df['P_ISEV'] = pd.to_numeric(df['P_ISEV'])

# Define age ranges
age_ranges = [(0, 14), (15, 24), (25, 34), (35, 44), (45, 54), (55, 64), (65, 74), (75, 100)]

# Create a new column 'AgeRange' based on age ranges
df['AgeRange'] = pd.cut(df['P_AGE'], bins=[age[0] for age in age_ranges] + [age_ranges[-1][1]], labels=[f'{age[0]}-{age[1]}' for age in age_ranges])

# Filter the DataFrame to consider only fatality cases (P_ISEV == 3)
fatality_df = df[df['P_ISEV'] == 3]

# Group by AgeRange, P_SEX, and C_HOUR, and calculate fatality rates
grouped = fatality_df.groupby(['AgeRange', 'P_SEX', 'C_HOUR']).size().unstack(fill_value=0)
grouped = grouped.div(grouped.sum(axis=1), axis=0) * 100  # Convert to percentages

# Find the age range, sex, and hour with the highest fatality rate
max_fatality_rate = grouped.max().max()
max_fatality_idx = grouped.stack().idxmax()

print(f"The age range, sex, and hour more likely to be associated with high fatality:")
print(f"Age Range: {max_fatality_idx[0]}, Sex: {max_fatality_idx[1]}, Hour: {max_fatality_idx[2]}")
print(f"Fatality Rate: {max_fatality_rate:.2f}%")

# %%
grouped.reset_index(drop=False, inplace=True)

# %%
grouped

# %%
df = copy.deepcopy(data)

# %%
df.columns

# %%
df = df[df['P_AGE']!= 'UU']
df = df[df['P_AGE']!= 'NN']
df = df[df['P_ISEV']!= 'U']
df = df[df['P_ISEV']!= 'N']
df = df[df['P_SEX']!= 'U']


relevant_columns = ['P_SEX', 'P_AGE', 'C_SEV']
filtered_df = df[relevant_columns]

# Filter out rows with unknown gender and non-numeric ages
# filtered_df = filtered_df[filtered_df['P_SEX'].isin(['M', 'F'])]
# filtered_df = filtered_df[filtered_df['P_AGE'].str.isnumeric()]

# Convert 'P_AGE' to numeric
# Convert 'P_AGE' to numeric
filtered_df['P_AGE'] = pd.to_numeric(filtered_df['P_AGE'])

# Group by age, gender, and calculate fatality rates
grouped_df = filtered_df.groupby(['P_AGE', 'P_SEX']).agg(
    Total=('P_SEX', 'count'),
    Fatalities=('C_SEV', lambda x: (x == 1).sum())
).reset_index()

grouped_df['Fatality Rate'] = (grouped_df['Fatalities'] / grouped_df['Total']) * 100

# Plot fatality rates by age and gender
plt.figure(figsize=(10, 6))
for gender in ['M', 'F']:
    gender_data = grouped_df[grouped_df['P_SEX'] == gender]
    plt.plot(gender_data['P_AGE'], gender_data['Fatality Rate'], label=gender)
plt.xlabel('Age')
plt.ylabel('Fatality Rate (%)')
plt.title('Fatality Rates by Age and Gender')
plt.legend()
plt.grid(True)
plt.show()

# %%
grouped_df

# %%
x = grouped_df['P_AGE']
y = grouped_df['Fatality Rate']
c = grouped_df['P_SEX']
p = ggplot(grouped_df, aes(x=x, y=y, color = c)) + geom_line()
p

# %% [markdown]
# Explore how different vehicle types ('V_TYPE') and collision configurations ('C_CONF') contribute to collision severity or fatality rates.

# %%
df = copy.deepcopy(df)

# %%
df['V_TYPE'].unique()

# %%
df['C_SEV'].unique()

# %%
df['C_CONF'].unique()

# %%

df = df[df['V_TYPE']!= 'UU']
df = df[df['V_TYPE']!= 'NN']
df = df[df['V_TYPE']!= 'QQ']


# Filter relevant columns
relevant_columns = ['V_TYPE', 'C_CONF', 'C_SEV']
filtered_df = df[relevant_columns]

# Group by 'V_TYPE' and 'C_CONF' and calculate relevant metrics
grouped_df = filtered_df.groupby(['V_TYPE', 'C_CONF']).agg(
    Total=('V_TYPE', 'count'),
    Fatalities=('C_SEV', lambda x: (x == 1).sum())
).reset_index()

# Calculate fatality rates within each group
grouped_df['Fatality Rate'] = (grouped_df['Fatalities'] / grouped_df['Total']) * 100

# Convert numeric columns to strings for concatenation
grouped_df['V_TYPE_C_CONF'] = grouped_df['V_TYPE'].astype(str) + ' - ' + grouped_df['C_CONF'].astype(str)

# Plotting
plt.figure(figsize=(12, 6))
plt.bar(grouped_df['V_TYPE_C_CONF'], grouped_df['Fatality Rate'])
plt.xticks(rotation=90)
plt.xlabel('Vehicle Type - Collision Configuration')
plt.ylabel('Fatality Rate (%)')
plt.title('Fatality Rates by Vehicle Type and Collision Configuration')
plt.tight_layout()
plt.show()


# %%
grouped_df.head(10)

# %%
# filter only common collisions 6, 2, 21, 33, 35, 36, QQ, UU
grouped_df = grouped_df[grouped_df['C_CONF'].isin([6, 2, 21, 33, 35, 36])]

# %%
# Aggregate data to calculate overall fatality rate for each 'V_TYPE'
overall_grouped_df = grouped_df.groupby('V_TYPE').agg(
    Total=('Total', 'sum'),
    Fatalities=('Fatalities', 'sum')
).reset_index()

overall_grouped_df['Fatality Rate'] = (overall_grouped_df['Fatalities'] / overall_grouped_df['Total']) * 100
overall_grouped_df['V_TYPE'].astype('category')

p = ggplot(grouped_df) + \
    geom_bar(aes(x='V_TYPE_C_CONF', y='Fatality Rate', color='V_TYPE'), stat='identity', position='dodge', color = 'orange', fill = 'black') + \
    theme(axis_text_x=element_text(angle=90, hjust=1)) + \
    labs(x='Vehicle Type - Collision Configuration', y='Fatality Rate (%)', title='Fatality Rates by Vehicle Type and Collision Configuration') + \
        theme_classic() + flavor_high_contrast_dark() + \
        theme(
        axis_text_x = element_text(angle = 90, hjust = 1, size = 7),
        axis_text_y = element_text(angle = 0, hjust = 1), 
        axis_line_y=element_line(color='black', size=0.5)
    ) + theme(legend_position='none')

# Show the plot
p

# %%
pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)

# %%
print(grouped_df)

# %%



