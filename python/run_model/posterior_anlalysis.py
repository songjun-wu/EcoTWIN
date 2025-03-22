import os
import numpy as np
import matplotlib.pyplot as plt
from def_GEM import Path

output_path = Path.output_path


fnames = os.listdir(output_path)
for fname in fnames:
    fname_new = fname.split('.')[0] + '.txt'
    np.savetxt(output_path + fname_new, np.fromfile(output_path + fname))

"""
ovf = np.fromfile(output_path + 'overland_flow_map.bin').reshape(-1, 630, 481)

plt.imshow(np.log(ovf[0,:,:]))
plt.savefig(output_path + 'ovf.png')
print(ovf.shape)"
"""