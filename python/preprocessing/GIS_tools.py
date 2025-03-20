import numpy as np

def d8_flow_direction(dem, nodata):
    kernel = np.array([[32, 64, 128],
                       [16,  0,   1],
                       [8,   4,   2]])
    directions = np.full(dem.shape, nodata)
    
    for i in range(1, dem.shape[0] - 1):
        for j in range(1, dem.shape[1] - 1):
            if np.isnan(dem[i, j]):
                continue
            window = dem[i-1:i+2, j-1:j+2]
            diff = window[1, 1] - window
            diff[1, 1] = -np.inf  # Ignore center cell
            diff[np.isnan(window)] = -np.inf  # Ignore NaN values
            directions[i, j] = kernel[np.unravel_index(np.argmax(diff), diff.shape)]
    return directions




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







def calc_flow_acc(fdir):
    offsets = {1: (0, 1), 2: (1, 1), 4: (1, 0), 8: (1, -1),
           16: (0, -1), 32: (-1, -1), 64: (-1, 0), 128: (-1, 1)}
    from collections import deque
    rows, cols = fdir.shape
    acc = np.ones((rows, cols), dtype=np.int32)  # each cell contributes 1 (itself)
    dep = np.zeros((rows, cols), dtype=np.int32)

    # Count number of inflowing (upstream) cells for each cell
    for i in range(rows):
        for j in range(cols):
            d = fdir[i, j]
            if d in offsets:
                ni, nj = i + offsets[d][0], j + offsets[d][1]
                if 0 <= ni < rows and 0 <= nj < cols:
                    dep[ni, nj] += 1

    # Process cells in topological order using a queue
    q = deque((i, j) for i in range(rows) for j in range(cols) if dep[i, j] == 0)
    while q:
        i, j = q.popleft()
        d = fdir[i, j]
        if d in offsets:
            ni, nj = i + offsets[d][0], j + offsets[d][1]
            if 0 <= ni < rows and 0 <= nj < cols:
                acc[ni, nj] += acc[i, j]
                dep[ni, nj] -= 1
                if dep[ni, nj] == 0:
                    q.append((ni, nj))
    return acc


def modify_dem_based_on_fdir(dem, fdir, sorted_cells, epsilon=0.01):

    offsets = {1: (0, 1), 2: (1, 1), 4: (1, 0), 8: (1, -1),
           16: (0, -1), 32: (-1, -1), 64: (-1, 0), 128: (-1, 1)}
    flag = True
    iter = 0
    while flag:
        flag = False
        for i,j in sorted_cells:
            if np.isnan(dem[i, j]):
                continue
            window = dem[i-1:i+2, j-1:j+2]
            d = fdir[i, j]
            if d in offsets:
                ni, nj = i + offsets[d][0], j + offsets[d][1]
                if dem[ni, nj] != np.nanmin(window):
                    dem[ni, nj] = np.nanmin(window) - epsilon


        iter+=1
    return dem

def sort_grid_based_on_fdir(fdir, nodata=0):
        temp = np.copy(fdir)
        rowNum, colNum = temp.shape
        map2array = []
        counter = 0

        # Count valid cells (non-nodata and between 1 and 9)
        for r in range(1, rowNum - 1):
            for c in range(1, colNum - 1):
                value = temp[r, c]
                if 1 <= value <= 129:
                    counter += 1
        # Process cells until all are sorted
        iter = 0
        while len(map2array) < counter:
            
            for r in range(1, rowNum - 1):
                for c in range(1, colNum - 1):
                    value = temp[r, c]
                    if value == nodata:
                        continue

                    # Check neighboring cells
                    value7 = temp[r - 1, c - 1]
                    value8 = temp[r - 1, c]
                    value9 = temp[r - 1, c + 1]
                    value4 = temp[r, c - 1]
                    value6 = temp[r, c + 1]
                    value1 = temp[r + 1, c - 1]
                    value2 = temp[r + 1, c]
                    value3 = temp[r + 1, c + 1]

                    # If no flow into this cell, add to sorted list
                    condition = (value7 != 2 and value8 != 4 and value9 != 8 and
                        value4 != 1 and value6 != 16 and value1 != 128 and
                        value2 != 64 and value3 != 32 and value != nodata)

                    if condition:
                        map2array.append([r, c])
            iter += 1
            # Mark processed cells as nodata
            for i in range(len(map2array)):
                r = map2array[i][0]
                c = map2array[i][1]
                temp[r, c] = nodata

        return map2array