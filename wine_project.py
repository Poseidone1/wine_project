# Load packages/modules
import numpy as np
import pandas as pd
import geopandas as gpd
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
import geopy.geocoders
import rasterio as rio
import glob as glb
import os

from cartopy.feature import ShapelyFeature
from shapely.geometry import Point, box
from functools import partial
from geopy.extra.rate_limiter import RateLimiter
from geopy.geocoders import GoogleV3
from rasterio.merge import merge
from rasterio.plot import show
from rasterio.mask import mask
from fiona.crs import from_epsg
from random import randint

%matplotlib notebook

# paths
douro_path = "./data_source/douro/"  # path to load Douro datasets
alentejio = "./data_source/alentejo/" # path to load Alentejio datasets

# Methods Section
def addressGeocoded(df,gc):
    '''
    This function accepts a dataframe and a geocode object and returns
    a geo dataframe

    :param df: dataframe with addresses
    :param gc: geocode object

    :returns geodataframe
    '''
    tmp_df = df.copy() # create a copy of the original dataframe, in this way no changes will be applied to the original one
    tmp_df['geolocation'] = tmp_df['address'].apply(gc) # translate address into coordinate
    tmp_df['geometry'] = tmp_df['geolocation'].apply(lambda loc: tuple(loc.point[0:2]) if loc else None) #extract tuple point location
    tmp_df['geometry'] = tmp_df['geometry'].apply(Point) # convert tuple in shapely geometry point
    gdf = gpd.GeoDataFrame(tmp_df)
    gdf.set_crs("EPSG:3763", inplace=True) #Set the projection to the ETRS89/PT-TMS09
    gdf = gdf.drop(columns=['geolocation']) #Drop geolocation information; shapefile only accept one geometry column when saving the geodataframe
    gdf.to_file("./data_source/douro/douro_wine_producers.shp") # save the geodataframe in shape file; in this way no queries are sent to Google geocoding service
    return gdf

def imgDisplay(image, ax, bands, stretch_args=None, **imshow_args):
    '''
    This method reorganise the structure of the raster image

    :param image: raster image
    :param ax: fig object
    :param bands: bands of the raster image

    :returns the axes and the image
    '''
    dispimg = img.copy().astype(np.float32)  # make a copy of the original image,
    # but be sure to cast it as a floating-point image, rather than an integer

    for b in range(img.shape[0]):  # loop over each band, stretching using percentile_stretch()
        if stretch_args is None:  # if stretch_args is None, use the default values for percentile_stretch
            dispimg[b] = percentile_stretch(img[b])
        else:
            dispimg[b] = percentileStretch(img[b], **stretch_args)

    # next, we transpose the image to re-order the indices
    dispimg = dispimg.transpose([1, 2, 0])

    # finally, we display the image
    handle = ax.imshow(dispimg[:, :, bands], **imshow_args)

    return handle, ax

def generateHandles(labels, colors, edge='k', alpha=1):
    '''
    generate_handles help to build the legend for the features used in the map

    :param lables: list of string name to be assocaited with a color
    :param color: color list

    :returns handle object
    '''
    lc = len(colors)  # get the length of the color list
    handles = []
    for i in range(len(labels)):
        handles.append(mpatches.Rectangle((0, 0), 1, 1, facecolor=colors[i % lc], edgecolor=edge, alpha=alpha))
    return handles

def colorListCreation(object_list,hexcolor=0xFFFFFF):
    '''
    This methods create a random list of colors according
    to the size of the list of objects need to be colored

    :param object_list: object need to be associated with a color
    :param hexcolor: color in hex; the dault value is white

    :returns color list
    '''
    colors = []
    for i in range(len(object_list)):
        colors.append('#%06X' % randint(0, hexcolor))
    return colors

def getFeatures(gdf):
    '''
    Function to parse features from GeoDataFrame in such a manner that rasterio wants them

    :param gdf: geodataframe

    :returns a geodataframe in json format
    '''
    import json
    return [json.loads(gdf.to_json())['features'][0]['geometry']]

