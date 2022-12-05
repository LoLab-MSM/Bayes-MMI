import pandas as pd
import numpy as np
import copy
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
from matplotlib import collections as matcoll
import seaborn as sns
import sys

indir = '../files_generated_in_MMI_sclc/'
resdf = pd.read_pickle(indir+'galipaud_results_pp_and_AIC.pickle')

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
sns.scatterplot([x+.4 for x in range(len(resdf_pp.index))],resdf_pp.w_AICc,ax=ax,label='sums of weights',color='darkred')

plt.xticks(range(len(resdf_pp)),resdf_pp['index'],rotation=90)
plt.ylabel('Posterior probability/\nSums of AIC weights')
plt.xlabel('Candidate models')
plt.subplots_adjust(bottom=0.48,top=0.95,left=0.15,right=0.95)
plt.savefig('../generated_figures/diff_examplemethods_scatter_wpriorchange.pdf',format='pdf')
plt.show()

x1=[1,1,1]
x2=[0.94,0.87,0.79]
x3=[0.37,0.67,0.49]
x4=[0.37,0.25,0.07]

pretzheat = pd.DataFrame({r'$x_1$':x1,r'$x_2$':x2,r'$x_3$':x3,r'$x_4$':x4})
pretzheat.index = ['Summed weights:\nGalipaud et al. 2014','Summed weights:\nthis manuscript','Posterior probability']
pretzheat_sw = pretzheat.loc[['Summed weights:\nGalipaud et al. 2014','Summed weights:\nthis manuscript']]
pretzheat_pp = pretzheat.loc[['Posterior probability']]

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
plt.savefig('../generated_figures/diff_examplemethods_heatmap.pdf',format='pdf')
plt.show()
