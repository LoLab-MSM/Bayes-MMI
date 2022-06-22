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
    get_postprobs_allbutstructure, hypo_to_num, num_to_hypo

from posterior_prob_networkgraph_plotting import make_plots_for_datasets_in_a_row

#indir = '../files_generated_in_MMI_sclc/'
indir = '../analyzed_pickles/'

dfdict = pd.read_pickle('../helper_functions_and_files/updatedinjune_all_9327_models_in_dataframe_with_subtype_starting_makeup_code.pickle')

updated_modelmakeups = np.load('../helper_functions_and_files/updatedinjune_apr_11_all_model_makeups_from_redo_ignoring_uneven_bidirtxns.npy')
upd_modnums = []
for j in dfdict.index:
    if dfdict.loc[j]['model_makeup'] in updated_modelmakeups:
        upd_modnums.append(j)

# print(upd_modnums)

tdict = {}
for dset in ['TKO','RPM','clA']:
    df = pd.read_pickle(indir+'compare_'+dset+'_gleipnir_results_subset_betafit_to9264_somemissing_4_7_2022_addlanalyses.pickle')
    df = df.loc[df.index.isin(upd_modnums)]
    # 
    df_wA = copy.deepcopy(df[df['subtype_starting_and_makeup_code'].str.contains('\...1')])
    df_wN = copy.deepcopy(df[df['subtype_starting_and_makeup_code'].str.contains('\...2')])
    df_wA2 = copy.deepcopy(df[df['subtype_starting_and_makeup_code'].str.contains('\...3')])
    # for topologies filtered by earliest initiating subtype (A)
    for topo in ['0','1.','2','4','5','6','7']:
        tdict_key = dset+' data structure '+topo+' starts including A' if dset != 'clA' else ' SCLC-A cell lines data structure '+topo+' starts including A'
        df = df_wA[df_wA['subtype_starting_and_makeup_code'].str.startswith(topo)]
        post_prob, prior_prob = get_postprobs_allbutstructure(df, add_to_dict=True)
        tdict[tdict_key] = copy.deepcopy(post_prob)
    # for topologies filtered by earliest initiating subtype when they don't have A (earliest subtype = N)
    for topo in ['3','8','9']:
        tdict_key = dset + ' data structure ' + topo + ' starts including N' if dset != 'clA' else 'SCLC-A cell lines data structure ' + topo + ' starts including N'
        df = df_wN[df_wN['subtype_starting_and_makeup_code'].str.startswith(topo)]
        post_prob, prior_prob = get_postprobs_allbutstructure(df, add_to_dict=True)
        tdict[tdict_key] = copy.deepcopy(post_prob)
    # the one topology that doesn't have A or N is A2&Y, so filter by initiating with A2
    topo = '10'
    tdict_key = dset + ' data structure ' + topo + ' starts including A2' if dset != 'clA' else 'SCLC-A cell lines data structure ' + topo + ' starts including A2'
    df = df_wA2[df_wA2['subtype_starting_and_makeup_code'].str.startswith(topo)]
    post_prob, prior_prob = get_postprobs_allbutstructure(df, add_to_dict=True)
    tdict[tdict_key] = copy.deepcopy(post_prob)

tdf = pd.DataFrame(tdict)

colors = ["mediumblue", "cornflowerblue", "white", "lightcoral", "firebrick"]
cmap1 = LinearSegmentedColormap.from_list("mycmap1", list(zip([0,0.25,0.5,0.75,1],colors)))
cmap2 = LinearSegmentedColormap.from_list("mycmap2", list(zip([0,(0.33/2),0.33,(.33+(1-.33)/2),1],colors)))

# x will be for evaluations looking not only at 'is there an effect from Non-NE' but for each effect,
#  which Non-NE subtype or group is likely to be causing it
x = copy.deepcopy(tdf)

