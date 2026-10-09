#Where is the best municipality to live in Slovenia?
#210/212 municipalities analysed, due to missing data from two municipalities:
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#importing and cleaning the data

df = pd.read_excel("slovenia_place_data.xlsx",
                   header = None,
                   usecols = [0, 1, 2],
                   names = ["measure", "municipality", "value"],
                   )

df = df.dropna(subset = ["municipality"])

df["measure"] = df["measure"].ffill()
df["value"] = pd.to_numeric(df["value"], errors = "coerce")
wide_df = df.pivot(index = "municipality", columns = "measure", values = "value")
wide_df = wide_df.dropna()
wide_df = wide_df.rename(columns = {"Population - Total - 1 January" : "Population",
                                    "Natural increase per 1,000 population" : "Nat Inc",
                                    "Total net migration per 1,000 population" : "Migration",
                                    "Ageing index - 1 January" : "Age idx",
                                    "Number of schools" : "Schools",
                                    "Employment rate (%)" : "Employment",
                                    "Average monthly gross earnings (index SI=100)" : "Gross Inc %"})

#Analysing and weighting data

#We will standardise all data to Z values to give each measure a fair weight

population = np.log(wide_df["Population"]) #Log so that high population doesn't skew results
natinc = wide_df["Nat Inc"]
migration = wide_df["Migration"]
age = wide_df["Age idx"]
schools = wide_df["Schools"]
employment = wide_df["Employment"]
income = wide_df["Gross Inc %"]

def z(measure, cutoff = 2.5):
    non_outliers = []
    mean = np.mean(measure)
    sd = np.std(measure)
    
    for i in measure:
        if i < mean + cutoff*sd and i > mean - cutoff*sd:
            non_outliers.append(i)
    true_mean = np.mean(non_outliers)
    true_sd = np.std(non_outliers)
    
    z = (measure - true_mean)/true_sd
    z = np.clip(z, -3, 3)
    return z

z_population = z(population)
z_natinc = z(natinc)
z_migration = z(migration)
z_age = z(age) 
z_schools= z(schools)
z_employment = z(employment)
z_income = z(income)

#Calculating overall score for each municipality

pop_w = input("from 1-10, how much do you value a high population?")
natinc_w = input("from 1-10, how much do you value a high natural increase?")
migration_w = input("from 1-10, how much do you value a high migration?")
age_w = input("from 1-10, how much do you value a less elderly place?")
schools_w = input("from 1-10, how much do you value a high number of schools?")
employment_w = input("from 1-10, how much do you value a high employment level?")
income_w = input("from 1-10, how much do you value a high income place?")

#subtracting age here because a younger population is better
wide_df["score"] = (int(pop_w)*z_population + int(natinc_w)*z_natinc + int(migration_w)*z_migration - (int(age_w)*z_age) + int(schools_w)*z_schools + int(employment_w)*z_employment + int(income_w)*z_income)

#Sorting in descending order
wide_df = wide_df.sort_values("score", ascending = False)
wide_df = wide_df.reset_index()

pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)

#printing all results
print(wide_df[["municipality", "score"]] )

#If you want to search an index use this:
#print(wide_df.iloc[20]["score"])

#If you want to search a municipality use this:
#print(wide_df[wide_df["municipality"] == "Bled"])

#Presenting the data

#Printing top 10 into bar chart

x = wide_df["municipality"].head(10)
y = wide_df["score"].head(10)

plt.bar(x, y)
plt.xlabel("Municipality")
plt.ylabel("Score")
plt.title("Slovenian Municipality Scores")
plt.xticks(rotation = 45, ha = "right")
plt.tight_layout()
plt.show()








    
        
