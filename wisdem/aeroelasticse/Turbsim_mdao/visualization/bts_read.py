import numpy as np

def fread(fid, nelements, dtype):
     if dtype is np.str:
         dt = np.uint8  # WARNING: assuming 8-bit ASCII for np.str!
     else:
         dt = dtype

     data_array = np.fromfile(fid, dt, nelements)
     data_array.shape = (nelements, 1)

     return data_array

fid = open('./turbsim_default.bts', 'rb');
nffc = 3
fileFmt = 'int16' # kind 2 ?

tmp   = fread( fid, 1, np.int16);        # TurbSim format identifier (should = 7 or 8 if periodic), INT(2)
nz    = fread( fid, 1, np.int32);        # the number of grid points vertically, INT(4)
ny    = fread( fid, 1, np.int32);        # the number of grid points laterally, INT(4)
ntwr  = fread( fid, 1, np.int32);        # the number of tower points, INT(4)
nt    = fread( fid, 1, np.int32);        # the number of time steps, INT(4)

dz    = fread( fid, 1, np.float32);      # grid spacing in vertical direction, REAL(4), in m
dy    = fread( fid, 1, np.float32);      # grid spacing in lateral direction, REAL(4), in m
dt    = fread( fid, 1, np.float32);      # grid spacing in delta time, REAL(4), in m/s
mffws = fread( fid, 1, np.float32);      # the mean wind speed at hub height, REAL(4), in m/s
zHub  = fread( fid, 1, np.float32);      # height of the hub, REAL(4), in m
z1    = fread( fid, 1, np.float32);      # height of the bottom of the grid, REAL(4), in m

Vslope = np.ones(3)
Voffset = np.ones(3)
Vslope[0]  = fread( fid, 1, np.float32); # the U-component slope for scaling, REAL(4)
Voffset[0] = fread( fid, 1, np.float32); # the U-component offset for scaling, REAL(4)
Vslope[1]  = fread( fid, 1, np.float32); # the V-component slope for scaling, REAL(4)
Voffset[1] = fread( fid, 1, np.float32); # the V-component offset for scaling, REAL(4)
Vslope[2]  = fread( fid, 1, np.float32); # the W-component slope for scaling, REAL(4)
Voffset[2] = fread( fid, 1, np.float32); # the W-component offset for scaling, REAL(4)

# Read the description string: "Generated by TurbSim (vx.xx, dd-mmm-yyyy) on dd-mmm-yyyy at hh:mm:ss."

nchar    = fread( fid, 1, np.int32);     # the number of characters in the description string, max 200, INT(4)
asciiINT = fread( fid, int(nchar), np.int8); # the ASCII integer representation of the character string


nPts        = ny*nz;
nv          = nffc*nPts;               # the size of one time step
nvTwr       = nffc*ntwr;
velocity    = np.zeros([int(s) for s in (nt,nffc,ny,nz)])
twrVelocity = np.zeros([int(s) for s in (nt,nffc,ntwr)])

for it in range(nt):
  ip = 0
  v_cnt = fread( fid, int(nv), fileFmt )
  for iz in range(nz):
    for iy in range(ny):
       for k in range(nffc):
          velocity[it,k,iy,iz] = ( v_cnt[ip] - Voffset[k])/Vslope[k] 
          ip = ip + 1
 
print velocity

np.save('velocity', velocity)