# z will be for evaluations looking at 'is there an effect from Non-NE at all', which is what's shown in the paper
z = copy.deepcopy(tdf)

# start with z because that's what plotted in the paper

# now need to change z such that it's not the individual effects but any at all
for i in z:
    for hypo in ['div_', 'diff_firsthalf_', 'diff_lasthalf_']:
        added_toY = False
        for j in [x for x in hypo_to_num[hypo + 'Yeff'] if z[i].loc[x] > 0]:
            added_toY = True
            z[i].loc[j] = z[i].loc[hypo + 'any']
        if added_toY:
            for j in [x for x in hypo_to_num[hypo + 'A2Yeff'] if z[i].loc[x] > 0]:
                z[i].loc[j] = 0
        else:
            for j in [x for x in hypo_to_num[hypo + 'A2Yeff'] if z[i].loc[x] > 0]:
                z[i].loc[j] = z[i].loc[hypo + 'any']

# for the network graph plotting view

# Figure 5B-D
arrowcolormap = {'cmap_diff':cmap1,
                 'cmap_eff':cmap1}

z_graph = z.drop([x for x in z.index if type(x) is str])

throughdict = {x:z_graph[x].to_dict() for x in z}
make_plots_for_datasets_in_a_row(throughdict,colormap=arrowcolormap,savedir='../generated_figures')

# for the heatmap plotting view

droplist = []
for i in z.index:
    if np.all(z.loc[i]==0):
        droplist.append(i)

droplist.extend([3,9,15,21,27,30,33,36])
droplist.extend([y for k in [hypo_to_num[x] for x in hypo_to_num.keys() if 'eff' in x] for y in k if y in z.index])
# this doesn't work because z.index is a mix of strings and ints
#z.drop([y for y in z.index if 'starts' in y],inplace=True)

z.drop(droplist,inplace=True)

z.index = [num_to_hypo[y] if y in num_to_hypo else y for y in z.index]
# now that it's all strings, can drop with this list comprehension
z.drop([y for y in z.index if 'starts' in y],inplace=True)

# rename the hypotheses (rows / indices)
z.rename(index={'AtoN':'A to N','NtoA':'N to A','AtoA2':'A to A2','A2toA':'A2 to A',
                'NtoY':'N to Y','YtoN':'Y to N','A2toY':'A2 to Y','YtoA2':'Y to A2',
                'AtoY':'A to Y','YtoA':'Y to A','NtoA2':'N to A2','A2toN':'A2 to N'},inplace=True)
z.rename(index={'div_any':'Non-NE effect on division&death',
                'diff_firsthalf_any':'Non-NE effect on early tsn',
                'diff_lasthalf_any':'Non-NE effect on late tsn',
                'eff_Y_contrib':'Effects present, Y contributes',
                'eff_A2_Y_contrib':'Effects present, A2 & Y contribute'},inplace=True)