def percentileStretch(img, pmin=0., pmax=100.):
    '''
    The method normalizes the color based on the maximun value per given band

    :param img: raster image that needs to go through color normalization
    :param pmin: percentile min value; default is 0
    :param pmax: percentile max value; default is 100

    :returns a stretched image
    '''
    # here, we make sure that pmin < pmax, and that they are between 0, 100
    if not 0 <= pmin < pmax <= 100:
        raise ValueError('0 <= pmin < pmax <= 100')
    # here, we make sure that the image is only 2-dimensional
    if not img.ndim == 2:
        raise ValueError('Image can only have two dimensions (row, column)')

    minval = np.percentile(img, pmin)
    maxval = np.percentile(img, pmax)

    stretched = (img - minval) / (maxval - minval)  # stretch the image to 0, 1
    stretched[img < minval] = 0  # set anything less than minval to the new minimum, 0.
    stretched[img > maxval] = 1  # set anything greater than maxval to the new maximum, 1.

    return stretched
#
######## Load Data
#
# Laod Portugal municipalities.
pt_municipalities_gdf = gpd.read_file("./data_source/Cont_AAD_CAOP2020/Cont_AAD_CAOP2020.shp")
# pt_municipalities_gdf.shape
pt_municipalities_gdf.head(15)
# Load Douro municipalities and parishes dataset where douro wine is produced.
douro_municipalities_df = pd.read_excel(douro_path+"douro_municipality_parish.xlsx")
# douro_municipalities_df.shape
douro_municipalities_df.head(15)
# Get the list of unique Douro municipalities
unique_munic = list(douro_municipalities_df['Concelhos'].unique()) #List of unique municipalities
pt_douro_munic_gdf = pt_municipalities_gdf[pt_municipalities_gdf['Concelho'].apply(lambda muni: muni in unique_munic)] #extract Douro municipalities from Portugal dataset
#
#
# Check all the douro wine production municipalities are in the new sub geodataframe
print(pt_douro_munic_gdf['Concelho'].unique().shape)
print(unique_munic.shape)
test_list = []
for element in unique_munic:
    if element not in pt_douro_munic_gdf['Concelho'].unique():
        test_list.append(element)
print(test_list)
pt_municipalities_gdf[pt_municipalities_gdf['Freguesia']=='Escalhão']
#
#
# Check Google geocoding API service access in Appendix to see how the geodatframe has been obtained
douro_wine_producers_gdf = gpd.read_file("./data_source/douro/douro_wine_producers.shp")
unique_producer = list(douro_wine_producers_gdf['producer'].unique()) #Create a list of unique Douro wine producers
douro_wine_producers_gdf.head(10)
#
# Load Douro Region shapefile
douro_gdf = gpd.read_file(douro_path+"RDD_ETRS89/RDD_ETRS89.shp")
print(douro_gdf.crs)
dxmin, dymin, dxmax, dymax = douro_gdf.total_bounds #total_bounds gives output the xmin, ymin, xmax, ymax of the area
#
########### Create Douro map
#
# Create the figure layout
pt_crs = ccrs.UTM(29) #Universal Trasverse Marcator system for Portugal
dfig, ax = plt.subplots(1, 1, figsize=(12, 12), subplot_kw=dict(projection=pt_crs))
ax = plt.axes(projection=ccrs.Mercator()) # create axes object with Maractor projection
douro_region = ShapelyFeature(douro_gdf['geometry'], pt_crs, edgecolor='w',linewidth=2,facecolor='none',zorder=3)
ax.add_feature(douro_region)# add the douro region borders
#
gridlines = ax.gridlines(draw_labels=True)
gridlines.left_labels = False
gridlines.bottom_labels = False
# Douro's boundaries are used to zoom the map to our area of interest
ax.set_extent([dxmin, dxmax, dymin, dymax], crs=pt_crs) #set_extent allow to zoom in the area of interest
#
pt_douro_munic_gdf.crs # pt_douro_parish_gdf has the same CRS
#
munic_colors = colorListCreation(unique_munic) #List of colors for the municipalities
producer_colors = colorListCreation(unique_producer,0xbad0de) #List of colors for the producers
pt_douro_munic_wgs84 = pt_douro_munic_gdf.to_crs("EPSG:4326") # Conversion from Cartesian to Geographic coordinates
for i, name in enumerate(unique_munic):
    douro_municip = ShapelyFeature(pt_douro_munic_wgs84['geometry'][pt_douro_munic_wgs84['Concelho']==name],
                                   pt_crs,
                                   edgecolor='k',
                                   facecolor=munic_colors[i],  # use munic_colors[i] if no raster map is used in the background
                                   linewidth=1,
                                   alpha=0.25
                                  )
    ax.add_feature(douro_municip)# add the douro region borders
