import numpy as np
import pyDOE


# All at a time sampling
def AAT_sampling(xmins, xmaxs, xdistribution, nsample):
    nparam = len(xmins)

    X = pyDOE.lhs(nparam, nsample)   # X dim = [N, M]
    for i in range(nparam):
        if xdistribution[i]=='uniform':
            X[:,i] = xmins[i] + (xmaxs[i] - xmins[i]) * X[:,i]
        elif xdistribution[i]=='log':
            X[:,i] = 10**(np.log10(xmins[i]) + (np.log10(xmaxs[i]) - np.log10(xmins[i])) * X[:,i])

    return X

# One at a time sampling
def OAT_sampling(xmins, xmaxs, xdistribution, nsample, des_type):
    from numpy.matlib import repmat

    nparam = len(xmins)

    X_AAT = AAT_sampling(xmins, xmaxs, xdistribution, 2*nsample)  # dim = nsample*2, nparam
    
    X = np.full((nsample*(nparam+1), nparam), np.nan)

    counter = 0
    for i in range(nsample):  # repeat for nsample times
        a = X_AAT[i*2, :]
        b = X_AAT[i*2+1, :]
        
        X[counter, :] = a
        counter += 1

        x = repmat(a, nparam, 1) # dim = nparam, nparam; repeat base array a for M times (pertubate M times later - once for each param)

        if des_type == 'radial':
            for j in range(nparam):
                x[j, j] = b[j]
                X[counter, :] = x[j, :]
                counter += 1

        elif des_type == 'trajectory':
            for j in range(nparam):
                x[j, 0:j+1] = b[0:j+1]
                X[counter, :] = x[j, :]
                counter += 1
        else:
            raise ValueError('"des_type" must be one among ["radial", "trajectory"]')
        
    return X

# Calculate the Morris indices
def EE_indices(nsample, xmins, xmaxs, X, Y, design_type, filterPercentage):

    """
    X   parameter matrix            (nsample*(nparam+1), nparam)
    Y   associated output values    (nsample*(nparam+1))
    """

    nparam = len(xmins)

    EE = np.full((nsample, nparam), np.nan)
    k = 0
    ki = 0

    for i in range(nsample):
        for j in range(nparam):
            if design_type == 'radial':
                EE[i, j] = (Y[k+1]-Y[ki]) / (X[k+1, j]-X[ki, j]) * (xmaxs[j] - xmins[j])
            elif design_type == 'trajectory':
                idx = abs(X[k+1, :]-X[k, :]) > 0
                if sum(idx) != 1:
                    raise ValueError('X[%d,:] and X[%d,:] differ in more ' % (k, k+1) +
                                     'than one component, or are equivalent')
                EE[i, idx] = (Y[k+1]-Y[k]) / (X[k+1, idx]-X[k, idx]) * (xmaxs[idx] - xmins[idx])

            else:
                raise ValueError('"design_type" must be one among ["radial",  "trajectory"]')

            k += 1
        k += 1
        ki += k
    

    # exclude the abnormal sets
    filteredIDX = int(filterPercentage * EE.shape[0])
    if filteredIDX==0:
        EE_filtered = EE
    else:
        dim_tmp = EE.shape[0] - filteredIDX*2
        
        EE_filtered = np.full((dim_tmp, EE.shape[1]), np.nan)

        for i in range(EE.shape[1]):        
            idx_tmp = np.argsort(EE[:,i])[filteredIDX:-filteredIDX]
            EE_filtered[:, i] = EE[idx_tmp, i]

    mi = np.nanmean(abs(EE_filtered), axis=0) # mean absolute value of EE (excluding NaNs)
    sigma = np.nanstd(EE_filtered, axis=0) # std of EE (excluding NaNs)
      
    return mi, sigma, EE_filtered