# easier to deal with
z.rename(columns={
       'TKO data structure 0 starts including A':'TKO 4 subtypes',
       'TKO data structure 1. starts including A':'TKO 3 subtypes (A,N,Y)',
       'TKO data structure 2 starts including A':'TKO 3 subtypes (A,A2,Y)',
       'TKO data structure 3 starts including N':'TKO 3 subtypes (N,A2,Y)',
       'TKO data structure 4 starts including A':'TKO 3 subtypes (A,N,A2)',
       'TKO data structure 5 starts including A':'TKO 3 subtypes (A,N)',
       'TKO data structure 6 starts including A':'TKO 3 subtypes (A,A2)',
       'TKO data structure 7 starts including A':'TKO 3 subtypes (A,Y)',
       'TKO data structure 8 starts including N':'TKO 3 subtypes (N,A2)',
       'TKO data structure 9 starts including N':'TKO 3 subtypes (N,Y)',
       'TKO data structure 10 starts including A2':'TKO 3 subtypes (A2,Y)',
       'RPM data structure 0 starts including A':'RPM 4 subtypes',
       'RPM data structure 1. starts including A':'RPM 3 subtypes (A,N,Y)',
       'RPM data structure 2 starts including A':'RPM 3 subtypes (A,A2,Y)',
       'RPM data structure 3 starts including N':'RPM 3 subtypes (N,A2,Y)',
       'RPM data structure 4 starts including A':'RPM 3 subtypes (A,N,A2)',
       'RPM data structure 5 starts including A':'RPM 3 subtypes (A,N)',
       'RPM data structure 6 starts including A':'RPM 3 subtypes (A,A2)',
       'RPM data structure 7 starts including A':'RPM 3 subtypes (A,Y)',
       'RPM data structure 8 starts including N':'RPM 3 subtypes (N,A2)',
       'RPM data structure 9 starts including N':'RPM 3 subtypes (N,Y)',
       'RPM data structure 10 starts including A2':'RPM 3 subtypes (A2,Y)',
       'SCLC-A cell lines data structure 0 starts including A':'SCLC-A cells 4 subtypes',
       'SCLC-A cell lines data structure 1. starts including A':'SCLC-A cells 3 subtypes (A,N,Y)',
       'SCLC-A cell lines data structure 2 starts including A':'SCLC-A cells 3 subtypes (A,A2,Y)',
       'SCLC-A cell lines data structure 3 starts including N':'SCLC-A cells 3 subtypes (N,A2,Y)',
       'SCLC-A cell lines data structure 4 starts including A':'SCLC-A cells 3 subtypes (A,N,A2)',
       'SCLC-A cell lines data structure 5 starts including A':'SCLC-A cells 3 subtypes (A,N)',
       'SCLC-A cell lines data structure 6 starts including A':'SCLC-A cells 3 subtypes (A,A2)',
       'SCLC-A cell lines data structure 7 starts including A':'SCLC-A cells 3 subtypes (A,Y)',
       'SCLC-A cell lines data structure 8 starts including N':'SCLC-A cells 3 subtypes (N,A2)',
       'SCLC-A cell lines data structure 9 starts including N':'SCLC-A cells 3 subtypes (N,Y)',
       'SCLC-A cell lines data structure 10 starts including A2':'SCLC-A cells 3 subtypes (A2,Y)'
                 },inplace=True)

# historically sent the forward transitions as 1-[transition] to the plotting script so fix it here
z.loc['A to N'] = 1-z.loc['A to N']
z.loc['N to Y'] = 1-z.loc['N to Y']
z.loc['A to A2'] = 1-z.loc['A to A2']
z.loc['A2 to Y'] = 1-z.loc['A2 to Y']
# replacing zeros with NaNs more accurately shows that a zero indicates it wasn't assessed in this topology
#  (if it was a probability close to zero, it would be a very small number, but not zero)
z.replace({0:np.nan},inplace=True)

zheat = z.T

# the whole figure
fig, (row1,row2) = plt.subplots(ncols=1,nrows=2,figsize=(14,8),gridspec_kw={'height_ratios':[1,20]})
ax = row2
sns.heatmap(zheat, cmap=cmap1, ax=ax,cbar=False,vmin=0, vmax=1)#, center=0.5, ax=ax, cbar=False) #cmap1 instead of "vlag"
cbar1 = fig.colorbar(ax.collections[0], cax=row1, orientation="horizontal")#,pad=0.1)#location="top", use_gridspec=False, pad=0.1)
cbar1.ax.set_title('Posterior probability',fontsize=16)
row1.xaxis.set_ticks_position('top')
cbar1.set_ticks([0,.5,1])
cbar1.ax.set_xticklabels([0,.5,1],fontsize=16)
ax.tick_params(axis='y',rotation=0)
ax.tick_params(axis='x',rotation=30)
plt.setp(ax.xaxis.get_majorticklabels(), ha='right')
fig.subplots_adjust(bottom=0.38,top=0.9,left=0.33,right=0.95)
plt.savefig('../generated_figures/alltopologies_heatmap.pdf',format='pdf')
plt.show()

