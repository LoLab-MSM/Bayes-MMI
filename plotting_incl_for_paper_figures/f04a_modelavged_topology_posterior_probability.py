import pandas as pd
import numpy as np
import copy
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
import seaborn as sns
import sys

# add this Bayes-MMI directory to the path to be able to import from helper_functions_and_files
sys.path.append('/home/beiksp/Bayes-MMI')

from helper_functions_and_files.posterior_probability_calculations import \
    get_structure_postprobs

indir = '../files_generated_in_MMI_sclc/'

dfdict = pd.read_pickle('../helper_functions_and_files/updatedinjune_all_9327_models_in_dataframe_with_subtype_starting_makeup_code.pickle')
updated_modelmakeups = np.load('../helper_functions_and_files/updatedinjune_apr_11_all_model_makeups_from_redo_ignoring_uneven_bidirtxns.npy')
upd_modnums = []
for j in dfdict.index:
    if dfdict.loc[j]['model_makeup'] in updated_modelmakeups:
        upd_modnums.append(j)

topo_modelavg_post = {}
for dset in ['TKO','RPM','clA']:
    df = pd.read_pickle(indir+'/results_fromNS_gathered_'+dset+'_somemissing_addlanalyses.pickle')
    df = df.loc[df.index.isin(upd_modnums)]
    # Fig 4A (the following line plus everything after this for loop
    topo_modelavg_post[dset], pri = get_structure_postprobs(df,add_to_dict=True,by_initiating_sub=1) #not using pri
    # run this instead for the plot without initating subtype filter
    # Fig S5A
    #topo_modelavg_post[dset], pri = get_structure_postprobs(df,add_to_dict=True)

tko = pd.DataFrame(topo_modelavg_post['TKO'], index=[0])
tko['dataset'] = 'TKO'
rpm = pd.DataFrame(topo_modelavg_post['RPM'], index=[0])
rpm['dataset'] = 'RPM'
cla = pd.DataFrame(topo_modelavg_post['clA'], index=[0])
cla['dataset'] = 'SCLC-A cell lines'

bardf = pd.concat([tko,rpm,cla])
bardf = pd.melt(bardf,id_vars=['dataset'])

sns.set_style('whitegrid') #old
plt.rcParams.update({'font.size': 16})

g = sns.catplot(
    data=bardf, kind='bar',
    x='value', y='variable', orient='h',
    hue='dataset', ci='sd',
    palette='dark', alpha=0.6,
    height=12,
    aspect=0.25)
g._legend.set_title("") #old
g.despine(left=True)
g.set_axis_labels("Posterior Probability","Structure")
g._legend._set_loc(1)
plt.xlim(0,1)
plt.tight_layout()
plt.savefig('../generated_figures/structure_probabilities_bw_datasets_barplot.pdf',format='pdf')
plt.show()
