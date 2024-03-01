import pandas as pd
import numpy as np
import copy
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
from matplotlib import collections as matcoll
import seaborn as sns
import sys

indir =  '../files_generated_in_MMI_sclc/'
outdir = '../generated_figures/'

resdf = pd.read_pickle(indir+'galipaud_results_pp_AIC_BIC.pickle')

resdf.index=[
r'$y={\beta_0}$',
r'$y={\beta_0} + {\beta_1}x_1$',
r'$y={\beta_0} + {\beta_2}x_2$',
r'$y={\beta_0} + {\beta_3}x_3$',
r'$y={\beta_0} + {\beta_4}x_4$',
r'$y={\beta_0} + {\beta_1}x_1 + {\beta_2}x_2$',
r'$y={\beta_0} + {\beta_1}x_1 + {\beta_3}x_3$',
r'$y={\beta_0} + {\beta_1}x_1 + {\beta_4}x_4$',
r'$y={\beta_0} + {\beta_2}x_2 + {\beta_3}x_3$',
r'$y={\beta_0} + {\beta_2}x_2 + {\beta_4}x_4$',
r'$y={\beta_0} + {\beta_3}x_3 + {\beta_4}x_4$',
r'$y={\beta_0} + {\beta_1}x_1 + {\beta_2}x_2 + {\beta_3}x_3$',
r'$y={\beta_0} + {\beta_1}x_1 + {\beta_2}x_2 + {\beta_4}x_4$',
r'$y={\beta_0} + {\beta_1}x_1 + {\beta_3}x_3 + {\beta_4}x_4$',
r'$y={\beta_0} + {\beta_2}x_2 + {\beta_3}x_3 + {\beta_4}x_4$',
r'$y={\beta_0} + {\beta_1}x_1 + {\beta_2}x_2 + {\beta_3}x_3 + {\beta_4}x_4$'
]

resdf_pp = copy.deepcopy(resdf)
resdf_pp.sort_values('post_prob_Z',ascending=False,inplace=True)
resdf_pp.reset_index(inplace=True)

## Fig 1C

equalprior_eachcandidate=1/len(resdf_pp)

segs = []
for i in range(len(resdf_pp.index)):
    pair=[(i,equalprior_eachcandidate), (i, resdf_pp.iloc[i].post_prob_Z)]
    segs.append(pair)

plt.rcParams.update({'font.size': 12})

line_segments = matcoll.LineCollection(segs, linestyle='--',label='change from prior probability',color='black')

fig, ax = plt.subplots(figsize=(6,8))
ax.add_collection(line_segments)

sns.scatterplot(resdf_pp.index,resdf_pp.post_prob_Z,ax=ax,label='posterior probability',color='black')
sns.scatterplot([x+.3 for x in range(len(resdf_pp.index))],resdf_pp.w_AICc,ax=ax,label='AIC weights',color='darkred')
#sns.scatterplot([x+.6 for x in range(len(resdf_pp.index))],resdf_pp.BIC_pp_est,ax=ax,label='BIC probability estimate',color='gold')

plt.xticks(range(len(resdf_pp)),resdf_pp['index'],rotation=90)
plt.ylabel('Posterior probability/\nAICc weights')# / BIC ')
plt.xlabel('Candidate models')
plt.subplots_adjust(bottom=0.48,top=0.95,left=0.15,right=0.95)
plt.savefig(outdir+'diff_examplemethods_scatter_wpriorchange_upd2023.pdf',format='pdf')
plt.show()

## Fig 1D

#AIC Galipaud, AIC mine,  pp
x1=[1,          1,         1]
x2=[0.94,       0.81,   0.67]
x3=[0.37,       0.49,   0.28]
x4=[0.37,       0.25,   0.09]

pretzheat = pd.DataFrame({r'$x_1$':x1,r'$x_2$':x2,r'$x_3$':x3,r'$x_4$':x4})
pretzheat.index = ['Summed weights:\nGalipaud et al. 2014','Summed weights:\nthis manuscript','Posterior probability']#,'Post. prob estimated from BIC']
pretzheat_sw = pretzheat.loc[['Summed weights:\nGalipaud et al. 2014','Summed weights:\nthis manuscript']]
pretzheat_pp = pretzheat.loc[['Posterior probability']]#,'Post. prob estimated from BIC']]

colors = ["mediumblue", "cornflowerblue", "white", "lightcoral", "firebrick"]
cmap1 = LinearSegmentedColormap.from_list("mycmap1", list(zip([0,0.25,0.5,0.75,1],colors)))
cmap2 = LinearSegmentedColormap.from_list("mycmap2", list(zip([0,0.5,1],colors[2:])))

plt.rcParams.update({'font.size': 24})

fig, (row1,row2,row3,row4,row5,row6) = plt.subplots(ncols=1,nrows=6,figsize=(14,8),
                                                    gridspec_kw={'height_ratios':[1,2,10,5,2,1]})
ax1=row3
ax2=row4
sns.heatmap(pretzheat_sw, cmap=cmap2, ax=ax1,cbar=False,vmin=0, vmax=1)#, center=0.5, ax=ax, cbar=False) #cmap1 instead of "vlag"
sns.heatmap(pretzheat_pp, cmap=cmap1, ax=ax2,cbar=False,vmin=0, vmax=1)#, center=0.5, ax=ax, cbar=False) #cmap1 instead of "vlag"
cbar1 = fig.colorbar(ax1.collections[0], cax=row1, orientation="horizontal")
cbar1.ax.set_title('Sums of weights',fontsize=16)
row1.xaxis.set_ticks_position('top')
cbar1.set_ticks([0,.5,1])
cbar1.ax.set_xticklabels([0,.5,1],fontsize=16)
ax1.tick_params(axis='y',rotation=0)
#ax1.tick_params(axis='x',rotation=30)
ax1.xaxis.set_ticks_position('top')
plt.setp(ax1.xaxis.get_majorticklabels(), ha='center')

