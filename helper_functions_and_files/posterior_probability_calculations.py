import numpy as np
import pandas as pd

# hypothesis names to list-based (hypbuilder) numbers
hypo_to_num = {}
hypo_to_num['div_Yeff'] = [1,7,13,19]
hypo_to_num['div_A2Yeff'] = [2,8,14,20]
hypo_to_num['div_noeff'] = [3,9,15,21]
hypo_to_num['die_Yeff'] = [4,10,16,22]
hypo_to_num['die_A2Yeff'] = [5,11,17,23]
hypo_to_num['die_noeff'] = [6,12,18,24]
hypo_to_num['diff_firsthalf_Yeff'] = [25,28]
hypo_to_num['diff_firsthalf_A2Yeff'] = [26,29]
hypo_to_num['diff_firsthalf_noeff'] = [27,30]
hypo_to_num['diff_lasthalf_Yeff'] = [31,34]
hypo_to_num['diff_lasthalf_A2Yeff'] = [32,35]
hypo_to_num['diff_lasthalf_noeff'] = [33,36]
hypo_to_num['AtoA2'] = [50]
hypo_to_num['AtoN'] = [49]
hypo_to_num['A2toY'] = [52]
hypo_to_num['NtoY'] = [51]
hypo_to_num['NtoA2'] = [37]
hypo_to_num['AtoY'] = [38]
hypo_to_num['A2toN'] = [39]
hypo_to_num['YtoA'] = [40]
hypo_to_num['NtoA'] = [41]
hypo_to_num['YtoN'] = [42]
hypo_to_num['A2toA'] = [43]
hypo_to_num['YtoA2'] = [44]

# and the other direction
num_to_hypo = {}
for j in [v for k, v in hypo_to_num.items()]:
    for z in j:
        num_to_hypo[z] = [k for k, v in hypo_to_num.items() if z in v][0]

for j in [1,2,3,4,5,6]:
    num_to_hypo[j]+='_A'

for j in [7,8,9,10,11,12]:
    num_to_hypo[j]+='_N'

for j in [13,14,15,16,17,18]:
    num_to_hypo[j]+='_A2'

for j in [19,20,21,22,23,24]:
    num_to_hypo[j]+='_Y'

for j in [25,26,27]:
    num_to_hypo[j]+='_A_A2'

for j in [28,29,30]:
    num_to_hypo[j]+='_A_N'

for j in [31,32,33]:
    num_to_hypo[j]+='_A2_Y'

for j in [34,35,36]:
    num_to_hypo[j]+='_N_Y'

