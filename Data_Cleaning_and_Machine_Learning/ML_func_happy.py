#import requests
import pandas as pd
#import json
import datetime
import numpy as np
# for position API
#import http.client, urllib.parse

# ML imports
from sklearn.preprocessing import MinMaxScaler
from sklearn.decomposition import PCA
from math import radians, cos, sin
from sklearn.cluster import KMeans
from scipy.spatial.distance import cdist
# import hvplot.pandas

# my own data-getting, data-cleaning code
import GetCleanData as gcda

#   Main functions:
#   step1 gets data from API via GetCleanData and date-chunkifies it
#   step2 prepares the data for clustering: rescales and puts dates on a circle


#           ----    Step1       ----

## rem is 0 for days 1-10, 1 for days 11-20, and 2 for days 21-
## the function returns 1 for 01/01-01/10, 6 for 02/21-02/29, and so on.
def chunkify(date):
    rem = min( (date.day-1) // 10, 2)
    return ( date.month *3  + rem -2 )

# both input years included: enter same for 1 year
def step1(latitude, longitude, start_year, end_year):
    daf = gcda.get_clean_weather(latitude, longitude, start_year, end_year)
    keepers = ['pure_date', 'humid_avg', 'wind_high', 'median_wind',
               'cloud_4', 'cloud_12','cloud_20', 'precipitation_hours', 'rain_sum',
               'snowfall_sum', 'temperature_2m_max', 'temperature_2m_min']
    daf = daf[keepers]
    shorter_names = {'temperature_2m_max': 'temp_max', 'temperature_2m_min':'temp_min', 'precipitation_hours':'precip_hrs'}
    daf.rename(columns=shorter_names, inplace=True)
    # chunkify dates
    daf['date_chunk'] = daf["pure_date"].map(chunkify)
    daf['year'] = daf["pure_date"].map(lambda x: x.year)
    daf.drop('pure_date', axis=1, inplace=True)
    # aggregate averages
    avg_df = daf.groupby(['year', 'date_chunk']).agg(np.mean)
    avg_df.reset_index(inplace=True)
    # aggregate standard deviations
    dev_df = daf.groupby(['year', 'date_chunk']).agg(np.std)
    dev_df.reset_index(inplace=True) 
    # join the two aggregates
    unscaled_df = avg_df.join(dev_df, rsuffix='_dev', lsuffix='_avg')
    # cosmetic post-join cleanup
    unscaled_df.drop(['year_dev', 'date_chunk_dev'], axis=1, inplace=True)
    unscaled_df.rename(columns = {'year_avg':'year', 'date_chunk_avg': 'date_chunk'}, inplace = True)
    return unscaled_df

#           ----    Step2       ----

# wrapper for everything below it
# unscaled_df is the output of step1
# comps is the number of principal components kept
# returns pair:
#  one df with columns 'xchunk', 'ychunk', and 'PC 11' for various 11s
#  other df with scaled, not PCA'ed data for computing distance matrices below

def step2(unscaled_df, comps):
    # scale weather data, forgetting dates
    scaled_df = rescale(unscaled_df)
    # run PCA on scaled weather data
    pcs_df = make_pca(scaled_df, comps)
    # convert integer date chunks to coordinates of points on a circle
    date_coord_df = dates_to_circle(unscaled_df[['date_chunk']])
    # combine PCA output with dates
    pcs_df['xchunk'] = date_coord_df['xchunk']
    pcs_df['ychunk'] = date_coord_df['ychunk']
    # return stuff ready for clustering
    return (pcs_df, scaled_df)

# adds circle-coordinate columns 'xchunk', 'ychunk' to input df
# based on input-df's existing 'date_chunk" column.
# date chunks z run from 1 to 36; so 10*z in degrees is equispaced on circle
def dates_to_circle(date_chunks_df):
    daf = date_chunks_df.copy()
    # put date chunks on circle
    daf['xchunk'] =     daf['date_chunk'].map(lambda z: sin(radians(10*z)) )
    daf[
        'ychunk'] =     daf['date_chunk'].map(lambda z:  cos(radians(10*z)) )
    # drop original integers
    # daf.drop('date_chunk', axis=1, inplace=True)
    return daf

# input: dataframe to be scaled, shaped like output of step1
# output: scaled dataframe with no date info, ready to be fed into PCA
def rescale(scaling_df):
    # build scaled_df with only weather
    #   auto-rescale standard deviation columns with MinMaxScaler
    dev_cols = ['temp_max_dev', 'temp_min_dev', 'rain_sum_dev', 'snowfall_sum_dev',
                'precip_hrs_dev', 'humid_avg_dev', 'median_wind_dev',
                'wind_high_dev', 'cloud_4_dev', 'cloud_12_dev', 'cloud_20_dev']
    X = scaling_df[dev_cols]
    scaler = MinMaxScaler()
    scaledata = scaler.fit_transform(X)
    # make new df to hold scaled data
    scaled_df = pd.DataFrame(scaledata, columns = dev_cols)
    #   hand-rescale averages to send "normal" ranges [0,max] to [0, 1]
    avg_maxes = {'temp_max_avg':100, 'temp_min_avg':100, 'humid_avg_avg':100,
                 'cloud_4_avg':100, 'cloud_12_avg':100, 'cloud_20_avg':100,
                 'precip_hrs_avg':24, 'rain_sum_avg':0.5 , 'snowfall_sum_avg':12,
                 'median_wind_avg':15, 'wind_high_avg':25}
    # rescale averages, add them into new df
    for colnam in avg_maxes.keys():
        scaled_df[colnam] = scaling_df[colnam].map(lambda x: (x / avg_maxes[colnam]) )
    return scaled_df 

# generating column names for the dataframe containing components, used in make_pca
def pc_cols(k):
    out = []
    for i in range(k):
        out.append('PC '+str(i))
    return out

# returns df with columns 'PC 11' for various 11s, and sequential index
def make_pca(scaled_df, comps):
    pca = PCA(n_components=comps)
    pca_out = pca.fit_transform(scaled_df)
    pcs2_df = pd.DataFrame(pca_out, columns = pc_cols(comps))
    # next two lines for debugging, remove in production!!
    for k in range(5):
        print(5+k, "principal components explain", sum(pca.explained_variance_ratio_[:5+k]))
    return pcs2_df


#           ----    Step3       ----

# We fit several models, varying hyper-parameters:
#  number of clusters, weight of dates; maybe randostate, maybe more.
# For each model, we produce:
#  - df with same index as all before, with labels for each (date chunks, year);
#  - distance matrix based on (post-pca !) cluster centers, only weather columns.
# Aggregation into total of 36 rows in not here.

#         one_model function
# ==> the first three inputs are passed-by-reference AND MODIFIED
# the first one (for_clusters_df) is reset
# the others are storage spaces for output, each gains new data
# a column named smth like "season k4 w1.2 r17" for many_labels_df
# an item with key like "season k4 w1.2 r17" for the distionary dist_matrices

# the column is the output of K-Means cluster algorithm run on
# the data in for_clusters_df with random state = randosta, and
# k clusters, date-coordinates weighted by w
# the value in the dictionary is the distance matrix:
# dist_matrices["season k4 w1.2 r17"][2][3] 
# is the distance between seasons 2 and 3, out of 0,1,2,3

# the name is for example "season k4 w1.2 r17" when
# there are 4 clusters, weight of dates is 1.2, and random state is 17

def one_model(for_clusters_df, many_labels_df, k, w, randosta):
    colnam = f'season k{k} w{w} r{randosta}'
    km = KMeans(n_clusters=k, random_state=randosta)
    # scale down date-coord columns by w
    for col in ['xchunk', 'ychunk']:
        for_clusters_df[col] = for_clusters_df[col]*w
    # fit the model
    km.fit(for_clusters_df)
    # add labels from this model to day_labels_df
    many_labels_df[colnam] = km.labels_
    # badchoice: # add distance matrix for this model to dist_matrices
    # dist_matrices[colnam] = cdist(km.cluster_centers_, km.cluster_centers_, metric='euclidean')
    # reset date-coord columns, undoing scaling by w
    for col in ['xchunk', 'ychunk']:
        for_clusters_df[col] = many_labels_df[col]
    # return nothing: effect is modification of day_labels_df, dist_matrices

# now we wrap one_model in a loop for several models
# klist, wlist must be same lenth!
# klist must be full of integers
# returns a pair: dataframe with labels, and dictionary with distance matrices

def step3(for_clusters_df, klist, wlist, randosta):
    # initialize df for labels output
    many_labels_df = for_clusters_df[['xchunk', 'ychunk']].copy()
    # initialize dictionary for distance-matrix output
    # badchoice: dist_matrices = {}
    for i in range(len(klist)):
        one_model(for_clusters_df, many_labels_df, klist[i], wlist[i], randosta)
    return many_labels_df

#           ----    Step4       ----

# aggregating

# aggregator returns most common label, second most common, and
# fraction of counts lost going from top to second: low if close
def top_two(serie):
    cts = serie.value_counts()
    top = cts.index[0]
    if (len(cts) > 1):
        second = cts.index[1]
        guilt = ( cts.iloc[0] - cts.iloc[1] ) / cts.iloc[0] 
    else:
        second = top
        guilt = 0
    return(top, second, guilt)

# takes in output of step 3        NEEDS DATE_CHUNKS COLUMN!!!
# returns df with 36 rows, with columns for each model,
# with triples (top, second-best, guilt) as values
def get_modes(many_labels_df):
    modes = many_labels_df.groupby(['date_chunk', 'xchunk', 'ychunk']).agg(lambda x: top_two(x))
    modes.reset_index(inplace=True)
    modes.sort_values(by = 'date_chunk', inplace=True)
    modes.set_index('date_chunk', inplace=True)
    return modes

# wraps up several steps, in order to
#   access the date_chunks column lost in step2; and
#   combine scaled_df from step2 with many_labels_df from step3 to get distance matrices
# returns pair:
#   df with 36 rows, column for each model, triples (top, second-best, guilt) as values
#   dictionary with distance matrices
def step234(unscaled_df, comps,klist, wlist, randosta):
    for_clusters_df, scaled_df = step2(unscaled_df, comps)
    many_labels_df = step3(for_clusters_df, klist, wlist, randosta)
    # now build dist_matrices
    dist_matrices = {}
    label_added_df = scaled_df.copy()
    for colnam in many_labels_df.columns:
        if ((colnam == 'xchunk' or colnam == 'ychunk') or colnam == 'date_chunk'):
            pass
        else:
            label_added_df['season'] = many_labels_df[colnam]
            label_summ_df = label_added_df.groupby('season').agg(np.mean)
            dist_mat = cdist(label_summ_df.iloc[:,1:], label_summ_df.iloc[:,1:], metric='euclidean')
            dist_matrices[colnam] = dist_mat
    many_labels_df['date_chunk'] = unscaled_df['date_chunk']
    return ( get_modes(many_labels_df), dist_matrices)


#           ----    Step5       ----
# smoothing, and choosing

# smoothe out one model:
#  takes the series of triples and the distance matrix
#  returns series of labels, total guilt
def smooth_one(triples, dist_mat):
    # old_top = triples.map(lambda x: x[0]).to_list()
    # old_second = triples.map(lambda x: x[1]).to_list()
    # old_guilt = triples.map(lambda x: x[2]).to_list()
    triples_list = triples.to_list()
    labels = triples.map(lambda x: x[0]).to_list()
    guilt = 0
    # most of the time it's enough to run the two smoothing loops once; but not always
    undone = True
    while (undone):
        # if this iteration finds nothing to change, leave the loop:
        undone = False
        # fill in embedded singletons at i-1
        for i in range(len(labels)):
            if ( (labels[i-2] == labels[i]) and (labels[i] != labels[i-1])):
                # found something to change, will need another loop
                undone = True
                guilt += switch_guilt(triples_list[i-1], labels[i], dist_mat)
                labels[i-1] = labels[i]
        # more controversially, "fix" the middle of 3 different consecutives
        # pick the one of the adjacent (at i-2, at i) current labels, 
        # based on season distance to old_top, old_second at i-1
        for i in range(len(labels)):
            if len({labels[i-2], labels[i-1], labels[i]}) == 3:
                # found something to change, will need another loop
                undone = True
                guilt_minus = switch_guilt(triples_list[i-1], labels[i-2], dist_mat)
                guilt_plus = switch_guilt(triples_list[i-1], labels[i], dist_mat)
                if guilt_plus >= guilt_minus:
                    labels[i-1] = labels[i-2]
                    guilt += guilt_minus
                else:
                    labels[i-1] = labels[i]
                    guilt += guilt_plus
        # anybody who got changed by one of these steps matches one of his neighbors
        # so he and his matching neighbor don't get changed by further steps
        # at this point, guilt is the sum of ~distances of switches performed

    # now, count boundaries
    bdries = 0
    for i in range(len(labels)):
        if labels[i-1] != labels[i]:
            # each extra boundary is as bad as a distance-1 switch
            bdries += 1
    # extra boundaries cause guilt; 3 and 5 are subject to change
    guilt += 2*max(0, bdries-5)
    return (labels, guilt)

# subroutine for smooth_one above;   returns 0 if switching to the other mode,
# return distance of switch if second-most-common is rare or far from new
def switch_guilt(triple, new, dist_mat):
    return min( dist_mat[new][triple[0]], dist_mat[new][triple[1]] + triple[2] )

# wrapper-looper, input is the pair returned by step234
# runs smooth_one on each model, pick the one with least guilt,
# returns df with 36 rows, 3 columns: xchunk, ychunk, season; date_chunk is index
def pick_smooth(pear):
    smooth_models = []
    for colnam in pear[0].columns:
        if ((colnam == 'xchunk' or colnam == 'ychunk') or colnam == 'date_chunk'):
            pass
        else:
            one_smooth = smooth_one(pear[0][colnam], pear[1][colnam] )
            smooth_models.append(one_smooth)
            print(f"{colnam} has guilt {one_smooth[1]}")
    smooth_models.sort(key= (lambda x: x[1]))
    # not taking 'date_chunk' explicitly - it's the index
    seasons_df = pear[0][['xchunk', 'ychunk']].copy()
    seasons_df['season'] = smooth_models[0][0]
    return seasons_df

#           ----    Step6       ----

# generating user output:
#  - starts/ends of seasons,
#    or pass seasons_df as dict/json to js to visualize;
#  - adjectives for seasons: absolute, relative, summary-style?

# first, super-wrapper of all previous steps
# hypers = (comps,klist, wlist, randosta)
# returns
#  one df for plotting circle-of-dots
#  another df with avgs of weather measures for each season
#  averages of averages are ok when inner avgs are over ~same-size chunks 
def get_seasons(latitude, longitude, start_year, end_year, hypers):
    unscaled_df = step1(latitude, longitude, start_year, end_year)
    pear = step234(unscaled_df, hypers[0], hypers[1], hypers[2], hypers[3])
    seasons_df = pick_smooth(pear)
    # that's ready for plotting; now build second output: weather avgs
    weather_avgs_df = unscaled_df.groupby(['date_chunk']).agg(np.mean)
    weather_avgs_df2 = seasons_df.join(weather_avgs_df)
    weather_avgs_df2.drop(['year', 'xchunk', 'ychunk'], axis=1, inplace=True)
    weather_avgs_df3 = weather_avgs_df2.groupby('season').agg(np.mean)
    return (seasons_df, weather_avgs_df3)


    # weather_avgs_df.reset_index(inplace=True)
    # weather_avgs_df.sort_values(by = 'date_chunk', inplace=True)
    # weather_avgs_df.set_index('date_chunk', inplace=True)
    # weather_avgs_df['season'] = seasons_df['season']
    # return (seasons_df, weather_avgs_df)

# prettify the two outputs!

def plot_labels(modes):
    for colnam in modes.columns:
        if ((colnam == 'xchunk' or colnam == 'ychunk') or colnam == 'date_chunk'):
            pass
        else:
            modes.plot.scatter(x='xchunk', y='ychunk', c=colnam, s=100, colormap='Set1')


def pretty_season_weather(ugly_df):
    daf = ugly_df[['temp_max_avg', 'temp_min_avg', 'cloud_12_avg', 'precip_hrs_avg', 'rain_sum_avg',
                      'snowfall_sum_avg', 'median_wind_avg', 'humid_avg_avg']].copy()
    daf.columns = ['High Temp', 'Low Temp', 'Percent Cloudy', 'Hours of rain/snow',
                   'Rain total', 'Snow total', 'Wind', 'Humidity']
    # temp scale for rounding
    for colnam in daf.columns:
        if colnam == 'Hours of rain/snow':
            daf[colnam] = daf[colnam].round(1)
        elif colnam == 'Rain total' or colnam == 'Snow total':
            daf[colnam] = daf[colnam].round(2)
        else:
            daf[colnam] = daf[colnam].round()
    return daf.transpose()

def seasons_for_flask(latitude, longitude, start_year, end_year, hypers):
    seasons = get_seasons(latitude, longitude, start_year, end_year, hypers)
    season_weather_table = seasons[1].to_html()
    plotme = {}
    plotme['xlist'] = seasons[0]['xchunk'].to_list()
    plotme['ylist'] = seasons[0]['ychunk'].to_list()
    plotme['seasonlist'] = seasons[0]['season'].to_list()
    return(season_weather_table, plotme)