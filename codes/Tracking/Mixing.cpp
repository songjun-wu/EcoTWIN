#include "Basin.h"

int Basin::Mixing_full(double storage, double &cstorage, double input, double cinput){

    if (input > roundoffERR){ // if there is inflow
        cstorage = (storage * cstorage + input * cinput) / (storage + input);
    } 
    else if ((input + storage) <= 0) {
        cstorage = 0.0;
    }


    return EXIT_SUCCESS;
}
