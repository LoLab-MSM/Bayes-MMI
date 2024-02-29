import pandas as pd
import numpy as np

in_and_outdir = '../files_generated_in_MMI_sclc/'

dfdict = pd.read_pickle('../helper_functions_and_files/all_5891_models_in_dataframe_with_subtype_starting_makeup_code.pickle')

for dset in ['TKO','RPM','clA']:
    df = pd.read_pickle(in_and_outdir+'results_fromNS_gathered_'+dset+'.pickle')
    df['INS_Z'] = np.exp(df.INS_log_Z)
    df['posterior_prob'] = df.INS_Z/np.sum(df.INS_Z)
    df = pd.concat([df, dfdict.loc[df.index]], axis=1)
    df.to_pickle(in_and_outdir+'results_fromNS_gathered_'+dset+'_addlanalyses.pickle')


