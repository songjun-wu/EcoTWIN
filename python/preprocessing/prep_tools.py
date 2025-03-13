import os
import numpy as np

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