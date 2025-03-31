import os
import numpy as np
import matplotlib.pyplot as plt
from def_GEM import Path

output_path = Path.output_path
nodata = -9999


fnames = os.listdir(output_path)
for fname in fnames:
    print(fname)
    if "_map" in fname and fname.split('.')[-1]=='bin':
        data = np.fromfile(output_path + fname).reshape(-1, 630, 481)
        data[data==nodata] = np.nan
        data = np.mean(data, axis=0)
        fig, ax = plt.subplots(1,1)
        im = ax.imshow(data)
        fig.colorbar(im, ax=ax)
        fig.savefig(output_path + '0_' + fname.split('.')[0] + '.png', dpi=600)
        print('Plot saved at :  ', output_path + fname.split('.')[0] + '.png')
        print(np.nanmin(data), np.nanmean(data), np.nanmax(data))
        print(data, np.sum(~np.isnan(data)))


    elif fname.split('.')[-1]=='bin':
        data = np.fromfile(output_path + fname)
        fig, ax = plt.subplots(1,1)
        ax.plot(data)
        fig.savefig(output_path + '1_' + fname.split('.')[0] + '.png', dpi=300)
        print('Plot saved at :  ', output_path + fname.split('.')[0] + '.png')

        #fname_new = fname.split('.')[0] + '.txt'
        #np.savetxt(output_path + fname_new, np.fromfile(output_path + fname))