# just the top 3 topologies
# Figure 5A
zheat = zheat.loc[['TKO 3 subtypes (A,A2,Y)','RPM 3 subtypes (A,N,Y)','SCLC-A cells 3 subtypes (A,N,A2)']]

fig, (row1,row2) = plt.subplots(ncols=1,nrows=2,figsize=(14,8),gridspec_kw={'height_ratios':[1,20]})
ax = row2
sns.heatmap(zheat, cmap=cmap1, ax=ax,cbar=False,vmin=0, vmax=1)#, center=0.5, ax=ax, cbar=False) #cmap1 instead of "vlag"
cbar1 = fig.colorbar(ax.collections[0], cax=row1, orientation="horizontal")#,pad=0.1)#location="top", use_gridspec=False, pad=0.1)
cbar1.ax.set_title('Posterior probability',fontsize=16)
row1.xaxis.set_ticks_position('top')
cbar1.set_ticks([0,.5,1])
cbar1.ax.set_xticklabels([0,.5,1],fontsize=16)
ax.tick_params(axis='y',rotation=0)
ax.tick_params(axis='x',rotation=30)
plt.setp(ax.xaxis.get_majorticklabels(), ha='right')
fig.subplots_adjust(bottom=0.38,top=0.9,left=0.33,right=0.95)
plt.savefig('../generated_figures/top3topology_heatmap.pdf',format='pdf')
plt.show()

#####
# No more figures in the paper (or supplement) after this, only example code for
#  differentiating between effects from Y and effects from A2 & Y
##

# x was generated above for this purpose (line 61)
#x = copy.deepcopy(tdf)

x = x.drop([y for y in x.index if type(y) is str])

x.rename(columns={
       'TKO data structure 0 starts including A':'TKO 4 subtypes, Y vs A2&Y',
       'TKO data structure 1. starts including A':'TKO 3 subtypes (A,N,Y), Y vs A2&Y',
       'TKO data structure 2 starts including A':'TKO 3 subtypes (A,A2,Y), Y vs A2&Y',
       'TKO data structure 3 starts including N':'TKO 3 subtypes (N,A2,Y), Y vs A2&Y',
       'TKO data structure 4 starts including A':'TKO 3 subtypes (A,N,A2), Y vs A2&Y',
       'TKO data structure 5 starts including A':'TKO 3 subtypes (A,N), Y vs A2&Y',
       'TKO data structure 6 starts including A':'TKO 3 subtypes (A,A2), Y vs A2&Y',
       'TKO data structure 7 starts including A':'TKO 3 subtypes (A,Y), Y vs A2&Y',
       'TKO data structure 8 starts including N':'TKO 3 subtypes (N,A2), Y vs A2&Y',
       'TKO data structure 9 starts including N':'TKO 3 subtypes (N,Y), Y vs A2&Y',
       'TKO data structure 10 starts including A2':'TKO 3 subtypes (A2,Y), Y vs A2&Y',
       'RPM data structure 0 starts including A':'RPM 4 subtypes, Y vs A2&Y',
       'RPM data structure 1. starts including A':'RPM 3 subtypes (A,N,Y), Y vs A2&Y',
       'RPM data structure 2 starts including A':'RPM 3 subtypes (A,A2,Y), Y vs A2&Y',
       'RPM data structure 3 starts including N':'RPM 3 subtypes (N,A2,Y), Y vs A2&Y',
       'RPM data structure 4 starts including A':'RPM 3 subtypes (A,N,A2), Y vs A2&Y',
       'RPM data structure 5 starts including A':'RPM 3 subtypes (A,N), Y vs A2&Y',
       'RPM data structure 6 starts including A':'RPM 3 subtypes (A,A2), Y vs A2&Y',
       'RPM data structure 7 starts including A':'RPM 3 subtypes (A,Y), Y vs A2&Y',
       'RPM data structure 8 starts including N':'RPM 3 subtypes (N,A2), Y vs A2&Y',
       'RPM data structure 9 starts including N':'RPM 3 subtypes (N,Y), Y vs A2&Y',
       'RPM data structure 10 starts including A2':'RPM 3 subtypes (A2,Y), Y vs A2&Y',
       'SCLC-A cell lines data structure 0 starts including A':'SCLC-A cells 4 subtypes, Y vs A2&Y',
       'SCLC-A cell lines data structure 1. starts including A':'SCLC-A cells 3 subtypes (A,N,Y), Y vs A2&Y',
       'SCLC-A cell lines data structure 2 starts including A':'SCLC-A cells 3 subtypes (A,A2,Y), Y vs A2&Y',
       'SCLC-A cell lines data structure 3 starts including N':'SCLC-A cells 3 subtypes (N,A2,Y), Y vs A2&Y',
       'SCLC-A cell lines data structure 4 starts including A':'SCLC-A cells 3 subtypes (A,N,A2), Y vs A2&Y',
       'SCLC-A cell lines data structure 5 starts including A':'SCLC-A cells 3 subtypes (A,N), Y vs A2&Y',
       'SCLC-A cell lines data structure 6 starts including A':'SCLC-A cells 3 subtypes (A,A2), Y vs A2&Y',
       'SCLC-A cell lines data structure 7 starts including A':'SCLC-A cells 3 subtypes (A,Y), Y vs A2&Y',
       'SCLC-A cell lines data structure 8 starts including N':'SCLC-A cells 3 subtypes (N,A2), Y vs A2&Y',
       'SCLC-A cell lines data structure 9 starts including N':'SCLC-A cells 3 subtypes (N,Y), Y vs A2&Y',
       'SCLC-A cell lines data structure 10 starts including A2':'SCLC-A cells 3 subtypes (A2,Y), Y vs A2&Y'
                 },inplace=True)

