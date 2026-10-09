# Slovenia-Municipality-Ranking

Gives the user a top 10 of Slovenian municipalities to live in based on their inputs.

Data from:

https://pxweb.stat.si/SiStatData/pxweb/en/Data/Data/2640010S.px/table/tableViewLayout2/?loadedQueryId=1843&timeType=item

Libraries: Pandas, NumPy, Matplotlib

<img width="425" height="281" alt="Slovenia_livability_result" src="https://github.com/user-attachments/assets/4e62939a-7807-4757-a992-8318219ab012" />


The image above is the result with my input choice, however the data presented may differ based on different weights chosen by the user.

## Method

First, I found the national government data for Slovenian municipalities and selected categories to determine the livability of each municipality.

Next, I copied the data into an Excel file and read it with pandas.

Then, I cleaned the data with pandas by removing the NaNs, taking just the first 3 columns, filling the measure column with `ffill()`, and changing the data frame (`df`) from "long" to "wide" (`wide_df`) by swapping the measure column into a top row.

Then, I renamed all of the measures to shorten them, took the log of each population in order to limit its skew, and made a z function to standardise the data, removing outliers above or below 2.5 standard deviations from the mean and using NumPy to clip each measure at -3 and +3.

Once the data was standardised, it was ready to be used to calculate the municipality score:

`score = (
    int(pop_w) * z_population
    + int(natinc_w) * z_natinc
    + int(migration_w) * z_migration
    - int(age_w) * z_age
    + int(schools_w) * z_schools
    + int(employment_w) * z_employment
    + int(income_w) * z_income`

Anything ending in `w` is the user's inputted value of the measure, and anything containing `z` is the standardised value for each municipality. Age was subtracted from the score since a higher proportion of older people is assumed to be a negative influence on a municipality.

Then, I used matplotlib to plot the top 10 highest scoring municipalities on a bar chart, labelling each axis and rotating each municipality name by 45 degrees in order to fit them all.

## Findings

Something very interesting I found was that in the majority of cases, the most "livable" municipality was Novo Mesto rather than my expected result of Ljubljana (though it frequently made the top 10).

One reason why Ljubljana may not have made top place is that its result was labelled an "outlier" as the most populous city by far.

## Limitations

Firstly, only 7 measures of data were used. A true livability score would take into account more measures to come to a more accurate conclusion.

Secondly, livability is subjective, and while my code allows the user to choose the weights, a precise weight is difficult for a user to know.

Thirdly, only 210 out of 212 municipalities were analysed because 2 municipalities were missing data.

Finally, by removing outliers and clipping from -3 to 3, I may have removed data that could have had significant impacts on the rankings.



