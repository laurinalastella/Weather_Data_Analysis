# Data getting and cleaning for Weather_Data_Analysis


 Use Alice_making_fivecities notebook to quickly get a csv file with summary historical statistics for any number of cities, for the time period from 2010-01-01 to 2019-12-31. Instructions:
1. Run the import cell at the top.
2. Uncomment and run the second cell, to initialize output file.
3. Recomment the second cell.
4. For each location, enter the city and the country into the third cell and run all cells in the notebook at add a line to the output file for that location.

  Known issues:
 - There is no way to input the state for the location, so only one "Spingfield, US" or "Oakland, US" is possible.
 - The output file has a stray character at the beginning: delete that ',' manually before using the csv.


 The AliceGetDataCleanData notebook has more readability and functionality, but less user-friendliness. In particular, an outer wrapper function is currently missing. 

## Next Steps

In order of decreasing urgency and likelihood of getting done.

 - add a way to enter the state part of location

 - add location in some form(s) to the output dictionary. options:
  - input strings,
  -  or latt/long obtained from positionstack.com,
  -  or latt/long obtained from the weather API - not the same!

 - turn the notebook into a .py file with functions, to enable data-getting from command line or flask app; and a separate testing notebook importing those functions.

 - add attributions: in code, in readme, in output ?

 - add error-handling

 - clean up some of the spaghetti...

(Further aggregation needed for machine learning will be done in that code, not here.)



