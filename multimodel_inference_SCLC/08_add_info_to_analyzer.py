import pandas as pd
import numpy as np

in_and_outdir = '../files_generated_in_MMI_sclc/'
in_and_outdir = 'analyzed_pickles/'

dfdict = pd.read_pickle('../helper_functions_and_files/updatedinjune_all_9327_models_in_dataframe_with_subtype_starting_makeup_code.pickle')
updated_modelmakeups = np.load('../helper_functions_and_files/updatedinjune_apr_11_all_model_makeups_from_redo_ignoring_uneven_bidirtxns.npy')
upd_modnums = []
for j in dfdict.index:
    if dfdict.loc[j]['model_makeup'] in updated_modelmakeups:
        upd_modnums.append(j)

for dset in ['TKO','RPM','clA']:
    df = pd.read_pickle(in_and_outdir+'compare_'+dset+'_gleipnir_results_subset_betafit_to9264_somemissing_4_7_2022.pickle')
    df['INS_Z'] = np.exp(df.INS_log_Z)
    df['posterior_prob'] = df.INS_Z/np.sum(df.INS_Z)
    df = pd.concat([df, dfdict.loc[df.index]], axis=1)
    df.to_pickle(in_and_outdir+'compare_'+dset+'_gleipnir_results_subset_betafit_to9264_somemissing_4_7_2022_addlanalyses.pickle')

