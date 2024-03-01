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
    get_structure_postprobs, get_postprobs_allbutstructure

indir = '../files_generated_in_MMI_sclc/'
outdir = '../generated_figures/'

## Fig 5A and Fig S6A

topo_modelavg_post = {}
for dset in ['TKO','RPM','clA']:
    df = pd.read_pickle(indir+'/results_fromNS_gathered_'+dset+'_addlanalyses.pickle')
    ## Fig 5A (the following line plus everything after this for loop
    topo_modelavg_post[dset], pri = get_structure_postprobs(df,add_to_dict=True,by_initiating_sub=1) #not using pri
    # run the below instead for the plot without initiating subtype filter
    ## Fig S6A
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
plt.savefig(outdir+'structure_probabilities_bw_datasets_barplot.pdf',format='pdf')
plt.show()

## Fig S5

initdict = {
     'starts_with_A':'A',
     'starts_with_A2':'A2',
     'starts_with_A2Y':'A2 & Y',
     'starts_with_AA2':'A & A2',
     'starts_with_AA2Y':'A, A2 & Y',
     'starts_with_AN':'A & N',
     'starts_with_ANA2':'A, N & A2',
     'starts_with_ANA2Y':'A, N, A2 & Y',
     'starts_with_ANY':'A, N & Y',
     'starts_with_AY':'A & Y',
     'starts_with_N':'N',
     'starts_with_NA2':'N & A2',
     'starts_with_NA2Y':'N, A2 & Y',
     'starts_with_NY':'N & Y',
     'starts_with_Y':'Y'
}

initiation_modelavg_post = {}
for dset in ['TKO','RPM','clA']:
    df = pd.read_pickle(indir+'/results_fromNS_gathered_'+dset+'_addlanalyses.pickle')
    post_prob, pri = get_postprobs_allbutstructure(df, add_to_dict=True)
    # individual priors for starting subtypes in pri but don't need to use because model-averaging them they all sum to 1/15
    initiation_modelavg_post[dset] = {k: post_prob[k] for k in post_prob if isinstance(k, str) and k.startswith('starts')}

tko = pd.DataFrame({initdict[k]: initiation_modelavg_post['TKO'][k] for k in initiation_modelavg_post['TKO']}, index=[0])
tko['dataset'] = 'TKO'
rpm = pd.DataFrame({initdict[k]: initiation_modelavg_post['RPM'][k] for k in initiation_modelavg_post['RPM']}, index=[0])
rpm['dataset'] = 'RPM'
cla = pd.DataFrame({initdict[k]: initiation_modelavg_post['clA'][k] for k in initiation_modelavg_post['clA']}, index=[0])
cla['dataset'] = 'SCLC-A cell lines'

bardf = pd.concat([tko,rpm,cla])
bardf = pd.melt(bardf,id_vars=['dataset'])

sns.set_style('whitegrid') #old
plt.rcParams.update({'font.size': 16})

g = sns.catplot(
    data=bardf, kind='bar',
    x='variable', y='value', orient='v',
    hue='dataset', ci='sd',
    palette='dark', alpha=0.6,
    height=6,
    aspect=2)
g._legend.set_title("") #old
g.despine(left=True)
g.set_axis_labels("Initiating subtype(s)","Posterior Probability")
g._legend._set_loc(1)
ax = g.axes[0][0]
ax.axhline((1/len(set(bardf.variable))),ls='--',color='black',linewidth=2)
ax.tick_params(axis='x',rotation=60)
plt.ylim(0,0.25)
plt.tight_layout()
plt.savefig(outdir+'initiation_probabilities_bw_datasets_wprior_barplot.pdf',format='pdf')
plt.show()
