# MAchine-learning seasons for Weather_Data_Analysis


 The current approach segments annual data into approximately 10-day blocks like "early march" or "late february" or "mid-june". Averages *and standard deviations* of some weather statistics are computed for each block, for each year. This data, with one row for each block in each year in the historical record, is then fed into PCA and then K-Means clustering, to produce a label for each row. Labels are then aggregated across years using mode to obtain 36 labels, one for each block, independent of year. The hope is that these clusters will be sufficiently convex on the date circle to call them seasons. Preliminary investigations give reasonable outputs for Chicago and San Francisco - even identifying "fogust" in SF!!

## Work needed.

1. Update code to work with the new iteration of Data Cleaning, to make API calls rather than rely on static csv files.

2. Automate choosing best hyper-parameters: 
 - the number of components from PCA, currently 20; and
 - the number of clusters: 4-6 seems pretty good.

3. Automate smoothing the result, like recoloring isolated points inside otherwise convex other-colored season.

4. Aggregate weather statistics for each season and get adjectives for them; like we did for historical summaries.

5. Produce consice report table/dictionary, like:<br>
"From mid-november to late-march, it's cold and rainy in SF, and can be both windy and not windy."




