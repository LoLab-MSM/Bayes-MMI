import numpy as np

def example_get_postprobs(df,add_to_dict=False,priordict={},which_evidence='Z'):
    #priordict default empty dict, could be that or None
    if not (type(priordict) is dict or priordict==None):
        print('priordict passed as incorrect variable, priordict will now be None')
        priordict = None
    try:
        if not (which_evidence.upper()=='Z' or which_evidence.upper()=='INS_Z'):
            print('which_evidence passed as incorrect variable, which_evidence will default to Z rather than INS_Z')
            which_evidence='Z'
    except AttributeError:
        print('which_evidence passed as incorrect variable, which_evidence will default to Z rather than INS_Z')
        which_evidence = 'Z'
        pass
    postprob_dict = {}
    hasx1 = []
    nox1 = []
    for i in df.index:
        if 'x1' in i or 'uniform' in i:
            hasx1.append(i)
        elif not 'x1' in i and not 'uniform' in i:
            nox1.append(i)
        else:
            print('PROBLEM')
    if len(hasx1) > 0 and len(nox1) > 0:
        priorx1 = []
        priorhas = .5/len(hasx1)
        priorno = .5/len(nox1)
        if priordict is not None:
            priordict['priorx1'] = {}
            priordict['priorx1']['priorhas'] = priorhas
            priordict['priorx1']['priorno'] = priorno
        for i in df.index:
            if 'x1' in i or 'uniform' in i:
                priorx1.append(priorhas)
            elif not 'x1' in i and not 'uniform' in i:
                priorx1.append(priorno)
            else:
                print('PROBLEM')
        df['priorx1'] = priorx1
        if which_evidence=='Z':
            x1postlist = df.Z*df.priorx1 / (np.sum(df.Z*df.priorx1))
        else:
            x1postlist = df.INS_Z*df.priorx1 / (np.sum(df.INS_Z*df.priorx1))
        df['x1post'] = x1postlist
        to_sum = []
        for i in df.index:
            if 'x1' in i or 'uniform' in i:
                to_sum.append(df.loc[i]['x1post'])
    else:
        print('Either x1 not included in model set or it is the only option, no posterior probability possible')
        to_sum = [0]
    if add_to_dict:
        postprob_dict['x1_present'] = np.sum(to_sum)
    else:
        print('x1 posterior probability: '+str(np.sum(to_sum)))
    # x2
    hasx2 = []
    nox2 = []
    for i in df.index:
        if 'x2' in i or 'uniform' in i:
            hasx2.append(i)
        elif not 'x2' in i and not 'uniform' in i:
            nox2.append(i)
        else:
            print('PROBLEM')
    if len(hasx2) > 0 and len(nox2) > 0:
        priorx2 = []
        priorhas = .5/len(hasx2)
        priorno = .5/len(nox2)
        if priordict is not None:
            priordict['priorx2'] = {}
            priordict['priorx2']['priorhas'] = priorhas
            priordict['priorx2']['priorno'] = priorno
        for i in df.index:
            if 'x2' in i or 'uniform' in i:
                priorx2.append(priorhas)
            elif not 'x2' in i and not 'uniform' in i:
                priorx2.append(priorno)
            else:
                print('PROBLEM')
        df['priorx2'] = priorx2
        if which_evidence=='Z':
            x2postlist = df.Z*df.priorx2 / (np.sum(df.Z*df.priorx2))
        else:
            x2postlist = df.INS_Z*df.priorx2 / (np.sum(df.INS_Z*df.priorx2))
        df['x2post'] = x2postlist
        to_sum = []
        for i in df.index:
            if 'x2' in i or 'uniform' in i:
                to_sum.append(df.loc[i]['x2post'])
    else:
        print('Either x2 not included in model set or it is the only option, no posterior probability possible')
        to_sum = [0]
    if add_to_dict:
            postprob_dict['x2_present'] = np.sum(to_sum)
    else:
        print('x2 posterior probability: '+str(np.sum(to_sum)))
    # x3
    hasx3 = []
    nox3 = []
    for i in df.index:
        if 'x3' in i or 'uniform' in i:
            hasx3.append(i)
        elif not 'x3' in i and not 'uniform' in i:
            nox3.append(i)
        else:
            print('PROBLEM')
    if len(hasx3) > 0 and len(nox3) > 0:
        priorx3 = []
        priorhas = .5/len(hasx3)
        priorno = .5/len(nox3)
        if priordict is not None:
            priordict['priorx3'] = {}
            priordict['priorx3']['priorhas'] = priorhas
            priordict['priorx3']['priorno'] = priorno
        for i in df.index:
            if 'x3' in i or 'uniform' in i:
                priorx3.append(priorhas)
            elif not 'x3' in i and not 'uniform' in i:
                priorx3.append(priorno)
            else:
                print('PROBLEM')
        df['priorx3'] = priorx3
        if which_evidence=='Z':
            x3postlist = df.Z*df.priorx3 / (np.sum(df.Z*df.priorx3))
        else:
            x3postlist = df.INS_Z*df.priorx3 / (np.sum(df.INS_Z*df.priorx3))
        df['x3post'] = x3postlist
        to_sum = []
        for i in df.index:
            if 'x3' in i or 'uniform' in i:
                to_sum.append(df.loc[i]['x3post'])
    else:
        print('Either x3 not included in model set or it is the only option, no posterior probability possible')
        to_sum = [0]
    if add_to_dict:
        postprob_dict['x3_present'] = np.sum(to_sum)
    else:
        print('x3 posterior probability: '+str(np.sum(to_sum)))
    # A2 to A
    hasx4 = []
    nox4 = []
    for i in df.index:
        if 'x4' in i or 'uniform' in i:
            hasx4.append(i)
        elif not 'x4' in i and not 'uniform' in i:
            nox4.append(i)
        else:
            print('PROBLEM')
    if len(hasx4) > 0 and len(nox4) > 0:
        priorx4 = []
        priorhas = .5/len(hasx4)
        priorno = .5/len(nox4)
        if priordict is not None:
            priordict['priorx4'] = {}
            priordict['priorx4']['priorhas'] = priorhas
            priordict['priorx4']['priorno'] = priorno
        for i in df.index:
            if 'x4' in i or 'uniform' in i:
                priorx4.append(priorhas)
            elif not 'x4' in i and not 'uniform' in i:
                priorx4.append(priorno)
            else:
                print('PROBLEM')
        df['priorx4'] = priorx4
        if which_evidence=='Z':
            x4postlist = df.Z*df.priorx4 / (np.sum(df.Z*df.priorx4))
        else:
            x4postlist = df.INS_Z*df.priorx4 / (np.sum(df.INS_Z*df.priorx4))
        df['x4post'] = x4postlist
        to_sum = []
        for i in df.index:
            if 'x4' in i or 'uniform' in i:
                to_sum.append(df.loc[i]['x4post'])
    else:
        print('Either x4 not included in candidate models or it is the only option, no posterior probability possible')
        to_sum = [0]
    if add_to_dict:
        postprob_dict['x4_present'] = np.sum(to_sum)
    else:
        print('x4 posterior probability: '+str(np.sum(to_sum)))


