#include "Basin.h"

int Basin::Routing_ovf(Control &ctrl, Param &par){

    int r, c, d, rr, cc, lat_ok;

    for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
        r = _sortedGrid.row[j];
        c = _sortedGrid.col[j];

        _Qs->matrix[r][c] = 1;
    }

    for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
        r = _sortedGrid.row[j];
        c = _sortedGrid.col[j];
        d = _sortedGrid.dir[j];

        lat_ok = 0;
        switch (d) 
        {
        case 8:
            rr = r+1;
            cc = c-1;
            lat_ok = 1;
        break;
        case 4:
            rr = r+1;
            cc = c;
            lat_ok = 1;
        break;
        case 2:
            rr = r+1;
            cc = c+1;
            lat_ok = 1;
        break;
        case 16:
            rr = r;
            cc = c-1;
            lat_ok = 1;
        break;
        case 5: //if it is an outlet
            break;
        case 1:
            rr = r;
            cc = c+1;
            lat_ok = 1;
        break;
        case 32:
            rr = r-1;
            cc = c-1;
            lat_ok = 1;
        break;
        case 64:
            rr = r-1;
            cc = c;
            lat_ok = 1;
        break;
        case 128:
            rr = r-1;
            cc = c+1;
            lat_ok = 1;
        break;
        default:
        return -1;
        }

        _Qs->matrix[rr][cc] += _Qs->matrix[r][c];
    }

    return EXIT_SUCCESS;
}