def get_postprobs_allbutstructure(df,add_to_dict=False,priordict={},which_evidence='INS_Z'):
    #priordict default empty dict, could be that or None
    if not (type(priordict) is dict or priordict==None):
        print('priordict passed as incorrect variable, priordict will now be None')
        priordict = None
    try:
        if not which_evidence in ['Z','INS_Z','BIC_marglik_est']:
            print('which_evidence passed as incorrect variable, \'which_evidence will\' default to INS_Z')
            which_evidence='INS_Z'
    except AttributeError:
        print('which_evidence passed as incorrect variable, \'which_evidence\' will default to INS_Z')
        which_evidence = 'INS_Z'
        pass
    postprob_dict = {}
    hasAN = []
    noAN = []
    for i in df.index:
        x = [int(j) for j in df.loc[i]['model_makeup'].split(',')]
        if 28 in x or 29 in x or 30 in x:
            hasAN.append(df.loc[i].model_makeup)
        if not (28 in x or 29 in x or 30 in x):
            noAN.append(df.loc[i].model_makeup)
    if len(hasAN) > 0 and len(noAN) > 0:
        priorAN = []
        priorhas = .5/len(hasAN)
        priorno = .5/len(noAN)
        if priordict is not None:
            priordict['priorAN'] = {}
            priordict['priorAN']['priorhas'] = priorhas
            priordict['priorAN']['priorno'] = priorno
        for i in df.index:
            x = [int(j) for j in df.loc[i]['model_makeup'].split(',')]
            if 28 in x or 29 in x or 30 in x:
                priorAN.append(priorhas)
            if not (28 in x or 29 in x or 30 in x):
                priorAN.append(priorno)
        df['priorAN_'+which_evidence] = priorAN
        ANpostlist = df[which_evidence]*df['priorAN_'+which_evidence] / (np.sum(df[which_evidence]*df['priorAN_'+which_evidence]))
        df['ANpost_'+which_evidence] = ANpostlist
        to_sum = []
        for i in df.index:
            x = [int(j) for j in df.loc[i]['model_makeup'].split(',')]
            if 28 in x or 29 in x or 30 in x:
                to_sum.append(df.loc[i]['ANpost_'+which_evidence])
    else:
        print('Either A ->N not included or it is the only option, no posterior probability possible')
        to_sum = [0]
    if add_to_dict:
        for j in hypo_to_num['AtoN']:
            postprob_dict[j] = 1-np.sum(to_sum)
    else:
        print('A ->N posterior probability: '+str(np.sum(to_sum)))
    # N to A
    hasNA = []
    noNA = []
    for i in df.index:
        x = [int(j) for j in df.loc[i]['model_makeup'].split(',')]
        if 41 in x:
            hasNA.append(df.loc[i].model_makeup)
        if not 41 in x:
            noNA.append(df.loc[i].model_makeup)
    if len(hasNA) > 0 and len(noNA) > 0:
        priorNA = []
        priorhas = .5/len(hasNA)
        priorno = .5/len(noNA)
        if priordict is not None:
            priordict['priorNA'] = {}
            priordict['priorNA']['priorhas'] = priorhas
            priordict['priorNA']['priorno'] = priorno
        for i in df.index:
            x = [int(j) for j in df.loc[i]['model_makeup'].split(',')]
            if 41 in x:
                priorNA.append(priorhas)
            if not 41 in x:
                priorNA.append(priorno)
        df['priorNA_'+which_evidence] = priorNA
        NApostlist = df[which_evidence]*df['priorNA_'+which_evidence] / (np.sum(df[which_evidence]*df['priorNA_'+which_evidence]))
        df['NApost_'+which_evidence] = NApostlist
        to_sum = []
        for i in df.index:
            x = [int(j) for j in df.loc[i]['model_makeup'].split(',')]
            if 41 in x:
                to_sum.append(df.loc[i]['NApost_'+which_evidence])
    else:
        print('Either N ->A not included or it is the only option, no posterior probability possible')
        to_sum = [0]
    if add_to_dict:
        for j in hypo_to_num['NtoA']:
            postprob_dict[j] = np.sum(to_sum)
    else:
        print('N ->A posterior probability: '+str(np.sum(to_sum)))
    # A to A2
    hasAA2 = []
    noAA2 = []
    for i in df.index:
        x = [int(j) for j in df.loc[i]['model_makeup'].split(',')]
        if 25 in x or 26 in x or 27 in x:
            hasAA2.append(df.loc[i].model_makeup)
        if not (25 in x or 26 in x or 27 in x):
            noAA2.append(df.loc[i].model_makeup)
    if len(hasAA2) > 0 and len(noAA2) > 0:
        priorAA2 = []
        priorhas = .5/len(hasAA2)
        priorno = .5/len(noAA2)
        if priordict is not None:
            priordict['priorAA2'] = {}
            priordict['priorAA2']['priorhas'] = priorhas
            priordict['priorAA2']['priorno'] = priorno
        for i in df.index:
            x = [int(j) for j in df.loc[i]['model_makeup'].split(',')]
            if 25 in x or 26 in x or 27 in x:
                priorAA2.append(priorhas)
            if not (25 in x or 26 in x or 27 in x):
                priorAA2.append(priorno)
        df['priorAA2_'+which_evidence] = priorAA2
        AA2postlist = df[which_evidence]*df['priorAA2_'+which_evidence] / (np.sum(df[which_evidence]*df['priorAA2_'+which_evidence]))
        df['AA2post_'+which_evidence] = AA2postlist
        to_sum = []
        for i in df.index:
            x = [int(j) for j in df.loc[i]['model_makeup'].split(',')]
            if 25 in x or 26 in x or 27 in x:
                to_sum.append(df.loc[i]['AA2post_'+which_evidence])
    else:
        print('Either A -> A2 not included or it is the only option, no posterior probability possible')
        to_sum = [0]
    if add_to_dict:
        for j in hypo_to_num['AtoA2']:
            postprob_dict[j] = 1-np.sum(to_sum)
    else:
        print('A ->A2 posterior probability: '+str(np.sum(to_sum)))
    # A2 to A
    hasA2A = []
    noA2A = []
    for i in df.index:
        x = [int(j) for j in df.loc[i]['model_makeup'].split(',')]
        if 43 in x:
            hasA2A.append(df.loc[i].model_makeup)
        if not 43 in x:
            noA2A.append(df.loc[i].model_makeup)
    if len(hasA2A) > 0 and len(noA2A) > 0:
        priorA2A = []
        priorhas = .5/len(hasA2A)
        priorno = .5/len(noA2A)
        if priordict is not None:
            priordict['priorA2A'] = {}
            priordict['priorA2A']['priorhas'] = priorhas
            priordict['priorA2A']['priorno'] = priorno
        for i in df.index:
            x = [int(j) for j in df.loc[i]['model_makeup'].split(',')]
            if 43 in x:
                priorA2A.append(priorhas)
            if not 43 in x:
                priorA2A.append(priorno)
        df['priorA2A_'+which_evidence] = priorA2A
        A2Apostlist = df[which_evidence]*df['priorA2A_'+which_evidence] / (np.sum(df[which_evidence]*df['priorA2A_'+which_evidence]))
        df['A2Apost_'+which_evidence] = A2Apostlist
        to_sum = []
        for i in df.index:
            x = [int(j) for j in df.loc[i]['model_makeup'].split(',')]
            if 43 in x:
                to_sum.append(df.loc[i]['A2Apost_'+which_evidence])
    else:
        print('Either A2 -> A not included or it is the only option, no posterior probability possible')
        to_sum = [0]
    if add_to_dict:
        for j in hypo_to_num['A2toA']:
            postprob_dict[j] = np.sum(to_sum)
    else:
        print('A2 ->A posterior probability: '+str(np.sum(to_sum)))
    # N to Y
    hasNY = []
    noNY = []
    for i in df.index:
        x = [int(j) for j in df.loc[i]['model_makeup'].split(',')]
        if 34 in x or 35 in x or 36 in x:
            hasNY.append(df.loc[i].model_makeup)
        if not (34 in x or 35 in x or 36 in x):
            noNY.append(df.loc[i].model_makeup)
    if len(hasNY) > 0 and len(noNY) > 0:
        priorNY = []
        priorhas = .5/len(hasNY)
        priorno = .5/len(noNY)
        if priordict is not None:
            priordict['priorNY'] = {}
            priordict['priorNY']['priorhas'] = priorhas
            priordict['priorNY']['priorno'] = priorno
        for i in df.index:
            x = [int(j) for j in df.loc[i]['model_makeup'].split(',')]
            if 34 in x or 35 in x or 36 in x:
                priorNY.append(priorhas)
            if not (34 in x or 35 in x or 36 in x):
                priorNY.append(priorno)
        df['priorNY_'+which_evidence] = priorNY
        NYpostlist = df[which_evidence]*df['priorNY_'+which_evidence] / (np.sum(df[which_evidence]*df['priorNY_'+which_evidence]))
        df['NYpost_'+which_evidence] = NYpostlist
        to_sum = []
        for i in df.index:
            x = [int(j) for j in df.loc[i]['model_makeup'].split(',')]
            if 34 in x or 35 in x or 36 in x:
                to_sum.append(df.loc[i]['NYpost_'+which_evidence])
    else:
        print('Either N -> Y not included or it is the only option, no posterior probability possible')
        to_sum = [0]
    if add_to_dict:
        for j in hypo_to_num['NtoY']:
            postprob_dict[j] = 1-np.sum(to_sum)
    else:
        print('N ->Y posterior probability: '+str(np.sum(to_sum)))
    # Y to N
    hasYN = []
    noYN = []
    for i in df.index:
        x = [int(j) for j in df.loc[i]['model_makeup'].split(',')]
        if 42 in x:
            hasYN.append(df.loc[i].model_makeup)
        if not 42 in x:
            noYN.append(df.loc[i].model_makeup)
    if len(hasYN) > 0 and len(noYN) > 0:
        priorYN = []
        priorhas = .5/len(hasYN)
        priorno = .5/len(noYN)
        if priordict is not None:
            priordict['priorYN'] = {}
            priordict['priorYN']['priorhas'] = priorhas
            priordict['priorYN']['priorno'] = priorno
        for i in df.index:
            x = [int(j) for j in df.loc[i]['model_makeup'].split(',')]
            if 42 in x:
                priorYN.append(priorhas)
            if not 42 in x:
                priorYN.append(priorno)
        df['priorYN_'+which_evidence] = priorYN
        YNpostlist = df[which_evidence]*df['priorYN_'+which_evidence] / (np.sum(df[which_evidence]*df['priorYN_'+which_evidence]))
        df['YNpost_'+which_evidence] = YNpostlist
        to_sum = []
        for i in df.index:
            x = [int(j) for j in df.loc[i]['model_makeup'].split(',')]
            if 42 in x:
                to_sum.append(df.loc[i]['YNpost_'+which_evidence])
    else:
        print('Either Y -> N not included or it is the only option, no posterior probability possible')
        to_sum = [0]
    if add_to_dict:
        for j in hypo_to_num['YtoN']:
            postprob_dict[j] = np.sum(to_sum)
    else:
        print('Y ->N posterior probability: '+str(np.sum(to_sum)))
    # A2 to Y
    hasA2Y = []
    noA2Y = []
    for i in df.index:
        x = [int(j) for j in df.loc[i]['model_makeup'].split(',')]
        if 31 in x or 32 in x or 33 in x:
            hasA2Y.append(df.loc[i].model_makeup)
        if not (31 in x or 32 in x or 33 in x):
            noA2Y.append(df.loc[i].model_makeup)
    if len(hasA2Y) > 0 and len(noA2Y) > 0:
        priorA2Y = []
        priorhas = .5/len(hasA2Y)
        priorno = .5/len(noA2Y)
        if priordict is not None:
            priordict['priorA2Y'] = {}
            priordict['priorA2Y']['priorhas'] = priorhas
            priordict['priorA2Y']['priorno'] = priorno
        for i in df.index:
            x = [int(j) for j in df.loc[i]['model_makeup'].split(',')]
            if 31 in x or 32 in x or 33 in x:
                priorA2Y.append(priorhas)
            if not (31 in x or 32 in x or 33 in x):
                priorA2Y.append(priorno)
        df['priorA2Y_'+which_evidence] = priorA2Y
        A2Ypostlist = df[which_evidence]*df['priorA2Y_'+which_evidence] / (np.sum(df[which_evidence]*df['priorA2Y_'+which_evidence]))
        df['A2Ypost_'+which_evidence] = A2Ypostlist
        to_sum = []
        for i in df.index:
            x = [int(j) for j in df.loc[i]['model_makeup'].split(',')]
            if 31 in x or 32 in x or 33 in x:
                to_sum.append(df.loc[i]['A2Ypost_'+which_evidence])
    else:
        print('Either A2 ->Y not included or it is the only option, no posterior probability possible')
        to_sum = [0]
    if add_to_dict:
        for j in hypo_to_num['A2toY']:
            postprob_dict[j] = 1-np.sum(to_sum)
    else:
        print('A2 ->Y posterior probability: '+str(np.sum(to_sum)))
    # Y to A2
    hasYA2 = []
    noYA2 = []
    for i in df.index:
        x = [int(j) for j in df.loc[i]['model_makeup'].split(',')]
        if 44 in x:
            hasYA2.append(df.loc[i].model_makeup)
        if not 44 in x:
            noYA2.append(df.loc[i].model_makeup)
    if len(hasYA2) > 0 and len(noYA2) > 0:
        priorYA2 = []
        priorhas = .5/len(hasYA2)
        priorno = .5/len(noYA2)
        if priordict is not None:
            priordict['priorYA2'] = {}
            priordict['priorYA2']['priorhas'] = priorhas
            priordict['priorYA2']['priorno'] = priorno
        for i in df.index:
            x = [int(j) for j in df.loc[i]['model_makeup'].split(',')]
            if 44 in x:
                priorYA2.append(priorhas)
            if not 44 in x:
                priorYA2.append(priorno)
        df['priorYA2_'+which_evidence] = priorYA2
        YA2postlist = df[which_evidence]*df['priorYA2_'+which_evidence] / (np.sum(df[which_evidence]*df['priorYA2_'+which_evidence]))
        df['YA2post_'+which_evidence] = YA2postlist
        to_sum = []
        for i in df.index:
            x = [int(j) for j in df.loc[i]['model_makeup'].split(',')]
            if 44 in x:
                to_sum.append(df.loc[i]['YA2post_'+which_evidence])
    else:
        print('Either Y -> A2 not included or it is the only option, no posterior probability possible')
        to_sum = [0]
    if add_to_dict:
        for j in hypo_to_num['YtoA2']:
            postprob_dict[j] = np.sum(to_sum)
    else:
        print('Y ->A2 posterior probability: '+str(np.sum(to_sum)))
    # A to Y
    hasAY = []
    noAY = []
    for i in df.index:
        x = [int(j) for j in df.loc[i]['model_makeup'].split(',')]
        if 38 in x:
            hasAY.append(df.loc[i].model_makeup)
        if not 38 in x:
            noAY.append(df.loc[i].model_makeup)
    if len(hasAY) > 0 and len(noAY) > 0:
        priorAY = []
        priorhas = .5/len(hasAY)
        priorno = .5/len(noAY)
        if priordict is not None:
            priordict['priorAY'] = {}
            priordict['priorAY']['priorhas'] = priorhas
            priordict['priorAY']['priorno'] = priorno
        for i in df.index:
            x = [int(j) for j in df.loc[i]['model_makeup'].split(',')]
            if 38 in x:
                priorAY.append(priorhas)
            if not 38 in x:
                priorAY.append(priorno)
        df['priorAY_'+which_evidence] = priorAY
        AYpostlist = df[which_evidence]*df['priorAY_'+which_evidence] / (np.sum(df[which_evidence]*df['priorAY_'+which_evidence]))
        df['AYpost_'+which_evidence] = AYpostlist
        to_sum = []
        for i in df.index:
            x = [int(j) for j in df.loc[i]['model_makeup'].split(',')]
            if 38 in x:
                to_sum.append(df.loc[i]['AYpost_'+which_evidence])
    else:
        print('Either A -> Y not included or it is the only option, no posterior probability possible')
        to_sum = [0]
    if add_to_dict:
        for j in hypo_to_num['AtoY']:
            postprob_dict[j] = np.sum(to_sum)
    else:
        print('A ->Y posterior probability: '+str(np.sum(to_sum)))
    # Y to A
    hasYA = []
    noYA = []
    for i in df.index:
        x = [int(j) for j in df.loc[i]['model_makeup'].split(',')]
        if 40 in x:
            hasYA.append(df.loc[i].model_makeup)
        if not 40 in x:
            noYA.append(df.loc[i].model_makeup)
    if len(hasYA) > 0 and len(noYA) > 0:
        priorYA = []
        priorhas = .5/len(hasYA)
        priorno = .5/len(noYA)
        if priordict is not None:
            priordict['priorYA'] = {}
            priordict['priorYA']['priorhas'] = priorhas
            priordict['priorYA']['priorno'] = priorno
        for i in df.index:
            x = [int(j) for j in df.loc[i]['model_makeup'].split(',')]
            if 40 in x:
                priorYA.append(priorhas)
            if not 40 in x:
                priorYA.append(priorno)
        df['priorYA_'+which_evidence] = priorYA
        YApostlist = df[which_evidence]*df['priorYA_'+which_evidence] / (np.sum(df[which_evidence]*df['priorYA_'+which_evidence]))
        df['YApost_'+which_evidence] = YApostlist
        to_sum = []
        for i in df.index:
            x = [int(j) for j in df.loc[i]['model_makeup'].split(',')]
            if 40 in x:
                to_sum.append(df.loc[i]['YApost_'+which_evidence])
    else:
        print('Either Y -> A not included or it is the only option, no posterior probability possible')
        to_sum = [0]
    if add_to_dict:
        for j in hypo_to_num['YtoA']:
            postprob_dict[j] = np.sum(to_sum)
    else:
        print('Y ->A posterior probability: '+str(np.sum(to_sum)))
    # N to A2
    hasNA2 = []
    noNA2 = []
    for i in df.index:
        x = [int(j) for j in df.loc[i]['model_makeup'].split(',')]
        if 37 in x:
            hasNA2.append(df.loc[i].model_makeup)
        if not 37 in x:
            noNA2.append(df.loc[i].model_makeup)
    if len(hasNA2) > 0 and len(noNA2) > 0:
        priorNA2 = []
        priorhas = .5/len(hasNA2)
        priorno = .5/len(noNA2)
        if priordict is not None:
            priordict['priorNA2'] = {}
            priordict['priorNA2']['priorhas'] = priorhas
            priordict['priorNA2']['priorno'] = priorno
        for i in df.index:
            x = [int(j) for j in df.loc[i]['model_makeup'].split(',')]
            if 37 in x:
                priorNA2.append(priorhas)
            if not 37 in x:
                priorNA2.append(priorno)
        df['priorNA2_'+which_evidence] = priorNA2
        NA2postlist = df[which_evidence]*df['priorNA2_'+which_evidence] / (np.sum(df[which_evidence]*df['priorNA2_'+which_evidence]))
        df['NA2post_'+which_evidence] = NA2postlist
        to_sum = []
        for i in df.index:
            x = [int(j) for j in df.loc[i]['model_makeup'].split(',')]
            if 37 in x:
                to_sum.append(df.loc[i]['NA2post_'+which_evidence])
    else:
        print('Either N ->A2 not included or it is the only option, no posterior probability possible')
        to_sum = [0]
    if add_to_dict:
        for j in hypo_to_num['NtoA2']:
            postprob_dict[j] = np.sum(to_sum)
    else:
        print('N ->A2 posterior probability: '+str(np.sum(to_sum)))
    # A2 to N
    hasA2N = []
    noA2N = []
    for i in df.index:
        x = [int(j) for j in df.loc[i]['model_makeup'].split(',')]
        if 39 in x:
            hasA2N.append(df.loc[i].model_makeup)
        if not 39 in x:
            noA2N.append(df.loc[i].model_makeup)
    if len(hasA2N) > 0 and len(noA2N) > 0:
        priorA2N = []
        priorhas = .5/len(hasA2N)
        priorno = .5/len(noA2N)
        if priordict is not None:
            priordict['priorA2N'] = {}
            priordict['priorA2N']['priorhas'] = priorhas
            priordict['priorA2N']['priorno'] = priorno
        for i in df.index:
            x = [int(j) for j in df.loc[i]['model_makeup'].split(',')]
            if 39 in x:
                priorA2N.append(priorhas)
            if not 39 in x:
                priorA2N.append(priorno)
        df['priorA2N_'+which_evidence] = priorA2N
        A2Npostlist = df[which_evidence]*df['priorA2N_'+which_evidence] / (np.sum(df[which_evidence]*df['priorA2N_'+which_evidence]))
        df['A2Npost_'+which_evidence] = A2Npostlist
        to_sum = []
        for i in df.index:
            x = [int(j) for j in df.loc[i]['model_makeup'].split(',')]
            if 39 in x:
                to_sum.append(df.loc[i]['A2Npost_'+which_evidence])
    else:
        print('Either A2 ->N not included or it is the only option, no posterior probability possible')
        to_sum = [0]
    if add_to_dict:
        for j in hypo_to_num['A2toN']:
            postprob_dict[j] = np.sum(to_sum)
    else:
        print('A2 ->N posterior probability: '+str(np.sum(to_sum)))
    # division effects at all (added later)
    hasdiveff = []
    nodiveff = []
    for i in df.index:
        x = [int(j) for j in df.loc[i]['model_makeup'].split(',')]
        if 1 in x or 7 in x or 13 in x or 19 in x or 2 in x or 8 in x or 14 in x or 20 in x:
            hasdiveff.append(df.loc[i].model_makeup)
        if not (1 in x or 7 in x or 13 in x or 19 in x or 2 in x or 8 in x or 14 in x or 20 in x):
            nodiveff.append(df.loc[i].model_makeup)
    if len(hasdiveff) > 0 and len(nodiveff) > 0:
        priordiveff = []
        priorhas = 0.5 / len(hasdiveff)
        priorno = 0.5 / len(nodiveff)
        if priordict is not None:
            priordict['priordiveff_any'] = {}
            priordict['priordiveff_any']['priorhas'] = priorhas
            priordict['priordiveff_any']['priorno'] = priorno
        for i in df.index:
            x = [int(j) for j in df.loc[i]['model_makeup'].split(',')]
            if 1 in x or 7 in x or 13 in x or 19 in x or 2 in x or 8 in x or 14 in x or 20 in x:
                priordiveff.append(priorhas)
            if not (1 in x or 7 in x or 13 in x or 19 in x or 2 in x or 8 in x or 14 in x or 20 in x):
                priordiveff.append(priorno)
        df['priordiveff_any_'+which_evidence] = priordiveff
        diveff_postlist = df[which_evidence] * df['priordiveff_any_'+which_evidence] / (np.sum(df[which_evidence] * df['priordiveff_any_'+which_evidence]))
        df['diveffpost_any_'+which_evidence] = diveff_postlist
        the_sum = np.sum(df.loc[df['priordiveff_any_'+which_evidence] == priorhas]['diveffpost_any_'+which_evidence])
    else:
        print('Only one possibility (all models have no division effects or all models have division effects), '
              'no posterior probability possible')
        the_sum = 0
    if add_to_dict:
        postprob_dict['div_any'] = the_sum
    else:
        print('any effect on division posterior probability: '+str(the_sum))
    # division effects separated by who the effects are by
    # (division effect probability is same as for death probability so not included)
    hasdiveffA2Y = []
    hasdiveffYonly = []
    nodiveff = []
    for i in df.index:
        x = [int(j) for j in df.loc[i]['model_makeup'].split(',')]
        if 1 in x or 7 in x or 13 in x or 19 in x:
            hasdiveffYonly.append(df.loc[i].model_makeup)
        if 2 in x or 8 in x or 14 in x or 20 in x:
            hasdiveffA2Y.append(df.loc[i].model_makeup)
        if not (1 in x or 7 in x or 13 in x or 19 in x or 2 in x or 8 in x or 14 in x or 20 in x):
            nodiveff.append(df.loc[i].model_makeup)
    if (len(nodiveff) > 0 and len(hasdiveffYonly) > 0) or (len(nodiveff) > 0 and len(hasdiveffA2Y) > 0) or (len(hasdiveffYonly) > 0 and len(hasdiveffA2Y) > 0):
        #have some with no effect, some with Y, maybe some with A2... so this one could be all 3, OR just no vs Y
        #have some with no effect, some with A2, maybe some with Y... probably not because that would be caught by the first one
        #have some with Y, some with A2... any with no effect would have been caught by the first 2 statements
        priordiveffspec = []
        priorhasY = 0
        priorhasA2Y = 0
        priorno = 0
        if len(nodiveff) > 0 and len(hasdiveffYonly) > 0 and len(hasdiveffA2Y) > 0:
            priorhasY = (1/3)/len(hasdiveffYonly)
            priorhasA2Y = (1/3)/len(hasdiveffA2Y)
            priorno = (1/3)/len(nodiveff)
        else:   # everything else would only have 2, not all 3
            if len(hasdiveffYonly) > 0:
                priorhasY = (1/2)/len(hasdiveffYonly)
            if len(hasdiveffA2Y) > 0:
                priorhasA2Y = (1/2)/len(hasdiveffA2Y)
            if len(nodiveff) > 0:
                priorno = (1/2)/len(nodiveff)
        if priordict is not None:
            priordict['priordiveff_spec'] = {}
            priordict['priordiveff_spec']['priorhasY'] = priorhasY
            priordict['priordiveff_spec']['priorhasA2Y'] = priorhasA2Y
            priordict['priordiveff_spec']['priorno'] = priorno
        for i in df.index:
            x = [int(j) for j in df.loc[i]['model_makeup'].split(',')]
            if 1 in x or 7 in x or 13 in x or 19 in x:
                priordiveffspec.append(priorhasY)
            if 2 in x or 8 in x or 14 in x or 20 in x:
                priordiveffspec.append(priorhasA2Y)
            if not (1 in x or 7 in x or 13 in x or 19 in x or 2 in x or 8 in x or 14 in x or 20 in x):
                priordiveffspec.append(priorno)
        df['priordiveff_spec_'+which_evidence] = priordiveffspec
        diveff_spec_postlist = df[which_evidence]*df['priordiveff_spec_'+which_evidence] / (np.sum(df[which_evidence]*df['priordiveff_spec_'+which_evidence]))
        df['diveffpost_spec_'+which_evidence] = diveff_spec_postlist
        to_sum_Y = []
        to_sum_A2Y = []
        for i in df.index:
            x = [int(j) for j in df.loc[i]['model_makeup'].split(',')]
            if 1 in x or 7 in x or 13 in x or 19 in x:
                to_sum_Y.append(df.loc[i]['diveffpost_spec_'+which_evidence])
            if 2 in x or 8 in x or 14 in x or 20 in x:
                to_sum_A2Y.append(df.loc[i]['diveffpost_spec_'+which_evidence])
    else:
        print('No comparisons between effect on division/death (only one effect tested), no posterior probability returned')
        to_sum_Y = [0]
        to_sum_A2Y = [0]
    if add_to_dict:
        for j in hypo_to_num['div_Yeff']:
            postprob_dict[j] = np.sum(to_sum_Y)
        for j in hypo_to_num['div_A2Yeff']:
            postprob_dict[j] = np.sum(to_sum_A2Y)
        for j in hypo_to_num['div_noeff']:
            postprob_dict[j] = 1-(np.sum(to_sum_A2Y)+np.sum(to_sum_Y))
    else:
        print('division effect from Y posterior probability: ' + str(np.sum(to_sum_Y)))
        print('division effect from A2&Y posterior probability: '+str(np.sum(to_sum_A2Y)))
        print('no division effect posterior probability: '+str(1-(np.sum(to_sum_A2Y)+np.sum(to_sum_Y))))
    # effects at all on first-half (early) transitions (added later)
    hashalfeff = []
    nohalfeff = []
    for i in df.index:
        x = [int(j) for j in df.loc[i]['model_makeup'].split(',')]
        if 25 in x or 28 in x or 26 in x or 29 in x:
            hashalfeff.append(df.loc[i].model_makeup)
        if not (25 in x or 28 in x or 26 in x or 29 in x):
            nohalfeff.append(df.loc[i].model_makeup)
    if len(hashalfeff) > 0 and len(nohalfeff) > 0:
        priorhalfeff = []
        priorhas = 0.5 / len(hashalfeff)
        priorno = 0.5 / len(nohalfeff)
        if priordict is not None:
            priordict['priorhalfeff_any'] = {}
            priordict['priorhalfeff_any']['priorhas'] = priorhas
            priordict['priorhalfeff_any']['priorno'] = priorno
        for i in df.index:
            x = [int(j) for j in df.loc[i]['model_makeup'].split(',')]
            if 25 in x or 28 in x or 26 in x or 29 in x:
                priorhalfeff.append(priorhas)
            if not (25 in x or 28 in x or 26 in x or 29 in x):
                priorhalfeff.append(priorno)
        df['priorhalfeff_any_'+which_evidence] = priorhalfeff
        halfeff_postlist = df[which_evidence] * df['priorhalfeff_any_'+which_evidence] / (np.sum(df[which_evidence] * df['priorhalfeff_any_'+which_evidence]))
        df['halfeffpost_any_'+which_evidence] = halfeff_postlist
        the_sum = np.sum(df.loc[df['priorhalfeff_any_'+which_evidence] == priorhas]['halfeffpost_any_'+which_evidence])
    else:
        print('Only one possibility (all models have no early-transition effects or all models have these effects), '
              'no posterior probability possible')
        the_sum = 0
    if add_to_dict:
        postprob_dict['diff_firsthalf_any'] = the_sum
    else:
        print('early-transition effects at all posterior probability: ' + str(the_sum))
    # firsthalfeff but where the effect comes from
    hashalfeffY = []
    hashalfeffA2Y = []
    nohalfeff = []
    for i in df.index:
        x = [int(j) for j in df.loc[i]['model_makeup'].split(',')]
        if 25 in x or 28 in x:
            hashalfeffY.append(df.loc[i].model_makeup)
        if 26 in x or 29 in x:
            hashalfeffA2Y.append(df.loc[i].model_makeup)
        if not (25 in x or 28 in x or 26 in x or 29 in x):
            nohalfeff.append(df.loc[i].model_makeup)
    if (len(nohalfeff) > 0 and len(hashalfeffY) > 0) or (len(nohalfeff) > 0 and len(hashalfeffA2Y) > 0) or (len(hashalfeffY) > 0 and len(hashalfeffA2Y) > 0):
        priorhalfeff_spec = []
        priorhasY = 0
        priorhasA2Y = 0
        priorno = 0
        if len(nohalfeff) > 0 and len(hashalfeffY) > 0 and len(hashalfeffA2Y) > 0:
            priorhasY = (1/3)/len(hashalfeffY)
            priorhasA2Y = (1/3)/len(hashalfeffA2Y)
            priorno = (1/3)/len(nohalfeff)
        else:   # everything else would only have 2, not all 3
            if len(hashalfeffY) > 0:
                priorhasY = (1/2)/len(hashalfeffY)
            if len(hashalfeffA2Y) > 0:
                priorhasA2Y = (1/2)/len(hashalfeffA2Y)
            if len(nohalfeff) > 0:
                priorno = (1/2)/len(nohalfeff)
        if priordict is not None:
            priordict['priorhalfeff_spec'] = {}
            priordict['priorhalfeff_spec']['priorhasY'] = priorhasY
            priordict['priorhalfeff_spec']['priorhasA2Y'] = priorhasA2Y
            priordict['priorhalfeff_spec']['priorno'] = priorno
        for i in df.index:
            x = [int(j) for j in df.loc[i]['model_makeup'].split(',')]
            if 25 in x or 28 in x:
                priorhalfeff_spec.append(priorhasY)
            if 26 in x or 29 in x:
                priorhalfeff_spec.append(priorhasA2Y)
            if not (25 in x or 28 in x or 26 in x or 29 in x):
                priorhalfeff_spec.append(priorno)
        df['priorhalfeff_spec_'+which_evidence] = priorhalfeff_spec
        halfeff_spec_postlist = df[which_evidence]*df['priorhalfeff_spec_'+which_evidence] / (np.sum(df[which_evidence]*df['priorhalfeff_spec_'+which_evidence]))
        df['halfeffpost_spec_'+which_evidence] = halfeff_spec_postlist
        to_sum_Y = []
        to_sum_A2Y = []
        for i in df.index:
            x = [int(j) for j in df.loc[i]['model_makeup'].split(',')]
            if 25 in x or 28 in x:
                to_sum_Y.append(df.loc[i]['halfeffpost_spec_'+which_evidence])
            if 26 in x or 29 in x:
                to_sum_A2Y.append(df.loc[i]['halfeffpost_spec_'+which_evidence])
    else:
        print('No comparisons between effect on early transitions (only one effect tested), no posterior probability returned')
        to_sum_Y = [0]
        to_sum_A2Y = [0]
    if add_to_dict:
        for j in hypo_to_num['diff_firsthalf_Yeff']:
            postprob_dict[j] = np.sum(to_sum_Y)
        for j in hypo_to_num['diff_firsthalf_A2Yeff']:
            postprob_dict[j] = np.sum(to_sum_A2Y)
        for j in hypo_to_num['diff_firsthalf_noeff']:
            postprob_dict[j] = 1-(np.sum(to_sum_A2Y)+np.sum(to_sum_Y))
    else:
        print('early-transition effect from Y posterior probability: ' + str(np.sum(to_sum_Y)))
        print('early-transition effect from A2&Y posterior probability: '+str(np.sum(to_sum_A2Y)))
        print('no early-transition effect posterior probability: '+str(1-(np.sum(to_sum_A2Y)+np.sum(to_sum_Y))))
    # effects at all on second-half (late) transitions (added later)
    hasendeff = []
    noendeff = []
    for i in df.index:
        x = [int(j) for j in df.loc[i]['model_makeup'].split(',')]
        if 31 in x or 34 in x or 32 in x or 35 in x:
            hasendeff.append(df.loc[i].model_makeup)
        if not (31 in x or 32 in x or 34 in x or 35 in x):
            noendeff.append(df.loc[i].model_makeup)
    if len(hasendeff) > 0 and len(noendeff) > 0:
        priorendeff = []
        priorhas = 0.5 / len(hasendeff)
        priorno = 0.5 / len(noendeff)
        if priordict is not None:
            priordict['priorendeff_any'] = {}
            priordict['priorendeff_any']['priorhas'] = priorhas
            priordict['priorendeff_any']['priorno'] = priorno
        for i in df.index:
            x = [int(j) for j in df.loc[i]['model_makeup'].split(',')]
            if 31 in x or 34 in x or 32 in x or 35 in x:
                priorendeff.append(priorhas)
            if not (31 in x or 32 in x or 34 in x or 35 in x):
                priorendeff.append(priorno)
        df['priorendeff_any_'+which_evidence] = priorendeff
        endeff_postlist = df[which_evidence] * df['priorendeff_any_'+which_evidence] / (np.sum(df[which_evidence] * df['priorendeff_any_'+which_evidence]))
        df['endeffpost_any_'+which_evidence] = endeff_postlist
        the_sum = np.sum(df.loc[df['priorendeff_any_'+which_evidence] == priorhas]['endeffpost_any_'+which_evidence])
    else:
        print('Only one possibility (all models have no late-transition effects or all models have these effects), '
              'no posterior probability possible')
        the_sum = 0
    if add_to_dict:
        postprob_dict['diff_lasthalf_any'] = the_sum
    else:
        print('late-transition effects at all, posterior probability: ' + str(the_sum))
    # secondhalfeff, but with where that effect comes from
    hasendeffY = []
    hasendeffA2Y = []
    noendeff = []
    for i in df.index:
        x = [int(j) for j in df.loc[i]['model_makeup'].split(',')]
        if 31 in x or 34 in x:
            hasendeffY.append(df.loc[i].model_makeup)
        if 32 in x or 35 in x:
            hasendeffA2Y.append(df.loc[i].model_makeup)
        if not (31 in x or 32 in x or 34 in x or 35 in x):
            noendeff.append(df.loc[i].model_makeup)
    if (len(noendeff) > 0 and len(hasendeffY) > 0) or (len(noendeff) > 0 and len(hasendeffA2Y) > 0) or (len(hasendeffY) > 0 and len(hasendeffA2Y) > 0):
        priorendeff_spec = []
        priorhasY = 0
        priorhasA2Y = 0
        priorno = 0
        if len(noendeff) > 0 and len(hasendeffY) > 0 and len(hasendeffA2Y) > 0:
            priorhasY = (1/3)/len(hasendeffY)
            priorhasA2Y = (1/3)/len(hasendeffA2Y)
            priorno = (1/3)/len(noendeff)
        else:   # everything else would only have 2, not all 3
            if len(hasendeffY) > 0:
                priorhasY = (1/2)/len(hasendeffY)
            if len(hasendeffA2Y) > 0:
                priorhasA2Y = (1/2)/len(hasendeffA2Y)
            if len(noendeff) > 0:
                priorno = (1/2)/len(noendeff)
        if priordict is not None:
            priordict['priorendeff_spec'] = {}
            priordict['priorendeff_spec']['priorhasY'] = priorhasY
            priordict['priorendeff_spec']['priorhasA2Y'] = priorhasA2Y
            priordict['priorendeff_spec']['priorno'] = priorno
        for i in df.index:
            x = [int(j) for j in df.loc[i]['model_makeup'].split(',')]
            if 31 in x or 34 in x:
                priorendeff_spec.append(priorhasY)
            if 32 in x or 35 in x:
                priorendeff_spec.append(priorhasA2Y)
            if not (31 in x or 32 in x or 34 in x or 35 in x):
                priorendeff_spec.append(priorno)
        df['priorendeff_spec_'+which_evidence] = priorendeff_spec
        endeff_spec_postlist = df[which_evidence]*df['priorendeff_spec_'+which_evidence] / (np.sum(df[which_evidence]*df['priorendeff_spec_'+which_evidence]))
        df['endeffpost_spec_'+which_evidence] = endeff_spec_postlist
        to_sum_Y = []
        to_sum_A2Y = []
        for i in df.index:
            x = [int(j) for j in df.loc[i]['model_makeup'].split(',')]
            if 31 in x or 34 in x:
                to_sum_Y.append(df.loc[i]['endeffpost_spec_'+which_evidence])
            if 32 in x or 35 in x:
                to_sum_A2Y.append(df.loc[i]['endeffpost_spec_'+which_evidence])
    else:
        print('No comparisons between effect on later transitions (only one effect tested), no posterior probability returned')
        to_sum_Y = [0]
        to_sum_A2Y = [0]
    if add_to_dict:
        for j in hypo_to_num['diff_lasthalf_Yeff']:
            postprob_dict[j] = np.sum(to_sum_Y)
        for j in hypo_to_num['diff_lasthalf_A2Yeff']:
            postprob_dict[j] = np.sum(to_sum_A2Y)
        for j in hypo_to_num['diff_lasthalf_noeff']:
            postprob_dict[j] = 1-(np.sum(to_sum_A2Y)+np.sum(to_sum_Y))
    else:
        print('late-transition effect from Y posterior probability: ' + str(np.sum(to_sum_Y)))
        print('late-transition effect from A2&Y posterior probability: '+str(np.sum(to_sum_A2Y)))
        print('no late-transition effect posterior probability: '+str(1-(np.sum(to_sum_A2Y)+np.sum(to_sum_Y))))
    # effect from Y or from A2 and Y, probability (i.e. if there are effects, which Non-NE 'group' is more likely?)
    # thus not considering models with no effects
    hasY = []
    hasA2Y = []
    doesnt = []
    for i in df.index:
        x = [int(j) for j in df.loc[i]['model_makeup'].split(',')]
        if 1 in x or 7 in x or 13 in x or 19 in x or 25 in x or 28 in x or 31 in x or 34 in x:
            hasY.append(df.loc[i].model_makeup)
        elif 2 in x or 8 in x or 14 in x or 20 in x or 26 in x or 29 in x or 32 in x or 35 in x:
            hasA2Y.append(df.loc[i].model_makeup)
        else:
            doesnt.append(df.loc[i].model_makeup)
    if len(hasY) > 0 and len(hasA2Y) > 0:
        priorwhichNonNE = []
        priorY = 0.5 / len(hasY)
        priorA2Y = 0.5 / len(hasA2Y)
        if priordict is not None:
            priordict['prioreff_whichNonNE'] = {}
            priordict['prioreff_whichNonNE']['priorhasY'] = priorY
            priordict['prioreff_whichNonNE']['priorhasA2Y'] = priorA2Y
        for i in df.index:
            x = [int(j) for j in df.loc[i]['model_makeup'].split(',')]
            if 1 in x or 7 in x or 13 in x or 19 in x or 25 in x or 28 in x or 31 in x or 34 in x:
                priorwhichNonNE.append(priorY)
            elif 2 in x or 8 in x or 14 in x or 20 in x or 26 in x or 29 in x or 32 in x or 35 in x:
                priorwhichNonNE.append(priorA2Y)
            else:
                priorwhichNonNE.append(0)
        df['priorwhichNonNE_'+which_evidence] = priorwhichNonNE
        whichNonNE_postlist = df[which_evidence] * df['priorwhichNonNE_'+which_evidence] / (np.sum(df[which_evidence] * df['priorwhichNonNE_'+which_evidence]))
        df['whichNonNEpost_'+which_evidence] = whichNonNE_postlist
        the_sum_Y = np.sum(df.loc[df['priorwhichNonNE_'+which_evidence] == priorY]['whichNonNEpost_'+which_evidence])
        the_sum_A2Y = np.sum(df.loc[df['priorwhichNonNE_'+which_evidence] == priorA2Y]['whichNonNEpost_'+which_evidence])
    else:
        print('Only one effect type (all models have effects from Y, or all models have effects from A2&Y - so no'
              'comparison between models with effects from Y vs those with effects from A2&Y), so'
              'no posterior probability possible ... disregarding models with no effects for this analysis so no'
              'posterior probability possible if no models have effects')
        the_sum_Y = 0
        the_sum_A2Y = 0
    if add_to_dict:
        postprob_dict['eff_Y_contrib'] = the_sum_Y
        postprob_dict['eff_A2_Y_contrib'] = the_sum_A2Y
    else:
        print('effects in the models are from Y, posterior probability: ' + str(the_sum_Y))
        print('effects in the models are from A2 and Y, posterior probability: ' + str(the_sum_A2Y))
    # starting state
    startsA = len(df[df['subtype_starting_and_makeup_code'].str.endswith('1000')])
    startsN = len(df[df['subtype_starting_and_makeup_code'].str.endswith('2000')])
    startsA2 = len(df[df['subtype_starting_and_makeup_code'].str.endswith('3000')])
    startsY = len(df[df['subtype_starting_and_makeup_code'].str.endswith('4000')])
    startsAN = len(df[df['subtype_starting_and_makeup_code'].str.endswith('1200')])
    startsAA2 = len(df[df['subtype_starting_and_makeup_code'].str.endswith('1300')])
    startsAY = len(df[df['subtype_starting_and_makeup_code'].str.endswith('1400')])
    startsNA2 = len(df[df['subtype_starting_and_makeup_code'].str.endswith('2300')])
    startsNY = len(df[df['subtype_starting_and_makeup_code'].str.endswith('2400')])
    startsA2Y = len(df[df['subtype_starting_and_makeup_code'].str.endswith('3400')])
    startsANA2 = len(df[df['subtype_starting_and_makeup_code'].str.endswith('1230')])
    startsANY = len(df[df['subtype_starting_and_makeup_code'].str.endswith('1240')])
    startsAA2Y = len(df[df['subtype_starting_and_makeup_code'].str.endswith('1340')])
    startsNA2Y = len(df[df['subtype_starting_and_makeup_code'].str.endswith('2340')])
    startsANA2Y = len(df[df['subtype_starting_and_makeup_code'].str.endswith('1234')])
    ## structure comparisons
    try:
        priorA = (1/15)/startsA
    except ZeroDivisionError:
        priorA = 0
    try:
        priorN = (1/15)/startsN
    except ZeroDivisionError:
        priorN = 0
    try:
        priorA2 = (1/15)/startsA2
    except ZeroDivisionError:
        priorA2 = 0
    try:
        priorY = (1/15)/startsY
    except ZeroDivisionError:
        priorY = 0
    try:
        priorAN = (1/15)/startsAN
    except ZeroDivisionError:
        priorAN = 0
    try:
        priorAA2 = (1/15)/startsAA2
    except ZeroDivisionError:
        priorAA2 = 0
    try:
        priorAY = (1/15)/startsAY
    except ZeroDivisionError:
        priorAY = 0
    try:
        priorNA2 = (1/15)/startsNA2
    except ZeroDivisionError:
        priorNA2 = 0
    try:
        priorNY = (1/15)/startsNY
    except ZeroDivisionError:
        priorNY = 0
    try:
        priorA2Y = (1/15)/startsA2Y
    except ZeroDivisionError:
        priorA2Y = 0
    try:
        priorANA2 = (1/15)/startsANA2
    except ZeroDivisionError:
        priorANA2 = 0
    try:
        priorANY = (1/15)/startsANY
    except ZeroDivisionError:
        priorANY = 0
    try:
        priorAA2Y = (1/15)/startsAA2Y
    except ZeroDivisionError:
        priorAA2Y = 0
    try:
        priorNA2Y = (1/15)/startsNA2Y
    except ZeroDivisionError:
        priorNA2Y = 0
    try:
        priorANA2Y = (1/15)/startsANA2Y
    except ZeroDivisionError:
        priorANA2Y = 0
    if priordict is not None:
        priordict['priorstarts'] = {}
        priordict['priorstarts']['priorA'] = priorA
        priordict['priorstarts']['priorN'] = priorN
        priordict['priorstarts']['priorA2'] = priorA2
        priordict['priorstarts']['priorY'] = priorY
        priordict['priorstarts']['priorAN'] = priorAN
        priordict['priorstarts']['priorAA2'] = priorAA2
        priordict['priorstarts']['priorAY'] = priorAY
        priordict['priorstarts']['priorNA2'] = priorNA2
        priordict['priorstarts']['priorNY'] = priorNY
        priordict['priorstarts']['priorA2Y'] = priorA2Y
        priordict['priorstarts']['priorANA2'] = priorANA2
        priordict['priorstarts']['priorANY'] = priorANY
        priordict['priorstarts']['priorAA2Y'] = priorAA2Y
        priordict['priorstarts']['priorNA2Y'] = priorNA2Y
        priordict['priorstarts']['priorANA2Y'] = priorANA2Y
    priorstarts = []
    for i in df.index:
        if df.loc[i]['subtype_starting_and_makeup_code'].endswith('1000'):
            priorstarts.append(priorA)
        elif df.loc[i]['subtype_starting_and_makeup_code'].endswith('2000'):
            priorstarts.append(priorN)
        elif df.loc[i]['subtype_starting_and_makeup_code'].endswith('3000'):
            priorstarts.append(priorA2)
        elif df.loc[i]['subtype_starting_and_makeup_code'].endswith('4000'):
           priorstarts.append(priorY)
        elif df.loc[i]['subtype_starting_and_makeup_code'].endswith('1200'):
            priorstarts.append(priorAN)
        elif df.loc[i]['subtype_starting_and_makeup_code'].endswith('1300'):
            priorstarts.append(priorAA2)
        elif df.loc[i]['subtype_starting_and_makeup_code'].endswith('1400'):
            priorstarts.append(priorAY)
        elif df.loc[i]['subtype_starting_and_makeup_code'].endswith('2300'):
            priorstarts.append(priorNA2)
        elif df.loc[i]['subtype_starting_and_makeup_code'].endswith('2400'):
            priorstarts.append(priorNY)
        elif df.loc[i]['subtype_starting_and_makeup_code'].endswith('3400'):
            priorstarts.append(priorA2Y)
        elif df.loc[i]['subtype_starting_and_makeup_code'].endswith('1230'):
            priorstarts.append(priorANA2)
        elif df.loc[i]['subtype_starting_and_makeup_code'].endswith('1240'):
            priorstarts.append(priorANY)
        elif df.loc[i]['subtype_starting_and_makeup_code'].endswith('1340'):
            priorstarts.append(priorAA2Y)
        elif df.loc[i]['subtype_starting_and_makeup_code'].endswith('2340'):
            priorstarts.append(priorNA2Y)
        elif df.loc[i]['subtype_starting_and_makeup_code'].endswith('1234'):
            priorstarts.append(priorANA2Y)
        else:
            print('issue, model '+str(i))
    df['priorstarts_'+which_evidence] = priorstarts
    startpostlist = df[which_evidence]*df['priorstarts_'+which_evidence] / (np.sum(df[which_evidence]*df['priorstarts_'+which_evidence]))
    df['startspost_'+which_evidence] = startpostlist
    # make sure the posterior probability sums to 1
    startA_sum = np.sum(df[df['subtype_starting_and_makeup_code'].str.endswith('1000')]['startspost_'+which_evidence])
    startN_sum = np.sum(df[df['subtype_starting_and_makeup_code'].str.endswith('2000')]['startspost_'+which_evidence])
    startA2_sum = np.sum(df[df['subtype_starting_and_makeup_code'].str.endswith('3000')]['startspost_'+which_evidence])
    startY_sum = np.sum(df[df['subtype_starting_and_makeup_code'].str.endswith('4000')]['startspost_'+which_evidence])
    startAN_sum = np.sum(df[df['subtype_starting_and_makeup_code'].str.endswith('1200')]['startspost_'+which_evidence])
    startAA2_sum = np.sum(df[df['subtype_starting_and_makeup_code'].str.endswith('1300')]['startspost_'+which_evidence])
    startAY_sum = np.sum(df[df['subtype_starting_and_makeup_code'].str.endswith('1400')]['startspost_'+which_evidence])
    startNA2_sum = np.sum(df[df['subtype_starting_and_makeup_code'].str.endswith('2300')]['startspost_'+which_evidence])
    startNY_sum = np.sum(df[df['subtype_starting_and_makeup_code'].str.endswith('2400')]['startspost_'+which_evidence])
    startA2Y_sum = np.sum(df[df['subtype_starting_and_makeup_code'].str.endswith('3400')]['startspost_'+which_evidence])
    startANA2_sum = np.sum(df[df['subtype_starting_and_makeup_code'].str.endswith('1230')]['startspost_'+which_evidence])
    startANY_sum = np.sum(df[df['subtype_starting_and_makeup_code'].str.endswith('1240')]['startspost_'+which_evidence])
    startAA2Y_sum = np.sum(df[df['subtype_starting_and_makeup_code'].str.endswith('1340')]['startspost_'+which_evidence])
    startNA2Y_sum = np.sum(df[df['subtype_starting_and_makeup_code'].str.endswith('2340')]['startspost_'+which_evidence])
    startANA2Y_sum = np.sum(df[df['subtype_starting_and_makeup_code'].str.endswith('1234')]['startspost_'+which_evidence])
    if add_to_dict:
        postprob_dict['starts_with_A'] = startA_sum
        postprob_dict['starts_with_N'] = startN_sum
        postprob_dict['starts_with_A2'] = startA2_sum
        postprob_dict['starts_with_Y'] = startY_sum
        postprob_dict['starts_with_AN'] = startAN_sum
        postprob_dict['starts_with_AA2'] = startAA2_sum
        postprob_dict['starts_with_AY'] = startAY_sum
        postprob_dict['starts_with_NA2'] = startNA2_sum
        postprob_dict['starts_with_NY'] = startNY_sum
        postprob_dict['starts_with_A2Y'] = startA2Y_sum
        postprob_dict['starts_with_ANA2'] = startANA2_sum
        postprob_dict['starts_with_ANY'] = startANY_sum
        postprob_dict['starts_with_AA2Y'] = startAA2Y_sum
        postprob_dict['starts_with_NA2Y'] = startNA2Y_sum
        postprob_dict['starts_with_ANA2Y'] = startANA2Y_sum
    else:
        print('starts with A posterior probability: '+str(startA_sum))
        print('starts with N posterior probability: '+str(startN_sum))
        print('starts with A2 posterior probability: '+str(startA2_sum))
        print('starts with Y posterior probability: '+str(startY_sum))
        print('starts with AN posterior probability: '+str(startAN_sum))
        print('starts with AA2 posterior probability: '+str(startAA2_sum))
        print('starts with AY posterior probability: '+str(startAY_sum))
        print('starts with NA2 posterior probability: '+str(startNA2_sum))
        print('starts with NY posterior probability: '+str(startNY_sum))
        print('starts with A2Y posterior probability: '+str(startA2Y_sum))
        print('starts with ANA2 posterior probability: '+str(startANA2_sum))
        print('starts with ANY posterior probability: '+str(startANY_sum))
        print('starts with AA2Y posterior probability: '+str(startAA2Y_sum))
        print('starts with NA2Y posterior probability: '+str(startNA2Y_sum))
        print('starts with ANA2Y posterior probability: '+str(startANA2Y_sum))
    if add_to_dict:
        #make the dict so that it doesnt include posterior probs for subtypes that aren't actually in the models
        j = set([y for z in [[int(j) for j in i.split(',')] for i in df.model_makeup] for y in z])
        #for j in checkmakeups:
        if not (1 in j or 2 in j or 3 in j): #or 4 in j or 5 in j or 6 in j): # not doing the death ones currently
            postprob_dict[1] = 0
            postprob_dict[2] = 0
            postprob_dict[3] = 0
        if not (7 in j or 8 in j or 9 in j): #or 4 in j or 5 in j or 6 in j): # not doing the death ones currently
            postprob_dict[7] = 0
            postprob_dict[8] = 0
            postprob_dict[9] = 0
        if not (13 in j or 14 in j or 15 in j): #or 4 in j or 5 in j or 6 in j): # not doing the death ones currently
            postprob_dict[13] = 0
            postprob_dict[14] = 0
            postprob_dict[15] = 0
        if not (19 in j or 20 in j or 21 in j): #or 4 in j or 5 in j or 6 in j): # not doing the death ones currently
            postprob_dict[19] = 0
            postprob_dict[20] = 0
            postprob_dict[21] = 0
        if not (25 in j or 26 in j or 27 in j): #or 4 in j or 5 in j or 6 in j): # not doing the death ones currently
            postprob_dict[25] = 0
            postprob_dict[26] = 0
            postprob_dict[27] = 0
        if not (28 in j or 29 in j or 30 in j): #or 4 in j or 5 in j or 6 in j): # not doing the death ones currently
            postprob_dict[28] = 0
            postprob_dict[29] = 0
            postprob_dict[30] = 0
        if not (31 in j or 32 in j or 33 in j): #or 4 in j or 5 in j or 6 in j): # not doing the death ones currently
            postprob_dict[31] = 0
            postprob_dict[32] = 0
            postprob_dict[33] = 0
        if not (34 in j or 35 in j or 36 in j): #or 4 in j or 5 in j or 6 in j): # not doing the death ones currently
            postprob_dict[34] = 0
            postprob_dict[35] = 0
            postprob_dict[36] = 0
        print('returning posterior probability dict, this does not include model topology probabilities')
        return postprob_dict, priordict

