

class Opt:
    cond = {}
    # Options
    cond['none'] = {'key':None, 'value':None,  'description':'General variables'}

    cond['climate_input_format_2'] = {'key':'opt_climate_input_format', 'value':2,
                                      'general_description':'How is climate inputs orgainsed? 1 = raster; 2 = aggregated binary file (climate_zone file should be specified)',
                                      'description':'Binary inputs based on cliamte zones'}
    cond['tracking_isotope_1'] = {'key':'opt_tracking_isotope', 'value':1,
                                  'general_description':'Enable isotopic tracking? 0:disabled, 1:enabled',
                                  'description':'Isotopic tracking'}
    
    cond['intecept_1']   = {'key':'opt_intecept', 'value':1, 
                        'general_description':'Canopy interception. 1:maximum canopy storage unmodified; 2:storage corrected (Landarf et al., 2024)',
                        'description':'Maximum canopy storage unmodified'}
    
    cond['intecept_2']   = {'key':'opt_intecept', 'value':2, 
                        'general_description':'Canopy interception. 1:maximum canopy storage unmodified; 2:maximum canopy storage corrected (Landarf et al., 2024)',
                        'description':'Maximum canopy storage corrected (Landarf et al., 2024)'}

    cond['snow_1']   = {'key':'opt_snow', 'value':1, 
                        'general_description':'Snow accumulation method. 1:Degree day factor method',
                        'description':'Degree day factor method for snow melt'}


class setting:
    max_category = 10


    