# -*- coding: utf-8 -*-
"""
Created on Sat Jun  4 10:28:40 2016

@author: rick
"""
import numpy as np
import pandas as pd
import rasterio as rio
import sys
sys.prefix

moves = {'up':[(-1,0,-1),4], 'left': [(-1,1,-1),1], 'down' : [(1,0,0),64], 'right' : [(1,1,0),16],
         'downRight' : [(1,1,0,0),32], 'downLeft' : [(1,-1,0,-1), 128], 'upRight' : [(-1,1,-1,0),8], 
         'upLeft' : [(-1,-1,-1,-1),2]}
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

def makeFlows(arr, shiftd, fdr, path):
    iso = np.not_equal(arr, shiftd)
    arr = iso * np.equal(fdr,path) * arr
    shiftd = iso * np.equal(fdr,path) * shiftd
    return pd.DataFrame({'TOCOMID' : arr[np.not_equal(arr,shiftd)], 
                             'FROMCOMID' : shiftd[np.not_equal(arr,shiftd)],
                                'move' : path})

def compAll(arr,fdr,moves,flows):
    for move in moves:
        flow = makeFlows(arr, rollArray(arr, moves[move][0]), fdr, moves[move][1])
        flows = pd.concat([flows,flow])
    return flows
    

with rio.open('G:/data/test_wsheds.tif') as src:
    profile = src.profile.copy()
    data = src.read()    
    
with rio.open('G:/data/test_fdr.tif') as src:
    profile2 = src.profile.copy()
    fdr = src.read()  


flows = pd.DataFrame()
flows = compAll(data,fdr,moves,flows)
flows2 = flows.drop_duplicates()
flows3 = flows2.ix[flows2.FROMCOMID != -2147483647]
flows2.ix[flows2.TOCOMID == -2147483647]
print flows
profile2
    
chk = dbf2DF('D:/Projects/lakesAnalysis/From_To_Tables710/LkFrmTo_R01a.dbf')
    
np.not_equal(t, 33)
t = np.array(np.arange(100))
t.shape = (1,10,10)

new = np.roll(t[0,:], 1, axis=0)
new[0,:] = t[0,0,:]

fdr = np.zeros((1,10,10))
fdr[0,3,5] = 1
fdr[0,2,4] = 2
fdr[0,3,2] = 4
fdr[0,4,2] = 8
fdr[0,8,2] = 16
fdr[0,7,7] = 32
fdr[0,5,2] = 64
fdr[0,6,5] = 128
fdr.astype(int)
t.shape

flows = pd.DataFrame()
flows = compAll(t,fdr,moves,flows)
print flows



# get array
basns = np.array(np.arange(100))
basns.shape = (1,10,10)

shift1 = rollArray(t, moves['left'][0])
shift2 = rollArray(t, moves['upLeft'][0])
shift4 = rollArray(t, moves['up'][0])
shift8 = rollArray(t, moves['upRight'][0])
shift16 = rollArray(t, moves['right'][0])
shift32 = rollArray(t, moves['downRight'][0])
shift64 = rollArray(t, moves['down'][0])
shift128 = rollArray(t, moves['downLeft'][0])

#load fdr
fdr = np.ones((1,10,10))
fdr[:] = 8
fdr[0,2,2:5] = 2
fdr[0,3,2:5] = 2
fdr[0,4,2:5] = 2
fdr
#process


makeFlows(basns, shift1,fdr, 1)




#    def compare(self, shft, way):
#        iso = np.not_equal(self.data, shft)
#        t = iso * np.equal(self.fdr, way) * self.data
#        f = iso * np.equal(self.fdr, way) * self.data
#        return pd.DataFrame({'TOCOMID' : t[np.not_equal(t,f)], 
#                             'FROMCOMID' : f[np.not_equal(t,f)]})



with rio.open(filepath, 'r') as src:
    profile = src.profile.copy()
    data = src.read()

with rio.open(filepath, 'r') as fdr:
    pro_fdr = fdr.profile.copy()
    data_fdr = fdr.read()
    
    
#shiftArray should be a function not a class!!

def makeFlows(arr_3d, fdr):
# this will shift the array in one of the eight directions and return the shifted
#array, it comes in as 3-dimensional and will be shifted 2_dimensionally, depending on 
# the direction of the shift will imply which rows/coluimns will need to be replaced with 
# data from the original array so that we don't get those cells returned when making
# the comparison with the originals
def dirTuple(dir):
    if dir == 'U':
        return (-1,0)
    if dir == 'L':
        return (-1,1)
    if dir == 'D':
        return (1,0)
    if dir == 'R':
        return (1,1)

