import os
import numpy as np

def pcraster_ldd_to_d8(fdir):
    fdir[fdir==9] = 128
    fdir[fdir==8] = 64
    fdir[fdir==7] = 32
    fdir[fdir==4] = 16
    fdir[fdir==1] = 8
    fdir[fdir==2] = 4
    fdir[fdir==3] = 2
    fdir[fdir==6] = 1
    return fdir

def cal_slope(dem, fdir, cellsize, nodata=-9999.0):
    d8_dirs = {
        1:  (0, 1),   # East
        2:  (1, 1),   # Southeast
        4:  (1, 0),   # South
        8:  (1, -1),  # Southwest
        16: (0, -1),  # West
        32: (-1, -1), # Northwest
        64: (-1, 0),  # North
        128:(-1, 1)   # Northeast
    }

    distance_dirs = {
        1:  1,   # East
        2:  np.sqrt(2),   # Southeast
        4:  1,   # South
        8:  np.sqrt(2),  # Southwest
        16: 1,  # West
        32: np.sqrt(2), # Northwest
        64: 1,  # North
        128:np.sqrt(2)   # Northeast
    }

    slope = np.full(dem.shape, nodata)

    for r in range(dem.shape[0]):
        for c in range(dem.shape[1]):
            if fdir[r,c] in d8_dirs.keys():
                dr = d8_dirs[fdir[r,c]][0]
                dc = d8_dirs[fdir[r,c]][1]
                slope[r,c] = np.degrees((np.abs((dem[r,c] - dem[r+dr, c+dc]) / (cellsize * distance_dirs[fdir[r,c]]))))
    
    return slope
                


def saveToASCII(data, fileName, save_path, format, mask, xllcorner=0, yllcorner=0, cellsize=500, nodata=-9999):
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    data = data.astype(np.double)
    data[np.isnan(data)] = -9999

    if format=='int':
        
        np.savetxt(save_path + fileName + '.asc', data, fmt='%d')
    else:
        np.savetxt(save_path + fileName + '.asc', data)

    line1 = 'ncols         ' + str(data.shape[1])
    line2 = 'nrows         ' + str(data.shape[0])
    line3 = 'xllcorner     ' + str(xllcorner)
    line4 = 'yllcorner     ' + str(yllcorner)
    line5 = 'cellsize      ' + str(cellsize)
    line6 = 'NODATA_value  ' + str(nodata)
    with open(save_path + fileName + '.asc', 'r+') as f:
        content = f.read()
        f.seek(0,0)
        f.write(line1+'\n'+line2+'\n'+line3+'\n'+line4+'\n'+line5+'\n'+line6+'\n'+content)