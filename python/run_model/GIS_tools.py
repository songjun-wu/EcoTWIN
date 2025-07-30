
import numpy as np


def from_catchment_to_EU(upper_left_coord, mask_small, arr_large, arr_small):

    # upper_left_coord: Coordinates of upper left corner [row, col]
    # mask: mask != nodata will be regarded as valid grid cells
    # arr_large: European raster
    # arr_small: catchment raster

    for r in range(mask_small.shape[0]):
        for c in range(mask_small.shape[1]):
            if mask_small[r,c]:
                if arr_large.ndim == 2:
                    arr_large[r + upper_left_coord[0], c + upper_left_coord[1]] = arr_small[r,c]
                elif arr_large.ndim == 3:
                    arr_large[:, r + upper_left_coord[0], c + upper_left_coord[1]] = arr_small[:,r,c]
    return arr_large


def from_EU_to_catchment(upper_left_coord, mask, arr_large, nodata):

    # upper_left_coord: Coordinates of upper left corner [row, col]
    # mask: mask != nodata will be regarded as valid grid cells
    # arr_large: European raster
    # arr_small: catchment raster

    x_corner = int(upper_left_coord[0])
    y_corner = int(upper_left_coord[1])
    if x_corner >= 0 and x_corner+mask.shape[0]<arr_large.shape[0] and y_corner>=0 and y_corner+mask.shape[1]<arr_large.shape[1]:
        arr_small = np.copy(arr_large)[x_corner:x_corner+mask.shape[0], y_corner:y_corner+mask.shape[1]]
    else:
        arr_small = np.copy(arr_large)[(x_corner+1):(x_corner+mask.shape[0]-1), (y_corner+1):(y_corner+mask.shape[1]-1)]
        arr_small = add_edge(arr_small, ext=1, no_data=-9999)

    arr_small[np.isnan(mask)] = nodata

    return arr_small


def add_edge(arr, ext=1, no_data = -9999.0):

    rows, cols = arr.shape
    rows += ext * 2
    cols += ext * 2

    arr_new = np.full((rows, cols), no_data).astype(np.float64)
    arr_new[ext:rows-ext, ext:cols-ext] = arr

    return arr_new


