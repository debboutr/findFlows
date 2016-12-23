# -*- coding: utf-8 -*-
"""
Created on Sat Jun  4 10:28:40 2016

@author: rick
"""
import sys
import numpy as np
import pandas as pd
import rasterio as rio

def rollArray(a, d):	
    if len(d) == 4:
        a = a[0,:]
        new = np.roll(np.roll(a, d[0], axis=0), d[1], axis=1)
        new[d[2],:] = a[d[2],:]
        new[:, d[3]] = a[:, d[3]] 
    if len(d) == 3:
        new = np.roll(a[0,:], d[0], axis=d[1])
        if d[1] == 0:
            new[d[2],:] = a[0,d[2],:]
        if d[1] == 1:
            new[:,d[2]] = a[0,:,d[2]]
    return np.expand_dims(new, axis=0) 

def makeFlows(arr, shiftd, fdr, path, nd):
    iso = np.not_equal(arr, shiftd) * np.not_equal(shiftd, nd)  # cells change value after shift * cells not equal to NoData
    pth = np.equal(fdr,path)  # True when equal to path value
    val = iso * pth * arr 
    shiftval = iso * pth * shiftd
    idx = np.not_equal(val,shiftd)
    tocom = val[idx]
    fromcom = shiftval[idx]
    tocom = tocom[tocom > 0]
    fromcom = fromcom[fromcom > 0]    
    # don't load-in the entire array to the DF, just connection vals
    df = pd.DataFrame({'TOCOMID' : tocom, 
                       'FROMCOMID' : fromcom,
                            'move' : path})
    return df.drop_duplicates(['FROMCOMID','TOCOMID'])

def compAll(arr, fdr ,moves, from_to, nd):
    for move in moves:
        flow = makeFlows(arr, rollArray(np.copy(arr), moves[move][0]), fdr, moves[move][1], nd)
        from_to = pd.concat([from_to,flow])
    return from_to

def expand(window, size=1):
    r, c = window
    return ((r[0] - size, r[1] + size), (c[0] - size, c[1] + size))

def check_window(window, w, h):
    r, c = window
    return ((max(0, r[0]), min(h, r[1])), (max(0, c[0]), min(w, c[1])))
    
def chunk_windows(r, indexes=None, max_ram=250000000):
    if indexes is None:
        indexes = r.indexes
    elif isinstance(indexes, int):
        indexes = [indexes]
    if not indexes:
        raise ValueError('No indexes to read')
    pixel_size = 0
    for bidx in indexes:
        if bidx not in r.indexes:
            raise IndexError('band index out of range')
        idx = r.indexes.index(bidx)
        pixel_size += np.dtype(r.dtypes[idx]).itemsize  
    chunk_size, _ = divmod(max_ram, pixel_size)
    r_h, r_w = r.height, r.width
    if chunk_size >= r_h * r_w:
        yield (0, 0), ((0, r_h), (0, r_w))
    else:
        b_h, b_w = r.block_shapes[0]
        d, _ = divmod(chunk_size, r_w * b_h)
        chunk_height = d * b_h
        d, m = divmod(r_h, chunk_height)
        n_chunks = d + int(m>0)
        for i in range(n_chunks):
            row = i * chunk_height
            height = min(chunk_height, r_h - row)
            yield (i, 0), ((row, row+chunk_height), (0, r_w)) 

def findFlows(zone_file, fdr_file):
    moves = {'up':[(-1,0,-1),4],'left':[(-1,1,-1),1],'down' :[(1,0,0),64], 
            'right':[(1,1,0),16],'downRight':[(1,1,0,0),32],
            'downLeft':[(1,-1,0,-1), 128],'upRight':[(-1,1,-1,0),8],
            'upLeft':[(-1,-1,-1,-1),2]}
    flows = pd.DataFrame()
    count = 0
    with rio.open(zone_file) as z:
        with rio.open(fdr_file) as f:  # 0 is NoData for fdr
            profile = z.profile.copy()
            #  profile2 = f.profile.copy()
            nd = profile['nodata']
            assert z.shape == f.shape, "Rasters have different extents!"
            for _, w in chunk_windows(z):
                new_w = check_window(expand(w,2), z.width, z.height)
                print w
                print new_w
                count += 1
                data = z.read(window=new_w)
                f_r = f.read(window=new_w)
                flows = pd.concat([flows,compAll(data,f_r,moves,flows,nd)])
    return flows.drop_duplicates(['FROMCOMID','TOCOMID'])
    
############################################################################### 
if __name__ == '__main__':
    sys.exit(findFlows())
