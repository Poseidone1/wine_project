import numpy as np
import pandas as pd
import geopandas as gpd
import geopy.geocoders

from functools import partial
from geopy.extra.rate_limiter import RateLimiter
from geopy.geocoders import GoogleV3

douro_path = "./data_source/douro/"  # path to load Douro datasets
alentejio = "./data_source/alentejo/" # path to load Alentejio datasets

def addressGeocoded(df,gc):
    '''
    This function accepts a dataframe and a geocode object and returns a geo dataframe

    :param df: dataframe with addresses
    :param gc: geocode object

    :returns geodataframe
    '''
    tmp_df = df.copy() # create a copy of the original dataframe, in this way
    #no changes will be applied to the original one
    tmp_df['geolocation'] = tmp_df['address'].apply(gc) # translate address into coordinate
    tmp_df['geometry'] = tmp_df['geolocation'].apply(lambda loc: tuple(loc.point[0:2]) if loc else None) #extract tuple point location
    tmp_df['geometry'] = tmp_df['geometry'].apply(Point) # convert tuple in shapely geometry point
    gdf = gpd.GeoDataFrame(tmp_df)
    gdf.set_crs("EPSG:3763", inplace=True) #Set the projection to the ETRS89/PT-TMS09
    gdf = gdf.drop(columns=['geolocation']) #Drop geolocation information;
    # shapefile only accept one geometry column when saving the geodataframe
    gdf.to_file("./data_source/douro/douro_wine_producers.shp") # save the
    # geodataframe in shape file; in this way no queries are sent to Google geocoding service
    return gdf