cbar2 = fig.colorbar(ax2.collections[0], cax=row6, orientation="horizontal")
cbar2.set_label('Posterior probability', fontsize=16)
# ticks position for row4/ax2?
cbar2.set_ticks([0,.5,1])
row4.xaxis.set_ticks_position('bottom')
cbar2.ax.set_xticklabels([0,.5,1],fontsize=16)
ax2.tick_params(axis='y',rotation=0)
#ax2.tick_params(axis='x',rotation=30)
plt.setp(ax2.xaxis.get_majorticklabels(), ha='center')

row2.axis('off')
row5.axis('off')
fig.subplots_adjust(bottom=0.15,top=0.9,left=0.33,right=0.95)
plt.savefig(outdir+'diff_examplemethods_heatmap_upd2023.pdf',format='pdf')
plt.show()

## Fig S1A

plt.rcParams.update({'font.size': 12})

fig, axs = plt.subplots(ncols=2,nrows=1,figsize=(10,5))

sns.scatterplot(resdf.BIC_pp_est,resdf.post_prob_Z,s=20,color='black',ax=axs[0])
axs[0].plot([0,1],[0,np.corrcoef(resdf.post_prob_Z,resdf.BIC_pp_est)[0,1]],color='gray',linestyle='--',label='r = '+str(round(np.corrcoef(resdf.post_prob_Z,resdf.BIC_pp_est)[0,1],3)))
# set x and y lims
axs[0].set_xlim(0,np.max(resdf.BIC_pp_est)+.025)
axs[0].set_ylim(0,np.max(resdf.post_prob_Z)+.025)

axs[0].set_xlabel('BIC-estimated posterior probability')
axs[0].set_ylabel('Posterior probability (marginal likelihood)')

axs[0].legend()

sns.scatterplot(resdf.w_AICc,resdf.post_prob_Z,s=20,color='black',ax=axs[1])
axs[1].plot([0,1],[0,np.corrcoef(resdf.post_prob_Z,resdf.w_AICc)[0,1]],color='gray',linestyle='--',label='r = '+str(round(np.corrcoef(resdf.post_prob_Z,resdf.w_AICc)[0,1],3)))
# set x and y lims
axs[1].set_xlim(0,np.max(resdf.w_AICc)+.025)
axs[1].set_ylim(0,np.max(resdf.post_prob_Z)+.025)

axs[1].set_xlabel('AICc weights')
axs[1].set_ylabel('')

axs[1].legend()

fig.subplots_adjust(bottom=0.15,top=0.9,left=0.1,right=0.95,wspace=0.25,hspace=0.1)
plt.savefig(outdir+'galipaud_example_corrZ_AIC_BIC.pdf',format='pdf')
plt.show()

## Fig S1B

dset = 'TKO'    # figures are similar for RPM and clA
df = pd.read_pickle(indir+'results_fromNS_gathered_'+dset+'_addlanalyses.pickle')
df.drop(df.iloc[np.where(np.isnan(df['posterior_prob']))].index, inplace=True)
df['delta_AIC'] = df.AIC - np.min(df.AIC)
df['w_AIC'] = np.exp(-.5 * df.delta_AIC) / np.sum(np.exp(-.5 * df.delta_AIC))
df['BIC_marglik_est'] = np.exp(-df['BIC'] / 2)
df['BIC_pp_est'] = df.BIC_marglik_est / np.sum(df.BIC_marglik_est)

fig, axs = plt.subplots(ncols=2,nrows=1,figsize=(10,5))

sns.scatterplot(df.BIC_pp_est,df.posterior_prob,s=10,color='black',ax=axs[0])
axs[0].plot([0,1],[0,np.corrcoef(df.posterior_prob,df.BIC_pp_est)[0,1]],color='gray',linestyle='--',label='r = '+str(round(np.corrcoef(df.posterior_prob,df.BIC_pp_est)[0,1],3)))
# set x and y lims
axs[0].set_xlim(-0.02, np.max([np.max(df.BIC_pp_est),np.max(df.w_AIC)])+.025)
axs[0].set_ylim(-0.00075, np.max(df.posterior_prob)+.0005)

axs[0].set_xlabel('BIC-estimated posterior probability')
axs[0].set_ylabel('Posterior probability (marginal likelihood)')

axs[0].legend()

sns.scatterplot(df.w_AIC,df.posterior_prob,s=10,color='black',ax=axs[1])
axs[1].plot([0,1],[0,np.corrcoef(df.posterior_prob,df.w_AIC)[0,1]],color='gray',linestyle='--',label='r = '+str(round(np.corrcoef(df.posterior_prob,df.w_AIC)[0,1],3)))
# set x and y lims
axs[1].set_xlim(-0.02,np.max([np.max(df.BIC_pp_est),np.max(df.w_AIC)])+.025)
axs[1].set_ylim(-0.00075,np.max(df.posterior_prob)+.0005)

axs[1].set_xlabel('AIC weights')
axs[1].set_ylabel('')

axs[1].legend()

fig.subplots_adjust(bottom=0.15,top=0.9,left=0.1,right=0.95,wspace=0.25,hspace=0.1)
plt.savefig(outdir+'corrZ_AIC_BIC_for_'+dset+'_data.pdf',format='pdf')
plt.show()