#    zone_file = r'D:\Projects\findFlows\sampleData\exWshed.tif'
#    fdr_file = r'D:\Projects\findFlows\sampleData\exFdr.tif'
#    findFlows(zone_file, fdr_file)
#zone_file = r'D:\Projects\LakeCat\play2\rasters\wtshds_05d.tif'
#fdr_file = r'D:\NHDPlusV21\NHDPlusMS\NHDPlus05\NHDPlusFdrFac05d\fdr'
#joe = findFlows(zone_file, fdr_file)
#os.mkdir(out_dir)
#joe.to_csv("%s/joe.csv" % out_dir, index=False)
############################################################################### 
# Import arcpy module
#import os
#import arcpy
#from arcpy.sa import Raster, Con, Combine, IsNull
#from datetime import datetime
#
#out_dir = r'D:\Projects\LakeCat\play2\testFindFlows'
#
## Check out any necessary licenses
#arcpy.CheckOutExtension("spatial")
#arcpy.env.workspace = out_dir
#
#
#fdr = Raster(fdr_file)
#Wtshds = Raster(zone_file)
#startTime = datetime.now()
## Process: Shift
#print 'shifting'
#shift1 = arcpy.Shift_management(Wtshds, "shift1", "-30", "0", Wtshds)
#shift2 = arcpy.Shift_management(Wtshds, "shift2", "-30", "30", Wtshds)
#shift4 = arcpy.Shift_management(Wtshds, "shift4", "0", "30", Wtshds)
#shift8 = arcpy.Shift_management(Wtshds, "shift8", "30", "30", Wtshds)
#shift16 = arcpy.Shift_management(Wtshds, "shift16", "30", "0", Wtshds)
#shift32 = arcpy.Shift_management(Wtshds, "shift32", "30", "-30", Wtshds)
#shift64 = arcpy.Shift_management(Wtshds, "shift64", "0", "-30", Wtshds)
#shift128 = arcpy.Shift_management(Wtshds, "shift128", "-30", "-30", Wtshds)
#
#
## Process: Raster Calculator
#print 'running raster calculator on shifts'
#flowto1 = ((shift1 != Wtshds) * (fdr == 1)) * shift1
#flowto2 = ((shift2 != Wtshds) * (fdr == 2)) * shift2
#flowto4 = ((shift4 != Wtshds) * (fdr == 4)) * shift4
#flowto8 = ((shift8 != Wtshds) * (fdr == 8)) * shift8
#flowto16 = ((shift16 != Wtshds) * (fdr == 16)) * shift16
#flowto32 = ((shift32 != Wtshds) * (fdr == 32)) * shift32
#flowto64 = ((shift64 != Wtshds) * (fdr == 64)) * shift64
#flowto128 = ((shift128 != Wtshds) * (fdr == 128)) * shift128
#
#FlowToSum = Con(IsNull(flowto1), 0, flowto1) + Con(IsNull(flowto2), 0, flowto2) + Con(IsNull(flowto4), 0, flowto4) + Con(IsNull(flowto8), 0, flowto8) + Con(IsNull(flowto16), 0, flowto16) + Con(IsNull(flowto32), 0, flowto32) + Con(IsNull(flowto64), 0, flowto64) + Con(IsNull(flowto128), 0, flowto128)
#FlowToFinal = Con(FlowToSum != 0, FlowToSum)
#outCombine = Combine([FlowToFinal, Wtshds])
#outCombine.save("%s/LkFrmTo_R05a.tif" % (out_dir))
#rasterList = arcpy.ListRasters("*", "")
#for raster in rasterList:
#    arcpy.Delete_management(raster)
#outDbf = "%s/LkFrmTo_R05a.dbf" % (out_dir)
#if not arcpy.Exists(outDbf):
#    arcpy.CopyRows_management(outCombine, outDbf, "")
#print "total elapsed time " + str(datetime.now()-startTime)

