
# Weather_Data_Analysis
=======
# MAchine-learning seasons for Weather_Data_Analysis


 The current approach segments annual data into approximately 10-day blocks like "early march" or "late february" or "mid-june". Averages *and standard deviations* of some weather statistics are computed for each block, for each year. This data, with one row for each block in each year in the historical record, is then fed into PCA and then K-Means clustering, to produce a label for each row. Labels are then aggregated across years using mode to obtain 36 labels, one for each block, independent of year. The hope is that these clusters will be sufficiently convex on the date circle to call them seasons. Preliminary investigations give reasonable outputs for Chicago and San Francisco - even identifying "fogust" in SF!

## Current files

- GetCleanData is many commits behind Laurina's error-handling, spellcecked version; but works with this code.
- ML_functions is very finalized, except the smoothing functions need to go through head and maybe fingers one more time: there's some crashing, and distance is computed from unscaled data, so is mostly garbage.
- bugfree_smoothing.ipynb  is where I/you play/test ML_functions.
- bugfree_smoothing.html is for Oct 14 presentation.


## Work needed.

1. Update code to work with the new iteration of Data Cleaning, to make API calls rather than rely on static csv files. DONE

2. Automate choosing best hyper-parameters: 
 - the number of components from PCA, currently 20; and
 - the number of clusters: 4-6 seems pretty good. DONE

3. Automate smoothing the result, like recoloring isolated points inside otherwise convex other-colored season. DONE-ish

4. Aggregate weather statistics for each season and get adjectives for them; like we did for historical summaries. TODO

5. Produce concise report table/dictionary, like:<br>
"From mid-november to late-march, it's cold and rainy in SF, and can be both windy and not windy." TODO

6. User-facing version of pretty colored circle?
 - label dates on it
 - re-color with meaningful colors (green rainy, red hot, blue cold, white snowy, etc)
 - push picture out through flask; or, more likely, push data out through slack and remake picture with js. WISHFUL THINKING





