# -*- coding: utf-8 -*-
"""
Created on Sat Jun  4 10:28:40 2016

@author: rick
"""

def rollArray(arr, direction):
	
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
	iso = np.not_equal(arr, shiftd) * np.not_equal(shiftd, nd) 
	arr = iso * np.equal(fdr,path) * arr 
	shiftd = iso * np.equal(fdr,path) * shiftd
	return pd.DataFrame({'TOCOMID' : arr[np.not_equal(arr,shiftd)], 
							 'FROMCOMID' : shiftd[np.not_equal(arr,shiftd)],
								'move' : path})

def compAll(arr,fdr,moves,flows, nd):
	for move in moves:
		flow = makeFlows(arr, rollArray(arr, moves[move][0]), fdr, moves[move][1], nd)
		flows = pd.concat([flows,flow])
	return flows
	
def main(zf, ff, of):
	moves = {'up':[(-1,0,-1),4], 'left': [(-1,1,-1),1], 'down' : [(1,0,0),64], 'right' : [(1,1,0),16],
			 'downRight' : [(1,1,0,0),32], 'downLeft' : [(1,-1,0,-1), 128], 'upRight' : [(-1,1,-1,0),8], 
			 'upLeft' : [(-1,-1,-1,-1),2]}
	with rio.open(zone_file) as src:
		profile = src.profile.copy()
		data = src.read()    
		
	with rio.open(fdr_file) as src:
		profile2 = src.profile.copy()
		fdr = src.read()  

	nd = profile['nodata']
	flows = pd.DataFrame()
	flows = compAll(data,fdr,moves,flows,nd).drop_duplicates(['FROMCOMID','TOCOMID'])
	flows.to_csv(of, index=False)
	print "Finished flow table: %s" % of

############################################################################### 
if __name__ == '__main__':
	import sys
	import numpy as np
	import pandas as pd
	import rasterio as rio
	zone_file = sys.argv[1]
	fdr_file = sys.argv[2]
	out_file = sys.argv[3]
	main(zone_file, fdr_file, out_file)											
	



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