def get_structure_postprobs(df,add_to_dict=False,priordict={},rel_likelihood=False,by_initiating_sub=None,which_evidence='INS_Z'):
    #priordict default empty dict, could be that or None
    if not (type(priordict) is dict or priordict==None):
        print('priordict passed as incorrect variable, priordict will now be None')
        priordict = None
    try:
        if not which_evidence in ['Z','INS_Z','BIC_marglik_est']:
            print('which_evidence passed as incorrect variable, \'which_evidence will\' default to INS_Z')
            which_evidence='INS_Z'
    except AttributeError:
        print('which_evidence passed as incorrect variable, \'which_evidence\' will default to INS_Z')
        which_evidence = 'INS_Z'
        pass
    if by_initiating_sub:
        if type(by_initiating_sub) is tuple:
            # for instance if by_initiating_sub = ('1000', '1200', '1300', '1400', '1230', '1240', '1340', '1234')
            #   -> indicates any initiating condition where A is an initiating subtype
            # would also need this one if you want to say, "any initiating condition where A or N are initiating subtypes"
            #   -> would be by_inititiating_sub = ('1000','1200','1300','1400','1230','1240','1340','1234',
            #                                      '1200','1230','1240','1234','2000','2300','2400','2340')
            # or, if you want to say, "only the initiating condition with A alone", would be (1000)
            df = df.loc[df.model_starting_subtype_makeup_code.str.endswith(by_initiating_sub)]
        if type(by_initiating_sub) is int:
            # for instance if by_initiating_sub = 1, indicates any initiating condition where A is an initiating subtype
            #  using an int like this you can only filter by "includes this initiating subtype +/- others",
            #  could never specify "starts with A only" or "starts with A *or* N" (see above)
            df = df[df['subtype_starting_and_makeup_code'].str.contains('\...'+str(by_initiating_sub))]
        else:
            print('by_initiating_subtype '+str(by_initiating_sub)+' not recognized, cannot filter by this')
            print('returning None')
            return None
    if rel_likelihood:
        df = df.loc[df[which_evidence] > (np.max(df[which_evidence]) / 10 ** .5)]
    isstruct0 = len(df[df['subtype_starting_and_makeup_code'].str.startswith('0')])
    isstruct1 = len(df[df['subtype_starting_and_makeup_code'].str.startswith('1.')])
    isstruct2 = len(df[df['subtype_starting_and_makeup_code'].str.startswith('2')])
    isstruct3 = len(df[df['subtype_starting_and_makeup_code'].str.startswith('3')])
    isstruct4 = len(df[df['subtype_starting_and_makeup_code'].str.startswith('4')])
    isstruct5 = len(df[df['subtype_starting_and_makeup_code'].str.startswith('5')])
    isstruct6 = len(df[df['subtype_starting_and_makeup_code'].str.startswith('6')])
    isstruct7 = len(df[df['subtype_starting_and_makeup_code'].str.startswith('7')])
    isstruct8 = len(df[df['subtype_starting_and_makeup_code'].str.startswith('8')])
    isstruct9 = len(df[df['subtype_starting_and_makeup_code'].str.startswith('9')])
    isstruct10 = len(df[df['subtype_starting_and_makeup_code'].str.startswith('10')])
    #
    ## structure comparisons
    try:
        prior0 = (1/11)/isstruct0
    except ZeroDivisionError:
        prior0 = 0
    try:
        prior1 = (1/11)/isstruct1
    except ZeroDivisionError:
        prior1 = 0
    try:
        prior2 = (1/11)/isstruct2
    except ZeroDivisionError:
        prior2 = 0
    try:
        prior3 = (1/11)/isstruct3
    except ZeroDivisionError:
        prior3 = 0
    try:
        prior4 = (1/11)/isstruct4
    except ZeroDivisionError:
        prior4 = 0
    try:
        prior5 = (1/11)/isstruct5
    except ZeroDivisionError:
        prior5 = 0
    try:
        prior6 = (1/11)/isstruct6
    except ZeroDivisionError:
        prior6 = 0
    try:
        prior7 = (1/11)/isstruct7
    except ZeroDivisionError:
        prior7 = 0
    try:
        prior8 = (1/11)/isstruct8
    except ZeroDivisionError:
        prior8 = 0
    try:
        prior9 = (1/11)/isstruct9
    except ZeroDivisionError:
        prior9 = 0
    try:
        prior10 = (1/11)/isstruct10
    except ZeroDivisionError:
        prior10 = 0
    #
    if priordict is not None:
        priordict['prior0'] = prior0
        priordict['prior1'] = prior1
        priordict['prior2'] = prior2
        priordict['prior3'] = prior3
        priordict['prior4'] = prior4
        priordict['prior5'] = prior5
        priordict['prior6'] = prior6
        priordict['prior7'] = prior7
        priordict['prior8'] = prior8
        priordict['prior9'] = prior9
        priordict['prior10'] = prior10
    priorstructs = []
    for i in df.index:
        if df.loc[i]['subtype_starting_and_makeup_code'].startswith('0'):
            priorstructs.append(prior0)
        elif df.loc[i]['subtype_starting_and_makeup_code'].startswith('1.'):
            priorstructs.append(prior1)
        elif df.loc[i]['subtype_starting_and_makeup_code'].startswith('2'):
            priorstructs.append(prior2)
        elif df.loc[i]['subtype_starting_and_makeup_code'].startswith('3'):
           priorstructs.append(prior3)
        elif df.loc[i]['subtype_starting_and_makeup_code'].startswith('4'):
            priorstructs.append(prior4)
        elif df.loc[i]['subtype_starting_and_makeup_code'].startswith('5'):
            priorstructs.append(prior5)
        elif df.loc[i]['subtype_starting_and_makeup_code'].startswith('6'):
            priorstructs.append(prior6)
        elif df.loc[i]['subtype_starting_and_makeup_code'].startswith('7'):
            priorstructs.append(prior7)
        elif df.loc[i]['subtype_starting_and_makeup_code'].startswith('8'):
            priorstructs.append(prior8)
        elif df.loc[i]['subtype_starting_and_makeup_code'].startswith('9'):
            priorstructs.append(prior9)
        elif df.loc[i]['subtype_starting_and_makeup_code'].startswith('10'):
            priorstructs.append(prior10)
        else:
            print('issue, model '+str(i))
    #
    df['priorstructs_'+which_evidence] = priorstructs
    #
    structpostlist = df[which_evidence]*df['priorstructs_'+which_evidence] / (np.sum(df[which_evidence]*df['priorstructs_'+which_evidence]))
    df['structspost_'+which_evidence] = structpostlist
    #
    np.sum(structpostlist)
    #
    struct0_sum = np.sum(df[df['subtype_starting_and_makeup_code'].str.startswith('0')]['structspost_'+which_evidence])
    struct1_sum = np.sum(df[df['subtype_starting_and_makeup_code'].str.startswith('1.')]['structspost_'+which_evidence])
    struct2_sum = np.sum(df[df['subtype_starting_and_makeup_code'].str.startswith('2')]['structspost_'+which_evidence])
    struct3_sum = np.sum(df[df['subtype_starting_and_makeup_code'].str.startswith('3')]['structspost_'+which_evidence])
    struct4_sum = np.sum(df[df['subtype_starting_and_makeup_code'].str.startswith('4')]['structspost_'+which_evidence])
    struct5_sum = np.sum(df[df['subtype_starting_and_makeup_code'].str.startswith('5')]['structspost_'+which_evidence])
    struct6_sum = np.sum(df[df['subtype_starting_and_makeup_code'].str.startswith('6')]['structspost_'+which_evidence])
    struct7_sum = np.sum(df[df['subtype_starting_and_makeup_code'].str.startswith('7')]['structspost_'+which_evidence])
    struct8_sum = np.sum(df[df['subtype_starting_and_makeup_code'].str.startswith('8')]['structspost_'+which_evidence])
    struct9_sum = np.sum(df[df['subtype_starting_and_makeup_code'].str.startswith('9')]['structspost_'+which_evidence])
    struct10_sum = np.sum(df[df['subtype_starting_and_makeup_code'].str.startswith('10')]['structspost_'+which_evidence])
    #
    if not add_to_dict:
        print('topology with A, N, A2, Y (structure 0) posterior probability: '+str(struct0_sum))
        print('topology with A, N, Y (structure 1) posterior probability: '+str(struct1_sum))
        print('topology with A, A2, Y (structure 2) posterior probability: '+str(struct2_sum))
        print('topology with N, A2, Y (structure 3) posterior probability: '+str(struct3_sum))
        print('topology with A, N, A2 (structure 4) posterior probability: '+str(struct4_sum))
        print('topology with A, N (structure 5) posterior probability: '+str(struct5_sum))
        print('topology with A, A2 (structure 6) posterior probability: '+str(struct6_sum))
        print('topology with A, Y (structure 7) posterior probability: '+str(struct7_sum))
        print('topology with N, A2 (structure 8) posterior probability: '+str(struct8_sum))
        print('topology with N, Y (structure 9) posterior probability: '+str(struct9_sum))
        print('topology with A2, Y (structure 10) posterior probability: '+str(struct10_sum))
    else:
        structprobs = {
            0:struct0_sum,1:struct1_sum,2:struct2_sum,3:struct3_sum,4:struct4_sum,5:struct5_sum,6:struct6_sum,7:struct7_sum,
                  8:struct8_sum,9:struct9_sum,10:struct10_sum
        }
        return structprobs, priordict


