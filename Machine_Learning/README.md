
# Weather_Data_Analysis
=======
# MAchine-learning seasons for Weather_Data_Analysis


 Daily weather data is aggreated into approximately 10-day blocks like "early march" or "late february" or "mid-june". Averages *and standard deviations* of some weather statistics are computed for each block, for each year. This data, with one row for each block in each year in the historical record, is then fed into PCA and then K-Means clustering, to produce a label for each row. Our model's first guess for the labels for each of the 36 date blocks is the modes of the labels across the years; an ad-hoc smoothing procedure is then applied to produce meaningful contiguous seasons, while changing as little as possible. We run several models, and then automatically picked the one that produced the nicest-looking results with the least amount of ad-hoc smoothing.



## Current files

- GetCleanData is identical to the one used for the deployed website. Ideally, ML_func_happy.py should be edited to refer to that file, and the copy in this directory should be deleted.

- ML_func_happy.py contains all the machine-learning code.

- ML demo.ipynb is where you can play.



## Work needed.

(1-3 done)

4. Aggregate weather statistics for each season and get adjectives for them; like we did for historical summaries.

5. Produce concise report table/dictionary, like:<br>
"From mid-november to late-march, it's cold and rainy in SF, and can be both windy and not windy."

6. Design and implement a js-plotly version of the circle of colored dots to be displayed on the website. To make sense to user, label months, and choose meaningful colors: green rainy, red hot, blue cold, white snowy, etc.





