import pandas as pd
import numpy as np

# how to generate updatedinjune_all_9327_models_in_dataframe_with_subtype_starting_makeup_code.pickle
mm_list = list(np.load('all_models_createdthroughout_forhypbuilder_upto_9327.npy'))

# but if you give a different set of model makeups, this will calculate the codes for that too
#mm_list = list(np.load('../datafiles_generated_in_MMI_sclc/all_filtered_topologies_models_for_hypbuilder.npy')) #the output of 01_make_model_list_for_Hypbuilder.py

df = pd.DataFrame({'model_makeup':mm_list})

df_start_and_subtype_makeup_code = []
for i in df.index:
    x = [int(j) for j in df.loc[i]['model_makeup'].split(',')]
    code = 0
    if 48 in x and not (45 in x or 46 in x or 47 in x):  # starts A only
        code = 0.001000
    elif 48 in x and 45 in x and not (46 in x or 47 in x):  # starts A,N
        code = 0.001200
    elif 48 in x and 46 in x and not (45 in x or 47 in x):  # starts A,A2
        code = 0.001300
    elif 48 in x and 47 in x and not (45 in x or 46 in x):  # starts A,Y
        code = 0.001400
    elif 48 in x and 45 in x and 46 in x and not 47 in x:  # starts A,N,A2
        code = 0.001230
    elif 48 in x and 45 in x and 47 in x and not 46 in x:  # starts A,N,Y
        code = 0.001240
    elif 48 in x and 46 in x and 47 in x and not 45 in x:  # starts A,A2,Y
        code = 0.001340
    elif 48 in x and 46 in x and 47 in x and 45 in x:  # starts all four
        code = 0.001234
    elif 45 in x and not (46 in x or 47 in x or 48 in x):  # starts N only
        code = 0.002000
    elif 45 in x and 46 in x and not (47 in x or 48 in x):  # starts N,A2
        code = 0.002300
    elif 45 in x and 47 in x and not (46 in x or 48 in x):  # starts N,Y
        code = 0.002400
    elif 45 in x and 46 in x and 47 in x and not 48 in x:  # starts N,A2,Y
        code = 0.002340
    elif 46 in x and not (45 in x or 47 in x or 48 in x):  # starts A2 only
        code = 0.003000
    elif 46 in x and 47 in x and not (45 in x or 48 in x):  # starts A2,Y
        code = 0.003400
    elif 47 in x and not (45 in x or 46 in x or 48 in x):  # starts Y only
        code = 0.004000
    if ((1 in x or 2 in x or 3 in x) and (7 in x or 8 in x or 9 in x) and (13 in x or 14 in x or 15 in x) and (19 in x or 20 in x or 21 in x)): #all four
        if 1 in x: #Y effector
            code += 0.1
            if 25 in x or 31 in x or 28 in x or 34 in x:
                code += 0.01
            # else: #not adding that zero, that is, it's there on its own
        elif 2 in x: #A2&Y effectors
            code += 0.2
            if 26 in x or 32 in x or 29 in x or 35 in x:
                code += 0.02
            #else: #not adding that zero, that is, it's there on its own
        elif 3 in x: #no effectors
            if 25 in x or 31 in x or 28 in x or 34 in x:
                code += 0.01
            elif 26 in x or 32 in x or 29 in x or 35 in x:
                code += 0.02
            #else: #not adding anything
        else:
            print ('something went wrong '+df.loc[i]['model_makeup'])
    elif ((1 in x or 2 in x or 3 in x) and (7 in x or 8 in x or 9 in x) and (19 in x or 20 in x or 21 in x) and not (13 in x or 14 in x or 15 in x)): #A,N,Y
        # i guess this would never have any of the 2-8-20's, but whatever
        code += 1.0
        if 1 in x:
            code += 0.1
            if 28 in x or 34 in x:
                code += 0.01
            #else:
        elif 3 in x:
            if 28 in x or 34 in x:
                code += 0.01
            #else:
        else:
            print('something went wrong ' + df.loc[i]['model_makeup'])
    elif ((1 in x or 2 in x or 3 in x) and (13 in x or 14 in x or 15 in x) and (19 in x or 20 in x or 21 in x) and not (7 in x or 8 in x or 9 in x)): #A,A2,Y
        code += 2.0
        if 1 in x:
            code += 0.1
            if 25 in x or 31 in x:
                code += 0.01
            #else:
        elif 2 in x:
            if 26 in x or 32 in x:
                code += 0.2
            #else:
        elif 3 in x:
            if 25 in x or 31 in x:
                code += 0.01
            elif 26 in x or 32 in x:
                code += 0.02
            #else:
        else:
            print ('something went wrong '+df.loc[i]['model_makeup'])
    elif ((7 in x or 8 in x or 9 in x) and (13 in x or 14 in x or 15 in x) and (19 in x or 20 in x or 21 in x) and not (1 in x or 2 in x or 3 in x)): #N,A2,Y
        code += 3.0
        if 7 in x:
            code += 0.1
            if 25 in x or 31 in x or 28 in x or 34 in x:
                code += 0.01
            #else:
        elif 8 in x:
            code += 0.2
            if 26 in x or 32 in x or 29 in x or 35 in x:
                code += 0.02
            #else:
        elif 9 in x:
            if 25 in x or 31 in x or 28 in x or 34 in x:
                code += 0.01
            elif 26 in x or 32 in x or 29 in x or 35 in x:
                code += 0.02
            #else:
        else:
            print ('something went wrong '+df.loc[i]['model_makeup'])
    elif ((1 in x or 2 in x or 3 in x) and (7 in x or 8 in x or 9 in x) and (13 in x or 14 in x or 15 in x) and not (19 in x or 20 in x or 21 in x)): #A,N,A2
        # there'd never be 1-7-13's in here...
        code += 4.0
        if 2 in x:
            code += 0.2
            if 26 in x or 32 in x or 29 in x or 35 in x:
                code += 0.02
            #else:
        elif 3 in x:
            if 26 in x or 32 in x or 29 in x or 35 in x:
                code += 0.02
            #else:
        else:
            print ('something went wrong '+df.loc[i]['model_makeup'])
    elif ((1 in x or 2 in x or 3 in x) and (7 in x or 8 in x or 9 in x) and not (13 in x or 14 in x or 15 in x) and not (19 in x or 20 in x or 21 in x)): #A,N
        code += 5.0
        if not 3 in x: #don't really need the if statement but would be good to check things aren't going wrong with the else statement
        #else: #removed this and changed the if statement to have a 'not'
            print ('something went wrong '+df.loc[i]['model_makeup'])
    elif ((1 in x or 2 in x or 3 in x) and (13 in x or 14 in x or 15 in x) and not (7 in x or 8 in x or 9 in x) and not (19 in x or 20 in x or 21 in x)): #A,A2
        # no 1s...
        code += 6.0
        if 2 in x:
            code += 0.2
            if 26 in x or 32 in x:
                code += 0.02
            #else:
        elif 3 in x:
            if 26 in x or 32 in x:
                code += 0.02
            #else:
        else:
            print ('something went wrong '+df.loc[i]['model_makeup'])
    elif ((1 in x or 2 in x or 3 in x) and (19 in x or 20 in x or 21 in x) and not (13 in x or 14 in x or 15 in x) and not (7 in x or 8 in x or 9 in x)): #A,Y
        # no 2s...
        code += 7.0
        if 1 in x:
            code += 0.1
            if 25 in x or 31 in x:
                code += 0.01
            #else:
        elif 3 in x:
            if 25 in x or 31 in x:
                code += 0.01
            #else:
        else:
            print ('something went wrong '+df.loc[i]['model_makeup'])
    elif ((7 in x or 8 in x or 9 in x) and (13 in x or 14 in x or 15 in x) and not (1 in x or 2 in x or 3 in x) and not (19 in x or 20 in x or 21 in x)): #N,A2
        #shouldn't have 7s...
        code += 8.0
        if 8 in x:
            code += 0.2
            if 26 in x or 32 in x:
                code += 0.02
            #else:
        elif 9 in x:
            if 26 in x or 32 in x:
                code += 0.02
            #else:
        else:
            print ('something went wrong '+df.loc[i]['model_makeup'])
    elif ((7 in x or 8 in x or 9 in x) and (19 in x or 20 in x or 21 in x) and not (13 in x or 14 in x or 15 in x) and not (1 in x or 2 in x or 3 in x)): #N,Y
        #shouldn't have 8's...
        code += 9.0
        if 7 in x:
            code += 0.1
            if 28 in x or 34 in x:
                code += 0.01
            #else:
        elif 9 in x:
            if 28 in x or 34 in x:
                code += 0.01
            #else:
        else:
            print ('something went wrong '+df.loc[i]['model_makeup'])
    elif ((13 in x or 14 in x or 15 in x) and (19 in x or 20 in x or 21 in x) and not (7 in x or 8 in x or 9 in x) and not (1 in x or 2 in x or 3 in x)): #A2,Y
        # can't have 14's... assuming if A2&Y are both effectors, if they both affect each other it's like they both don't affect each other, so didn't include models like that
        code += 10.0
        if 13 in x:
            code += 0.1
            if 25 in x or 31 in x:
                code += 0.01
            #else:
        elif 15 in x:
            if 25 in x or 31 in x:
                code += 0.01
            #else:
        else:
            print ('something went wrong '+df.loc[i]['model_makeup'])
    else:
        print ('some sort of problem '+df.loc[i]['model_makeup'])
    #subtype_and_starting_makeup_importance[format(code, '.6f')] += df.loc[i]['posterior_prob']
    df_start_and_subtype_makeup_code.append(format(code, '.6f'))

df['subtype_starting_and_makeup_code'] = df_start_and_subtype_makeup_code

#df.to_pickle('updatedinjune_all_9327_models_in_dataframe_with_subtype_starting_makeup_code.pickle')

# or if you used the mm_list from the commmented out code at the top...
#df.to_pickle('all_5891_models_in_dataframe_with_subtype_starting_makeup_code.pickle')
