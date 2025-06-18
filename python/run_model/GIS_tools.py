

def from_catchment_to_EU(upper_left_coord, mask_small, arr_large, arr_small):

    # upper_left_coord: Coordinates of upper left corner [row, col]
    # mask: mask != nodata will be regarded as valid grid cells
    # arr_large: European raster
    # arr_small: catchment raster

    for r in range(mask_small.shape[0]):
        for c in range(mask_small.shape[1]):
            if mask_small[r,c]:
                arr_large[r + upper_left_coord[0], c + upper_left_coord[1]] = arr_small[r,c]
    return arr_large