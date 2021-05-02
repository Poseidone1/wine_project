import numpy as np
import rasterio as rio
import glob as glb
import os

from rasterio.merge import merge
from rasterio.plot import show
from rasterio.mask import mask


# paths
douro_path = "./data_source/douro/"  # path to load Douro datasets
alentejio = "./data_source/alentejo/" # path to load Alentejio datasets
########################################################
### Note: the following steps can be done only once ####
########################################################
# Create an list with the path of needed images
query = os.path.join(douro_path+"Sat_images","LT05*.tif")
dem_file = glb.glob(query) # glob function can be used to list files from a directory with specific criteria
dem_file
src_files_to_mosaic = [] # Create a list for the source files
# Iterate over raster files and add them to source -list in 'read mode'
for f in dem_file:
    src = rio.open(f)
    print(src.crs)
    src_files_to_mosaic.append(src)
mosaic, out_trans = merge(src_files_to_mosaic) #use merge to create a mosaic from the images
# Test if the image is correct
show(mosaic,cmap='terrain')
#Update medata data information and save the image on harddisk
print(src.meta) # print the metadata information of each single image
out_meta = src.meta.copy() #create a copy of metadata information
out_meta.update({"driver": "GTiff",
                 "height": mosaic.shape[1],
                 "width": mosaic.shape[2],
                 "transform": out_trans,
                 "compress": 'JPEG',
                 "jpeg_quality": 60
                }
               )
print(out_meta)
# Write the mosaic raster to disk
with rio.open(douro_path+"Sat_images/Douro_region_Mosaic.tif", "w", **out_meta) as dest:
    dest.write(mosaic)
    dest.close()
