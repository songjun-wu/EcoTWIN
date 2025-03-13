

class Opt:
    cond = {}
    # parameters to calibrate
    cond['none'] = {'key':None, 'value':None,  'description':'General variables'}
    cond['canopy_0'] = {'key':'opt_canopy', 'value':1,  'description':'Canopy intercpetion'}
    cond['snow_0']   = {'key':'opt_snow', 'value':1, 'description':'degree day function for snow melt'}


class Param:
    param = {}
    # parameters to calibrate
    param['albedoS']   = {'condition':Opt.cond['canopy_0']}