def shiftArray(arr_3d, dir): #(-1,0,-1),(-1,1,-1),(1,0,0),(1,1,0)
    arr = arr_3d[0,:] 
    if len(dir) == 1:
        shift = np.roll(arr[0,:], -1, axis=0) #U
        shift[-1,:] = self.noData
        shift = np.roll(arr[0,:], -1, axis=1) #L
        shift[:,-1] = self.noData
        shift = np.roll(arr[0,:], 1, axis=0) #D
        shift[0,:] = self.noData
        shift = np.roll(arr[0,:], 1, axis=1) #R
        shift[:,0] = self.noData

    else:
        shift = np.roll(np.roll(arr[0,:], -1, axis=1), 1)
        shift = np.roll(np.roll(arr[0,:], -1, axis=1),-1)
        shift = np.roll(np.roll(arr[0,:],1,axis=1),-1)
        shift = np.roll(np.roll(arr[0,:],1,axis=1), 1)
{'2D' : (dir4ax1, dir4ax2, rowShift, colShift), '1D' : }
 
#upL(-1,-1,-1,-1),
    moves = {'up':(-1,0,-1), 'left': (-1,1,-1), 'down' : (1,0,0), 'right' : (1,1,0),
    'downRight' : (-1,-1,-1,-1), 'downLeft' :(1,-1,0,-1), 'upRight' : (-1,1,-1,0), 'upLeft' : (1,1,0,0)]}
def rollArray(arr, direction):
    if len(dir) == 4:
        new = np.roll(np.roll(arr, direction[0], axis=0), direction[1], axis=1)
        new[direction[2],:] = 69 #arr[direction[2],:]
        new[:, direction[3]] = 69 #arr[:, direction[3]] 
    if len(dir) == 3:
        new = np.roll(arr[0,:], direction[0], axis=direction[1])
        if direction[1] == 0:
            new[direction[2],:] = 69 #arr[direction[2],:]
        if direction[1] = 1
            new[:,direction[2]] = 69 #arr[:,direction[2]]
    return new     


new = np.roll(np.roll(rick2, -1, axis=0), -1, axis=1)
new[-1,:] = 69
new[:,-1] = 69
#dnL(1,-1,0,-1)
new = np.roll(np.roll(rick2, 1, axis=0), -1, axis=1)
new[0,:] = rick2[0,:]
new[:,-1] = rick2[:,-1]
#upR (-1,1,-1,0)
new= np.roll(np.roll(rick2, -1, axis=0), 1, axis=1)
new[-1,:] = rick2[-1,:]
new[:,0] = rick2[:,0]
#dnR (1,1,0,0)
new = np.roll(np.roll(rick2, 1, axis=0), 1, axis=1)
new[0,:] = rick2[0,:]
new[:,0] = rick2[:,0]


#upL
np.roll(np.roll(rick2,-1,axis=0),-1,axis=1)
#dnL
np.roll(np.roll(rick2,1,axis=0),-1,axis=1)
#upR
np.roll(np.roll(rick2,-1,axis=0),1,axis=1)
#dnR
np.roll(np.roll(rick2,1,axis=0),1,axis=1)

upR = (-1,1)


    #upR
    shift = np.roll(np.roll(arr[0,:], -1, axis=0), 1)
    shift[-1,:] = arr[-1,:]
    shift[:,0] = arr[:,0]
    #U
    shift = np.roll(arr[0,:], -1, axis=0)
    shift[-1,:] = arr[-1,:]
    #upL
    shift = np.roll(np.roll(arr[0,:], -1, axis=0),-1)
    shift[-1,:] = arr[-1,:]
    shift[:,-1] = arr[:,-1]
    #L
    shift = np.roll(arr[0,:], -1, axis=1)
    shift[:,-1] = arr[:,-1]
    #dnL
    shift = np.roll(np.roll(arr[0,:],1,axis=0),-1)
    shift[0,:] = arr[0,:]
    shift[:,-1] = arr[:,-1]
    #D
    shift = np.roll(arr[0,:], 1, axis=0)
    shift[0,:] = arr[0,:]
    #dnR
    shift = np.roll(np.roll(arr[0,:],1,axis=0), 1)
    shift[:,0] = arr[:,0]
    shift[0,:] = arr[0,:]
    #R
    shift = np.roll(arr[0,:], 1, axis=1)
    shift[:,0] = arr[:,0]
 
def maskCol(arr1, arr2, idx):
    arr1[:,idx] = arr2[:,idx]
    return arr1
def maskRow(arr1, arr2, idx):
    arr1[idx,:] = arr2[idx,:]
    return arr1



    
    

