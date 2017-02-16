# -*- coding: utf-8 -*-
"""
Created on Sat Jun  4 10:28:40 2016

@author: rick
"""

def rollArray(arr, direction):
    """
    rolls the zonal raster array in the direction assigned from the dict.
    Fills row or column or both that get rolled to the other side of the 
    array with the rasters no-data value, those cells are unusable in
    this process. Returns the shifted array to be compared with the original
    and the fdr
    """
    if len(direction) == 4:
        arr = arr[0,:]
        new = np.roll(np.roll(arr, direction[0], axis=0), direction[1], axis=1)
        new[direction[2],:] = arr[direction[2],:]
        new[:, direction[3]] = arr[:, direction[3]] 
    if len(direction) == 3:
        new = np.roll(arr[0,:], direction[0], axis=direction[1])
        if direction[1] == 0:
            new[direction[2],:] = arr[0,direction[2],:]
        if direction[1] == 1:
            new[:,direction[2]] = arr[0,:,direction[2]]
    return np.expand_dims(new, axis=0) 

def makeFlows(arr, shiftd, fdr, path, nd):
    """
    called after each roll has been performed, compares arrays to see where zones
    flow into one another, holds the connections in the FROM TO table
    
    """
    iso = np.not_equal(arr, shiftd) * np.not_equal(shiftd, nd) 
    arr = iso * np.equal(fdr,path) * arr 
    shiftd = iso * np.equal(fdr,path) * shiftd
    return pd.DataFrame({'TOCOMID' : arr[np.not_equal(arr,shiftd)], 
							 'FROMCOMID' : shiftd[np.not_equal(arr,shiftd)],
								'move' : path})

def compAll(arr,fdr,moves,flows, nd):
    """
    this function uses the dictionary 'moves' to roll the zonal raster in all 8 directions
    
    """
    moves = {'up':[(-1,0,-1),4], 'left': [(-1,1,-1),1], 'down' : [(1,0,0),64], 
                   'right' : [(1,1,0),16], 'downRight' : [(1,1,0,0),32], 
                   'downLeft' : [(1,-1,0,-1), 128], 'upRight' : [(-1,1,-1,0),8], 
                    'upLeft' : [(-1,-1,-1,-1),2]}
                    
    for move in moves:
        flow = makeFlows(arr, rollArray(arr, moves[move][0]), fdr, moves[move][1], nd)
        flows = pd.concat([flows,flow])
        return flows
	
def main(zf, ff, of):
#	
#	with rio.open(zone_file) as src:
#		profile = src.profile.copy()
#		data = src.read()    
#		
#	with rio.open(fdr_file) as src:
#		profile2 = src.profile.copy()
#		fdr = src.read()  
    #How can I get the no=data value from the zonal raster before processing begins
    nd = profile['nodata']
    #initialize a DF to be filled when passed to the compAll function
    flows = pd.DataFrame()
    
    # run through the dict of moves to get all connections and drop duplicate connections
    flows = compAll(data,fdr,moves,flows,nd).drop_duplicates(['FROMCOMID','TOCOMID'])
    flows.to_csv(of, index=False)
    print "Finished flow table: %s" % of

############################################################################### 
if __name__ == '__main__':
    import sys
    import numpy as np
    import pandas as pd
    import rasterio as rio
    import riomucho
											
	
# -- I'm thinking it might be able to work as such...
 
# is the windows argument made to select out only certain windows for processing?


# I am hoping to pass the 2 rasters as inputs and then to minimize memory when 
# processing, split both inputs into windows that will cycle through the  
# rasters, will probably need to overlap by 1 cell both vertically and horizontally
# as they work through the raster.

processes = # this should be equal to the number of cores that I want to use??
 
with riomucho.RioMucho([sys.argv[1], sys.argv[2]], sys.argv[3], main,
    windows={windows}, # do I need to specify the number of windows to use?? or the window size?
    global_args={global arguments}, # seems like  I might be able to use to pass nodata value to  
    options={options to write}) as rios:


    rios.run({processes})