###############################################################################
#fdr = np.copy(f_r)
#arr = np.copy(data)
#move = 'down'
#path = moves[move][1]
#
#                
#def chunk_windows(r, indexes=None, max_ram=250000000):
#    """
#    Determine windows for reading a rasterio dataset based on a
#    user-specified RAM limit
# 
#    Parameters
#    ----------
#    r : rasterio.DatasetReader
#        The raster used to determine chunk size
#    indexes : int or sequence
#        The subset of indexes (bands) to use to determine chunk size.
#        Defaults to None, which uses all bands in the raster
#    max_ram : int
#        The maximum RAM to allocate per chunk.  Defaults to ~250MB.
# 
#    Returns
#    -------
#    A generator with the chunk index and chunk window address as a tuple.
#    This is the same structure that is returned by rasterio.block_windows
#    """
# 
#    # Get the indexes (bands) to use - these are 1-indexed (instead of 0)
#    if indexes is None:
#        indexes = r.indexes
#    elif isinstance(indexes, int):
#        indexes = [indexes]
#    if not indexes:
#        raise ValueError('No indexes to read')
# 
#    # Calculate the size of a pixel across all bands
#    pixel_size = 0
#    for bidx in indexes:
#        if bidx not in r.indexes:
#            raise IndexError('band index out of range')
#        idx = r.indexes.index(bidx)
#        pixel_size += np.dtype(r.dtypes[idx]).itemsize 
# 
#    # Calculate how many pixels to collect per chunk
#    chunk_size, _ = divmod(max_ram, pixel_size)
# 
#    # Short circuit the case where the entire raster fits in one chunk
#    r_h, r_w = r.height, r.width
#    if chunk_size >= r_h * r_w:
#        yield (0, 0), ((0, r_h), (0, r_w))
# 
#    # Otherwise calculate how many "block rows" (block height * raster width)
#    # will fit in one chunk (chunk_height)
#    else:
#        b_h, b_w = r.block_shapes[0]
#        d, _ = divmod(chunk_size, r_w * b_h)
#        chunk_height = d * b_h
# 
#        # Calculate the number of chunks and return the chunk windows
#        d, m = divmod(r_h, chunk_height)
#        n_chunks = d + int(m>0)
#        for i in range(n_chunks):
#            row = i * chunk_height
#            height = min(chunk_height, r_h - row)
#            yield (i, 0), ((row, row+chunk_height), (0, r_w))   
############################################################################### 




             
#                print w
#                #print new_w
#                if count == 168:
#                    break
#fdr = np.copy(f_r)
#arr = np.copy(data)                
                
###############################################################################
# a = pd.read_csv('D:/Projects/lakesAnalysis/From_To_Tables710/LakesFlowTableALL.csv')
# a.head()
# a.ix[a.FROMCOMID == 5875283]
# chk.ix[chk.REG01A_WTS == 5875283]
# flows.head()

# flowtable = 'L:/Priv/CORFiles/Geospatial_Library/Data/Project/SSWR1.1B/LakesAnalysis/From_To_Tables/LkFrmTo_R01a.dbf'
# infile = open(flowtable, 'rb')
# data = list(dbfreader(infile))

# flows2 = flows.drop_duplicates()
# flows3 = flows2.ix[flows2.FROMCOMID != -2147483647]
# flows.ix[flows.FROMCOMID == -2147483647]
# print flows
# profile2
# type(nd) 
# type(data[0,0,0]) 
# chk = dbf2DF('D:/Projects/lakesAnalysis/From_To_Tables710/LkFrmTo_R01a.dbf')

# np.not_equal(t, 33)
# t = np.array(np.arange(100))
# t.shape = (1,10,10)

# new = np.roll(t[0,:], 1, axis=0)
# new[0,:] = t[0,0,:]

# fdr = np.zeros((1,10,10))
# fdr[0,3,5] = 1
# fdr[0,2,4] = 2
# fdr[0,3,2] = 4
# fdr[0,4,2] = 8
# fdr[0,8,2] = 16
# fdr[0,7,7] = 32
# fdr[0,5,2] = 64
# fdr[0,6,5] = 128
# fdr.astype(int)
# t.shape

# flows = pd.DataFrame()
# flows = compAll(t,fdr,moves,flows)
# print flows



# # get array
# basns = np.array(np.arange(100))
# basns.shape = (1,10,10)

# shift1 = rollArray(data, moves['left'][0])
# shift2 = rollArray(t, moves['upLeft'][0])
# shift4 = rollArray(t, moves['up'][0])
# shift8 = rollArray(t, moves['upRight'][0])
# shift16 = rollArray(t, moves['right'][0])
# shift32 = rollArray(t, moves['downRight'][0])
# shift64 = rollArray(t, moves['down'][0])
# shift128 = rollArray(t, moves['downLeft'][0])

 # np.not_equal(data, shift1) * np.not_equal(shift1, nd)
# nd = 67
# #load fdr
# fdr = np.ones((1,10,10))
# fdr[:] = 8
# fdr[0,2,2:5] = 2
# fdr[0,3,2:5] = 2
# fdr[0,4,2:5] = 2
# fdr
