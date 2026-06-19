# EcoTWIN: an Ecohydrological model that Tracks Water, Isotopes, and Nutrients


## Introduction
EcoTWIN is a C++-based ecohydrological modelling framework designed for the integrated simulation of water, isotope, carbon, and nitrogen cycles. The model incorporates a wide range of process representations and provides the flexibility to switch between alternative conceptualisations according to the objectives and characteristics of a study catchment.

A unique feature of EcoTWIN is the isotope tracking, which allows it to track the flow path and velocities of vertical and lateral hydrological fluxes. 

The model also employs a dynamic parameterisation scheme, which allows boundary conditions (e.g., land use) and related model parameters to be updated at user-defined intervals during simulation. This capability enables the model to represent evolving boundary conditions, such as land-use change, vegetation dynamics, and management interventions.



## Publicatons
Wu, S., Soulsby, C., Zheng, Y., Musolff, A., & Tetzlaff, D. (2026). Divergent evolution of nitrogen cycling along gradients of landscape water velocities. _Science_, 392(6803), 1188–1193. https://doi.org/10.1126/science.aed0399

Wu, S., Tetzlaff, D., Zheng, Y., & Soulsby, C. (2026). EcoTWIN 1.0: a fully distributed tracer-aided ecohydrological model tracking water, isotopes, and nutrients. _Geoscientific Model Development_, 19, 2257–2278. https://doi.org/10.5194/gmd-19-2257-2026



## Model strucutre
EcoTWIN simulates the coupled terrestrial cycles of water, carbon, and nitrogen.

**Hydrological cycling**

The hydrological module represents _canopy interception, canopy evaporation, throughfall, snow accumulation and melt, infiltration, percolation, soil evaporation, depth-dependent transpiration, groundwater recharge, streamflow routing, and in-stream evaporation_.

In addition, EcoTWIN tracks the transport of water and dissolved substances (e.g., stable isotopes, nitrate, and dissolved organic carbon) across the landscape through three major flow pathways: _overland flow on the land surface, shallow groundwater flow through the vadose zone, and deep groundwater flow within the saturated zone_.


**Carbon cycling**

The carbon module simulates _gross primary production (GPP), net primary production (NPP), vegetation growth, litterfall, transfers among litter pools, humus formation, and the decomposition of soil and aquatic organic matter_.

_Carbon decomposition_ is linked to _gaseous carbon losses_, allowing the estimation of carbon fluxes such as _CO₂ emissions_.

**Nitrogen cycling**

Nitrogen cycling is tightly coupled with carbon dynamics. _Plant nitrogen uptake_ is determined by vegetation growth demand, while _mineralisation_ and _immobilisation_ are regulated by _transformations among carbon pools with different C to N ratios_.

The model also includes representations of _soil and in-stream denitrification processes_.

**Anthropogenic Management**

EcoTWIN incorporates a range of anthropogenic management practices, including:

* _Irrigation_;
* _Artificial drainage_;
* _Fertiliser application_;
* _Manure application_;
* _Crop harvest_.

These management modules enable the assessment of human impacts on coupled water, carbon, and nitrogen cycling across scales.

![Strucuture of EcoTWIN](docs/model_structure_v2.0.jpg)




## Instruction
A complete working example is provided in:  ***./examples/catchment_1***.
The routine contains the follwoing five steps:

**1 .Compliation**

Currently, EcoTWIN can only be deployed on Linux.  
For compilation, simply direct to ***Release-Linux*** and make.

    cd MODEL_PATH/Release_linux  
    make  

**2. Configuration**

EcoTWIN is configured primarily through the _config.ini_.  
A template is given in:  ***./examples/catchment_1/config.ini***.

- Specify the path of spetial inputs, climate inputs, and outputs in *Path section*.  
- Switch on/off isotopic and nutrient module in *Option section*. The conceptualisation of each process can also be switched between different modules.  
- Specify Climate, GIS, and Parameter inputs in corresponding sections.  
- Specify the fluxes/stages for output in *Reports section*  


**3. Data preparation**

Due to the flexible structure of EcoTWIN, the inputs are not fixed. The preparation of model inputs aligns with the configuration, and are documented in _config.ini_.
The spatial and climate inputs are based on ***./examples/catchment_1/spatial*** and ***./examples/catchment_1/climate***


**4. Execution**
To run EcoTWIN, simply distribute all inputs and executable in the working directory into the following structure.
* **working_directory**  
  * **Spatial_path** (_folder contains all asc outputs; specified in config.ini_)  
     * dem.asc  
     * fdir.asc  
     * ...  
  * **Climate_path** (_folder contains all climate outputs; specified in config.ini_)  
    * P.bin   
    * T.bin  
    * ...  
  * **Output_path** (_folder contains all model outputs_)
  * **config.ini**  (_configuration file_)
  * **Crop_info.ini**  (_Crop information_)
  * **param.ini**  (_parameter names and values_)
  * **EcoTWIN**  (_EcoTWIN executable_)  
  
  
Then direct to the working directory, and run EcoTWIN.  

    cd working_directory
    ./EcoTWIN

Simulation results will be written to the output directory specified in _config.ini_.