for i,color in enumerate(unique_producer):
    ax.plot(douro_wine_producers_gdf.iloc[i,2].y,douro_wine_producers_gdf.iloc[i,2].x,'o',color=producer_colors[i],transform=pt_crs)
# generate a list of handles for the county datasets
municipality_handles = generateHandles(unique_munic, munic_colors, alpha=0.25)
# update county_names to take it out of uppercase text
munici_names = [name.title() for name in unique_munic]

leg = ax.legend(municipality_handles, munici_names, title='Legend', title_fontsize=12, fontsize='small', loc='upper right', bbox_to_anchor=(0.,1.), frameon=True, framealpha=0.5)
#dfig
#Save the file
#dfig.savefig("./img/douromap_with_producers_and_municipalities.png", dpi=300, bbox_inches='tight')
#
### Add raster Image
#
with rio.open(douro_path+"Sat_images/Douro_region_Mosaic_reduced.tif") as dataset:
    img = dataset.read()
    xmin, ymin, xmax, ymax = dataset.bounds
    print(dataset.meta)
my_kwargs = {'extent': [dxmin, dxmax, dymin, dymax],
             'transform': pt_crs}

my_stretch = {'pmin': 0.1, 'pmax': 99.9}
h, ax = imgDisplay(img, ax, [2, 1, 0],stretch_args=my_stretch, **my_kwargs)
dfig
#Save the file
#dfig.savefig("./img/douromap_with_producers_and_municipalities_raster.png", dpi=300, bbox_inches='tight')
###
###
###
#Clip raster data using Douro dimensions
###
###
###
# The satelite image cover a bigger area; in order to work on Douro area, the image needs to be clip using Douro bounds.
# Note: The following section can be skip, the reduced raster map is already provided
# remove the comment to use it
#
# Load satelite image of Douro area
# with rio.open(douro_path+"Sat_images/Douro_region_Mosaic.tif") as dataset:
#    img = dataset.read()
#    xmin, ymin, xmax, ymax = dataset.bounds
#    print(dataset.bounds) # print area dimension
#    print(dataset.crs) # print projection
#    print(img)
#    print(img.shape) # print pixel inforamtion

#xmin, ymin, xmax, ymax = douro_gdf.total_bounds
#bbox = box(xmin, ymin, xmax, ymax)
#print(bbox)
#bbox = box(dxmin, dymin, dxmax, dymax) #Create a box area with the Douro dimension area
#geo = gpd.GeoDataFrame({'geometry': bbox}, index=[0],crs="4258") #Create a geodataframe adding the geometry and defining the same Doure CRS
#print(dataset.meta)
#geo = geo.to_crs(crs=dataset.crs) # Use the same CRS from raster image
# Display raster
#rfig, ax = plt.subplots(1, 1, figsize=(12, 12), subplot_kw=dict(projection=pt_crs))
#coords = getFeatures(geo)
#dataset = rio.open(douro_path+"Sat_images/Douro_region_Mosaic.tif")
#out_img, out_transform = mask(dataset, shapes=coords, crop=True)
#out_img.shape[1]
#out_meta = dataset.meta.copy()
#print(out_meta)
# out_meta.update({"driver": "GTiff",
#                  "height": out_img.shape[1],
#                  "width": out_img.shape[2],
#                  "transform": out_transform
#                 }
#                )
#with rio.open(douro_path+"Sat_images/Douro_region_Mosaic_reduced.tif", "w", **out_meta) as dest:
#    dest.write(out_img)
#    dest.close()