class shiftArray(object):
    def __init__(self, array, nd, fdr, fnd=255):
        self.length = len(array)
        self.noData = nd
        self.data = array
        self.fdr = fdr
        self.fnd = fnd

    def __len__(self, a='json'):
        print a        
        return len(self.data)
        
        
    def shiftupR(self):
        shift = np.roll(np.roll(self.data[0,:], -1, axis=0), 1)
        shift[-1,:] = self.noData
        shift[:,0] = self.noData
        shift = np.expand_dims(shift, axis=0)
      
      
        iso = np.not_equal(self.data, shift)
        t = iso * np.equal(self.fdr,2) * self.data
        f = iso * np.equal(self.fdr,2) * shift
        tos = t[np.not_equal(t,f)]
        froms = f[np.not_equal(t,f)]
        return pd.DataFrame({'TOCOMID' : tos, 'FROMCOMID' : froms})            

    def shiftUpC(self):
        shift = np.roll(self.data[0,:], -1, axis=0)
        shift[-1,:] = self.noData
        shift = np.expand_dims(shift, axis=0)
        iso = np.not_equal(self.data, shift)
        t = iso * np.equal(self.fdr,2) * self.data
        f = iso * np.equal(self.fdr,2) * shift
        tos = t[np.not_equal(t,f)]
        froms = f[np.not_equal(t,f)]
        return pd.DataFrame({'TOCOMID' : tos, 'FROMCOMID' : froms}) 

    def shiftupL(self):
        shift = np.roll(np.roll(self.data[0,:], -1, axis=0),-1)
        shift[-1,:] = self.noData
        shift[:,-1] = self.noData
        shift = np.expand_dims(shift, axis=0)
        iso = np.not_equal(self.data, shift)
        t = iso * np.equal(self.fdr,2) * self.data
        f = iso * np.equal(self.fdr,2) * shift
        tos = t[np.not_equal(t,f)]
        froms = f[np.not_equal(t,f)]
        return pd.DataFrame({'TOCOMID' : tos, 'FROMCOMID' : froms}) 

    def shiftL(self):
        shift = np.roll(self.data[0,:], -1, axis=1)
        shift[:,-1] = self.noData
        shift = np.expand_dims(shift, axis=0)
        iso = np.not_equal(self.data, shift)
        t = iso * np.equal(self.fdr,2) * self.data
        f = iso * np.equal(self.fdr,2) * shift
        tos = t[np.not_equal(t,f)]
        froms = f[np.not_equal(t,f)]
        return pd.DataFrame({'TOCOMID' : tos, 'FROMCOMID' : froms}) 

    def shiftdnL(self):
        shift = np.roll(np.roll(self.data[0,:],1,axis=0),-1)
        shift[0,:] = self.noData
        shift[:,-1] = self.noData
        shift = np.expand_dims(shift, axis=0)
        iso = np.not_equal(self.data, shift)
        t = iso * np.equal(self.fdr,2) * self.data
        f = iso * np.equal(self.fdr,2) * shift
        tos = t[np.not_equal(t,f)]
        froms = f[np.not_equal(t,f)]
        return pd.DataFrame({'TOCOMID' : tos, 'FROMCOMID' : froms}) 

    def shiftdnC(self):
        shift = np.roll(self.data[0,:], 1, axis=0)
        shift[0,:] = self.noData
        shift = np.expand_dims(shift, axis=0)
        iso = np.not_equal(self.data, shift)
        t = iso * np.equal(self.fdr,2) * self.data
        f = iso * np.equal(self.fdr,2) * shift
        tos = t[np.not_equal(t,f)]
        froms = f[np.not_equal(t,f)]
        return pd.DataFrame({'TOCOMID' : tos, 'FROMCOMID' : froms}) 

    def shiftdnR(self):
        shift = np.roll(np.roll(self.data[0,:],1,axis=0), 1)
        shift[:,0] = self.noData
        shift[0,:] = self.noData
        shift = np.expand_dims(shift, axis=0)
        iso = np.not_equal(self.data, shift)
        t = iso * np.equal(self.fdr,2) * self.data
        f = iso * np.equal(self.fdr,2) * shift
        tos = t[np.not_equal(t,f)]
        froms = f[np.not_equal(t,f)]
        return pd.DataFrame({'TOCOMID' : tos, 'FROMCOMID' : froms}) 

    def shiftR(self):
        shift = np.roll(self.data[0,:], 1, axis=1)
        shift[:,0] = self.noData
        shift = np.expand_dims(shift, axis=0)
        iso = np.not_equal(self.data, shift)
        t = iso * np.equal(self.fdr,2) * self.data
        f = iso * np.equal(self.fdr,2) * shift
        tos = t[np.not_equal(t,f)]
        froms = f[np.not_equal(t,f)]
        return pd.DataFrame({'TOCOMID' : tos, 'FROMCOMID' : froms}) 
            
        
test = np.ones((1,10,10))
test[:] = 147
test[0,:,:3] = 471

a = shiftArray(test,255,fdr).shiftupR()
b = shiftArray(test,255,fdr).shiftUpC()
c = shiftArray(test,255,fdr).shiftupL()
d = shiftArray(test,255,fdr).shiftL()
e = shiftArray(test, 255,fdr).shiftdnL()
f = shiftArray(test,255,fdr).shiftdnC()
g = shiftArray(test,255,fdr).shiftdnR()
h =  shiftArray(test,255,fdr).shiftR()

z = shiftArray(test,247)

fdr = np.ones((1,10,10))
fdr[:] = 8
fdr[0,2,2:5] = 2
fdr

shft2 = np.not_equal(test,h)
pip = shft2 * np.equal(fdr,2) * test 
pop = shft2 * np.equal(fdr,2) * h
t = pip[np.not_equal(pip,pop)]
s = pop[np.not_equal(pip,pop)]
df = pd.DataFrame({'TOCOMID' : s, 'FROMCOMID' : t})
