#include "Basin.h"

int Basin::Mixing_full(double storage, double &cstorage, double input, double cinput){

    if ((storage + input) > roundoffERR){
        cstorage = (storage * cstorage + input * cinput) / (storage + input);
    }

    return EXIT_SUCCESS;
}