# network graph plot

arrowcolormap = {'cmap_diff':cmap1,
                 'cmap_eff':cmap2}

throughdict = {y:x[y].to_dict() for y in x}
make_plots_for_datasets_in_a_row(throughdict,colormap=arrowcolormap,savedir='../generated_figures')

# heatmap plot

droplist = []
for i in x.index:
    if np.all(x.loc[i]==0):
        droplist.append(i)

droplist.extend([3,9,15,21,27,30,33,36])

x.drop(droplist,inplace=True)

# i want to give div_Yeff_A any values in any div_Yeff
for i in x:
    for hypo in ['div_', 'diff_firsthalf_', 'diff_lasthalf_']:
        x[i].loc[np.min([k for k in hypo_to_num[hypo + 'Yeff']])] = np.max(
            list(set(x[i].loc[[k for k in hypo_to_num[hypo + 'Yeff']]])))
        for j in sorted([k for k in hypo_to_num[hypo + 'Yeff']])[1:]:
            x[i].loc[j] = 0
        x[i].loc[np.min([k for k in hypo_to_num[hypo + 'A2Yeff']])] = np.max(
            list(set(x[i].loc[[k for k in hypo_to_num[hypo + 'A2Yeff']]])))
        for j in sorted([k for k in hypo_to_num[hypo + 'A2Yeff']])[1:]:
            x[i].loc[j] = 0

x.index = [num_to_hypo[y] for y in x.index]

droplist = []
for j in x.index:
    if 'div' in j and not j.endswith('_A'):
        droplist.append(j)
    if 'diff' in j and not ('_A_A2' in j or '_A2_Y' in j):  # has to be A2 and not Y ones because
                                                            # np.min([k for k in hypo_to_num[etc]]) refers to A2 transitions
        droplist.append(j)

x.drop(droplist,inplace=True)

