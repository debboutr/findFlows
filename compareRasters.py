# -*- coding: utf-8 -*-
"""
Created on Tue Oct 04 14:38:23 2016

@author: Rdebbout
"""

import os
import rasterio
import numpy as np

home = 'L:/Priv/CORFiles/Geospatial_Library/Data/Project/StreamCat/LandscapeRasters/QAComplete'
tifs = []
for x in os.listdir(home):
    if ".tif" in x and "mar14" in x and not 'xml' in x and not 'ovr' in x:
        print x
        tifs.append(x)
tifs = ['cbnf.tif','fert.tif','manure.tif']

def makeBinary(arr):
    arr[arr>0] = 1
    arr[arr<0] = 0
    return arr.astype(int)
        
         
with rasterio.open('%s/%s' % (home, tifs[1]), 'r') as one:
    with rasterio.open('%s/%s' % (home, tifs[2]), 'r') as two:
        for x in [y for y in one.meta if not 'nodata' in y and not 'dtype' in y]:
            if one.meta[x] != two.meta[x]:
                print 'Different transform!'
                break
        for block_index, win in one.block_windows(1):     
            al = one.read(1,window=win)
            ca = two.read(1, window=win)
            al = makeBinary(al)
            ca = makeBinary(ca)
            if np.array_equal(al,ca) == False:
                print win
                print np.array_equal(al,ca)
                break
        print 'Rasters are equal'

                


                
win = ((11008, 11136), (46976, 47104))
with rasterio.open('%s/%s' % (home, tifs[11]), 'r') as one:
    with rasterio.open('%s/%s' % (home, tifs[8]), 'r') as two:
        al = one.read(1,window=win)
        ca = two.read(1, window=win)
        
np.where(ca == 0)
np.where(al == 0)


##############################################################################
#wins = (((0,16499),(0,26375)),((16499,32998),(0,26375)),((0,16499),(26375,52750)),((16499,32998),(26375,52750)))
#
#for win in wins:
#    with rasterio.open('%s/%s' % (home, tifs[11]), 'r') as r:
#        al = r.read(1,window=win)
#        al[al>0] = 1
#        al[al<0] = 0
#        al = al.astype(int)
#    with rasterio.open('%s/%s' % (home, tifs[8]), 'r') as r:
#        ca = r.read(window=win)  # read all raster values
#        ca[ca>0] = 1
#        ca[ca<0] = 0
#        ca = ca.astype(int)
#        print np.array_equal(al,ca)
#        if np.array_equal(al,ca) == False:
#            al = None
#            ca = None
#            break
#        al = None
#        ca = None