def example_get_param_importance(df,add_to_dict=False,which_IC='AICc'):
    # delta_AIC and w_AIC need to be calculated for the df (AIC or AICc), or delta_BIC and x
    # actually the same calculation as for AIC/AICc but technically called a probability (p) rather than a weight (w)
    delta_term = 'delta_'+which_IC
    df[delta_term] = df[which_IC] - np.min(df[which_IC])
    prob_related_term = -1
    if which_IC in ['AIC','AICc']:
        prob_related_term = 'w_'+which_IC
    elif which_IC == 'BIC':
        prob_related_term = 'p_'+which_IC
    else:
        print('Incompatible information criterion provided ('+which_IC+'). \'which_IC\' must be one of the following: AIC, AICc, BIC.')
        return
    df[prob_related_term] = np.exp(-.5 * df[delta_term]) / np.sum(np.exp(-.5 * df[delta_term]))
    #df['delta_AICc'] = df.AICc - np.min(df.AICc)
    #df['w_AICc'] = np.exp(-.5 * df.delta_AICc) / np.sum(np.exp(-.5 * df.delta_AICc))
    #
    paramimp_dict = {}
    hasx1 = []
    nox1 = []
    for i in df.index:
        if 'x1' in i or 'uniform' in i:
            hasx1.append(i)
        elif not 'x1' in i and not 'uniform' in i:
            nox1.append(i)
        else:
            print('PROBLEM')
    if len(hasx1) > 0 and len(nox1) > 0:
        to_sum = []
        for i in df.index:
            if 'x1' in i or 'uniform' in i:
                to_sum.append(df.loc[i][prob_related_term])
    else:
        print('x1 not included in model set or it is the only option, SW will not be meaningful so returning zero')
        to_sum = [0]
    if add_to_dict:
        paramimp_dict['x1_present'] = np.sum(to_sum)
    else:
        print('x1 posterior probability: '+str(np.sum(to_sum)))
    # x2
    hasx2 = []
    nox2 = []
    for i in df.index:
        if 'x2' in i or 'uniform' in i:
            hasx2.append(i)
        elif not 'x2' in i and not 'uniform' in i:
            nox2.append(i)
        else:
            print('PROBLEM')
    if len(hasx2) > 0 and len(nox2) > 0:
        to_sum = []
        for i in df.index:
            if 'x2' in i or 'uniform' in i:
                to_sum.append(df.loc[i][prob_related_term])
    else:
        print('x2 not included in model set or it is the only option, SW will not be meaningful so returning zero')
        to_sum = [0]
    if add_to_dict:
            paramimp_dict['x2_present'] = np.sum(to_sum)
    else:
        print('x2 posterior probability: '+str(np.sum(to_sum)))
    # x3
    hasx3 = []
    nox3 = []
    for i in df.index:
        if 'x3' in i or 'uniform' in i:
            hasx3.append(i)
        elif not 'x3' in i and not 'uniform' in i:
            nox3.append(i)
        else:
            print('PROBLEM')
    if len(hasx3) > 0 and len(nox3) > 0:
        to_sum = []
        for i in df.index:
            if 'x3' in i or 'uniform' in i:
                to_sum.append(df.loc[i][prob_related_term])
    else:
        print('x3 not included in model set or it is the only option, SW will not be meaningful so returning zero')
        to_sum = [0]
    if add_to_dict:
        paramimp_dict['x3_present'] = 1-np.sum(to_sum)
    else:
        print('x3 posterior probability: '+str(np.sum(to_sum)))
    # x4
    hasx4 = []
    nox4 = []
    for i in df.index:
        if 'x4' in i or 'uniform' in i:
            hasx4.append(i)
        elif not 'x4' in i and not 'uniform' in i:
            nox4.append(i)
        else:
            print('PROBLEM')
    if len(hasx4) > 0 and len(nox4) > 0:
        to_sum = []
        for i in df.index:
            if 'x4' in i or 'uniform' in i:
                to_sum.append(df.loc[i][prob_related_term])
    else:
        print('x4 not included in model set or it is the only option, SW will not be meaningful so returning zero')
        to_sum = [0]
    if add_to_dict:
        paramimp_dict['x4_present'] = np.sum(to_sum)
    else:
        print('x4 posterior probability: '+str(np.sum(to_sum)))
