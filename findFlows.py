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
    # cells change value after shift * cells not equal to NoData
    iso = np.not_equal(arr, shiftd) * np.not_equal(shiftd, nd) * np.not_equal(arr, nd)
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