# rename the hypotheses (rows / indices)
x.rename(index={'AtoN':'A to N','NtoA':'N to A','AtoA2':'A to A2','A2toA':'A2 to A',
                'NtoY':'N to Y','YtoN':'Y to N','A2toY':'A2 to Y','YtoA2':'Y to A2',
                'AtoY':'A to Y','YtoA':'Y to A','NtoA2':'N to A2','A2toN':'A2 to N'}, inplace=True)
x.rename(index={'div_Yeff_A':'Y effect on division',
                'div_A2Yeff_A':'A2 & Y effect on division',
                'diff_firsthalf_Yeff_A_A2':'Y effect on early tsn',
                'diff_firsthalf_A2Yeff_A_A2':'A2 & Y effect on early tsn',
                'diff_lasthalf_Yeff_A2_Y':'Y effect on late tsn',
                'diff_lasthalf_A2Yeff_A2_Y':'A2 & Y effect on late tsn'
                }, inplace=True)

# historically sent the forward transitions as 1-[transition] to the plotting script so fix it here
x.loc['A to N'] = 1-x.loc['A to N']
x.loc['N to Y'] = 1-x.loc['N to Y']
x.loc['A to A2'] = 1-x.loc['A to A2']
x.loc['A2 to Y'] = 1-x.loc['A2 to Y']
# replacing xeros with NaNs more accurately shows that a xero indicates it wasn't assessed in this topology
#  (if it was a probability close to xero, it would be a very small number, but not xero)
x.replace({0:np.nan},inplace=True)

# different prior distributions for Y effect vs A2&Y effect vs none
xdiff = x.T[[c for c in x.T.columns if 'to' in c]]
xeff = x.T[[c for c in x.T.columns if not 'to' in c]]

plt.rcParams.update({'font.size': 18})

## Full
fig, (row1,row2) = plt.subplots(ncols=2,nrows=2,figsize=(20,12),gridspec_kw={'width_ratios': [2, 1],'height_ratios':[1,20]})
ax = row2[0]
ax2 = row2[1]
sns.heatmap(xdiff, cmap=cmap1, ax=ax,cbar=False,vmin=0, vmax=1)#, center=0.5, ax=ax, cbar=False) #cmap1 instead of "vlag"
cbar1 = fig.colorbar(ax.collections[0], cax=row1[0], orientation="horizontal")#,pad=0.1)#location="top", use_gridspec=False, pad=0.1)
sns.heatmap(xeff, cmap=cmap2, ax=ax2,cbar=False,vmin=0, vmax=1)#, center=0.3333, ax=ax2, cbar=False)
cbar2 = fig.colorbar(ax2.collections[0], cax=row1[1], orientation="horizontal")#,pad=0.1)#location="top", use_gridspec=False, pad=0.1)
cbar1.ax.set_title('Transition posterior probability',fontsize=16)
row1[0].xaxis.set_ticks_position('top')
cbar1.set_ticks([0,.5,1])
cbar1.ax.set_xticklabels([0,.5,1],fontsize=16)
cbar2.ax.set_title('Effect posterior probability',fontsize=16)
row1[1].xaxis.set_ticks_position('top')
cbar2.set_ticks([0,.33,1])
cbar2.ax.set_xticklabels([0,.33,1],fontsize=16)
ax2.set_yticks([])
ax.tick_params(axis='y',rotation=0)
ax.tick_params(axis='x',rotation=40)
ax2.tick_params(rotation=50)
plt.setp(ax.xaxis.get_majorticklabels(), ha='right')
plt.setp(ax2.xaxis.get_majorticklabels(), ha='right')
fig.subplots_adjust(wspace=0.1,hspace=0.05,bottom=0.5,top=0.95,left=0.31,right=0.99)
#plt.savefig('../generated_figures/alltopologies_comparingbetweeneffecttype_heatmap.pdf',format='pdf')
plt.show()


