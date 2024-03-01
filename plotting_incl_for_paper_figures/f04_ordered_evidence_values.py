import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import copy
import sys

pd.set_option('display.max_columns', 500)

indir =  '../files_generated_in_MMI_sclc/'
outdir = '../generated_figures/'

left = 0.1  # the value on the x axis where the left margin should be
right = 0.9
bottom = 0.1  # the value on the y axis where the bottom margin should be
top = 0.9
wspace = 0.1  # the proportion of the average of the left value and the right value -> for example, 0.2*((0.075+0.95)/2)
hspace = 0.15
plt.rcParams.update({'font.size': 22})
marksize = 40

def ticks_alt(value):
    """
    This function decompose the log value and returns a latex string.
    If 0<=value<99: return the value as it is.
    if 0.1<value<0: returns as it is rounded to the first decimal
    otherwise returns $base*10^{exp}$
    """
    exp = np.floor(value)
    base = abs(round(10**value/10**exp))
    if exp == 0 or exp == 1:
        return '${0:.1f}$'.format(round(10**value,1))
    if exp == -1:
        return '${0:.2f}$'.format(round(10**value,2))
    else:
        return '${0:d}\\times10^{{{1:d}}}$'.format(int(base), int(exp))

def format_logging(value):
    base = np.round(value*(10**(np.ceil(np.log10(value)*-1))))
    exp = np.round(np.log10(value))
    #return '${0:.0f}\\times10^{{{1:.0f}}}$'.format(base, exp)
    return '$10^{{{0:d}}}$'.format(int(exp))

def plot_with_x_and_y_breaks(df, lastprob_ind, add_to_lp=200, figsize=(14,8),
                             toplabel='', bottomlabel='', leftlabel='', rightlabel='',
                             savedir=None):
    if len(df) / (lastprob_ind + add_to_lp) < 2:
        print('Can\'t make x axis breaks because the 95% CI point is after halfway')
        return
    fig,axs = plt.subplots(2,2,figsize=figsize,gridspec_kw={'height_ratios': [2, 1]})
    leftxax = axs[0][0]
    leftxax2 = axs[1][0]
    leftxax.get_shared_x_axes().join(leftxax, leftxax2)
    rightxax = axs[0][1]
    rightxax2 = axs[1][1]
    rightxax.get_shared_x_axes().join(rightxax, rightxax2)
    topyax = axs[0][0]
    topyax2 = axs[0][1]
    topyax.get_shared_y_axes().join(topyax, topyax2)
    bottomyax = axs[1][0]
    bottomyax2 = axs[1][1]
    bottomyax.get_shared_y_axes().join(bottomyax, bottomyax2)
    # plot same data on all axes / that is, all 4 plots... only need to refer to xax or yax,
    sns.scatterplot(df.loc[df.INS_Z<=(np.max(df.INS_Z)/10**.5)].index,df.loc[df.INS_Z<=(np.max(df.INS_Z)/10**.5)].INS_Z,s=marksize,ax=leftxax,linewidth=0.1) #not sure if these edges are making the figures larger
    sns.scatterplot(df.loc[df.INS_Z<=(np.max(df.INS_Z)/10**.5)].index,df.loc[df.INS_Z<=(np.max(df.INS_Z)/10**.5)].INS_Z,s=marksize,ax=leftxax2,linewidth=0.1)
    sns.scatterplot(df.loc[df.INS_Z<=(np.max(df.INS_Z)/10**.5)].index,df.loc[df.INS_Z<=(np.max(df.INS_Z)/10**.5)].INS_Z,s=marksize,ax=rightxax,linewidth=0.1,label='All models')
    sns.scatterplot(df.loc[df.INS_Z<=(np.max(df.INS_Z)/10**.5)].index,df.loc[df.INS_Z<=(np.max(df.INS_Z)/10**.5)].INS_Z,s=marksize,ax=rightxax2,linewidth=0.1)
    #
    sns.scatterplot(df.loc[df['posterior_prob']>df.loc[lastprob_ind].posterior_prob].index,df.loc[df['posterior_prob']>df.loc[lastprob_ind].posterior_prob].INS_Z,color='orange',s=marksize,linewidth=0.1,ax=leftxax)
    sns.scatterplot(df.loc[df['posterior_prob']>df.loc[lastprob_ind].posterior_prob].index,df.loc[df['posterior_prob']>df.loc[lastprob_ind].posterior_prob].INS_Z,color='orange',s=marksize,linewidth=0.1,ax=leftxax2)
    sns.scatterplot(df.loc[df['posterior_prob']>df.loc[lastprob_ind].posterior_prob].index,df.loc[df['posterior_prob']>df.loc[lastprob_ind].posterior_prob].INS_Z,color='orange',s=marksize,linewidth=0.1,ax=rightxax,label='95% CI')
    sns.scatterplot(df.loc[df['posterior_prob']>df.loc[lastprob_ind].posterior_prob].index,df.loc[df['posterior_prob']>df.loc[lastprob_ind].posterior_prob].INS_Z,color='orange',s=marksize,linewidth=0.1,ax=rightxax2)
    #
    sns.scatterplot(df.loc[df.INS_Z>(np.max(df.INS_Z)/10**.5)].index,df.loc[df.INS_Z>(np.max(df.INS_Z)/10**.5)].INS_Z,color='red',s=marksize,linewidth=0.1,ax=leftxax)
    sns.scatterplot(df.loc[df.INS_Z>(np.max(df.INS_Z)/10**.5)].index,df.loc[df.INS_Z>(np.max(df.INS_Z)/10**.5)].INS_Z,color='red',s=marksize,linewidth=0.1,ax=leftxax2)
    sns.scatterplot(df.loc[df.INS_Z>(np.max(df.INS_Z)/10**.5)].index,df.loc[df.INS_Z>(np.max(df.INS_Z)/10**.5)].INS_Z,color='red',s=marksize,linewidth=0.1,ax=rightxax,label='relative likelihood CI')
    sns.scatterplot(df.loc[df.INS_Z>(np.max(df.INS_Z)/10**.5)].index,df.loc[df.INS_Z>(np.max(df.INS_Z)/10**.5)].INS_Z,color='red',s=marksize,linewidth=0.1,ax=rightxax2)
    #
    # Y AXIS ... do everything twice (once "left", once "right")
    # left
    # set where the breaks should be
    leftxax.set_yscale('log')
    leftxax2.set_yscale('log')
    leftxax.set_ylim(df.loc[(lastprob_ind+add_to_lp)].INS_Z,10**(np.floor(np.log10(df.INS_Z.max()))+1)) #max score, next order of magnitude up
    leftxax2.set_ylim(10**(np.floor(np.log10(df.INS_Z.min()))-1),df.loc[len(df.index)-(lastprob_ind+add_to_lp)].INS_Z)  # min score, next order of magnitude down
    # set the ticks at the breaks
    leftxax.set_yticks(list(leftxax.get_yticks())[2:-1])
    leftxax2.set_yticks(list(leftxax2.get_yticks())[:-2][::2] + [0.0001])
    # hide the spines between ax and ax2
    leftxax.spines['bottom'].set_visible(False)
    leftxax2.spines['top'].set_visible(False)
    # hide the ticks at the bottom of ax, ax2, and set them for ax3
    leftxax.set_xlim(-50,(lastprob_ind+add_to_lp))
    leftxax2.set_xlim(-50,(lastprob_ind+add_to_lp))
    #leftxax2.set_xticks(list(leftxax2.get_xticks())[::2])
    leftxax2.set_xticks([x*500 for x in list(range(0,int(np.floor((lastprob_ind+add_to_lp)/500))+1))])
    leftxax.set_xticks([])
    leftxax2.xaxis.tick_bottom()
    # make the breaks
    d = .015  # how big to make the diagonal lines in axes coordinates
    # arguments to pass to plot, just so we don't keep repeating them
    kwargs = dict(transform=leftxax.transAxes, color='k', clip_on=False)
    leftxax.plot((-d, +d), (-d, +d), **kwargs)        # top-left diagonal
    # ax2
    kwargs.update(transform=leftxax2.transAxes)  # switch axes
    d = .033  # how big to make the diagonal lines in axes coordinates
    d_ang = 0.018 # if d_ang = 0, d is _solely_ how big to make the diagonal lines in axes coordinates
    #            # if it's > 0, it will affect the rotation; in this case may want to increase d
    #            # must be 0 < d_ang < d for this purpose; the closer to d, the steeper the angle
    leftxax2.plot((-(d-d_ang), +(d-d_ang)), (1 - d, 1 + d), **kwargs)  # bottom-left diagonal
    # right
    # set where the breaks should be
    rightxax.set_yscale('log')
    rightxax2.set_yscale('log')
    rightxax.set_ylim(df.loc[(lastprob_ind+add_to_lp)].INS_Z,10**(np.floor(np.log10(df.INS_Z.max()))+1))
    rightxax2.set_ylim(10**(np.floor(np.log10(df.INS_Z.min()))-1),df.loc[len(df.index)-(lastprob_ind+add_to_lp)].INS_Z)  # remaining scores #0.11 was good for non-log
    # also do xlim for everything
    rightxax.set_xlim(len(df.index)-(lastprob_ind+add_to_lp),len(df.index)+50)
    rightxax2.set_xlim(len(df.index)-(lastprob_ind+add_to_lp),len(df.index)+50)
    # no ticks for this bc it's in the middle of the plot
    rightxax.yaxis.set_ticks_position("right")
    rightxax.yaxis.set_ticklabels([format_logging(x) for x in rightxax.get_yticks()/np.sum(df.INS_Z)])
    rightxax2.yaxis.set_ticks_position("right")
    rightxax2.yaxis.set_ticklabels([format_logging(x) for x in rightxax2.get_yticks()/np.sum(df.INS_Z)])
    rightxax.yaxis.set_label_position("right")
    rightxax2.yaxis.set_label_position("right")
    #
    rightxax.spines['bottom'].set_visible(False)
    rightxax2.spines['top'].set_visible(False)
    rightxax2.set_xticks(list(rightxax2.get_xticks()))#[::2])
    rightxax.set_xticks([])
    rightxax2.xaxis.tick_bottom()
    # x axis
    # make the breaks
    # arguments to pass to plot, just so we don't keep repeating them
    kwargs = dict(transform=rightxax.transAxes, color='k', clip_on=False)
    d = 0.015
    rightxax.plot((1 - d, 1 + d), (-d, +d), **kwargs)  # top-right diagonal
    # ax2
    kwargs.update(transform=rightxax2.transAxes)  # switch to the middle axes
    d = 0.033
    rightxax2.plot((1 - (d-d_ang), 1 + (d-d_ang)), (1 - d, 1 + d), **kwargs)
    #plt.show()
    #
    # X AXIS
    # top plots
    # set where the breaks should be
    topyax.set_xlim(-50,(lastprob_ind+add_to_lp))
    topyax2.set_xlim(len(df.index)-(lastprob_ind+add_to_lp),len(df.index)+50)
    # hide the spines between ax and ax2
    topyax.spines['right'].set_visible(False)
    topyax2.spines['left'].set_visible(False)
    # hide the ticks on the right side
    topyax2.yaxis.tick_right()
    topyax.yaxis.tick_left()
    # make the breaks
    d = .015
    kwargs = dict(transform=topyax.transAxes, color='k', clip_on=False)
    topyax.plot((1 - d, 1 + d), (1 - d, 1 + d), **kwargs)  # [0][0], top-right diagonal
    # ax2
    kwargs.update(transform=topyax2.transAxes)  # switch to the other axes
    topyax2.plot((-d, +d), (1 - d, 1 + d), **kwargs)       # [0][1], top-left diagonal
    topyax2.set_ylabel('')
    # set ylims for this too
    topyax.set_ylim(df.loc[(lastprob_ind+add_to_lp)].INS_Z,10**(np.floor(np.log10(df.INS_Z.max()))+1)) #max score, next order of magnitude up
    topyax2.set_ylim(df.loc[(lastprob_ind+add_to_lp)].INS_Z,10**(np.floor(np.log10(df.INS_Z.max()))+1)) #max score, next order of magnitude up
    # bottom plots
    #bottomyax.set_xlim(-50,(lastprob_ind+add_to_lp))
    #bottomyax2.set_xlim(len(df.index)-(lastprob_ind+add_to_lp),len(df.index)+50)
    #plt.show()
    # set the ticks at the breaks
    # hide spines and ticks
    bottomyax.spines['right'].set_visible(False)
    bottomyax2.spines['left'].set_visible(False)
    bottomyax.yaxis.tick_left()
    bottomyax2.yaxis.tick_right()
    # make the breaks with different angles bc the bottom plot needs that
    d = .033 # for differently angled diagonals
    kwargs = dict(transform=bottomyax.transAxes, color='k', clip_on=False)
    # for bottom axes
    bottomyax.plot((1 - (d-d_ang), 1 + (d-d_ang)), (-d, +d), **kwargs)  # [1][0], bottom-right diagonal
    kwargs.update(transform=bottomyax2.transAxes) #switch
    bottomyax2.plot((-(d-d_ang), +(d-d_ang)), (-d, +d), **kwargs)       # [1][1], bottom-left diagonal
    bottomyax.set_ylim(10**(np.floor(np.log10(df.INS_Z.min()))-1),df.loc[len(df.index)-(lastprob_ind+add_to_lp)].INS_Z)  # min score, next order of magnitude down
    bottomyax2.set_ylim(10**(np.floor(np.log10(df.INS_Z.min()))-1),df.loc[len(df.index)-(lastprob_ind+add_to_lp)].INS_Z)  # min score, next order of magnitude down
    #labeling
    topyax.set_ylabel('')
    bottomyax2.set_ylabel('')
    bottomyax.set_ylabel('')
    fig.text(0.01,0.5,leftlabel,va='center',rotation='vertical')
    fig.text(0.99,0.5,rightlabel,va='center',rotation='vertical')
    fig.text(0.45,0.025,bottomlabel,va='center',rotation='horizontal')
    fig.text((.5-(len(toplabel)*0.0055)),0.96,toplabel,va='center',rotation='horizontal')
    plt.subplots_adjust(left=left, right=right, bottom=bottom, top=top, wspace=wspace, hspace=hspace)
    if savedir:
        plt.savefig(savedir+dset+'_evidence_ordered.pdf',format='pdf')
    plt.show()


def plot_with_y_breaks(df, lastprob_ind, add_to_lp=200, figsize=(14,8),
                             toplabel='', bottomlabel='', leftlabel='', rightlabel='',
                             savedir=None):
    fig,axs = plt.subplots(2,1,figsize=figsize,gridspec_kw={'height_ratios': [2, 1]})
    ax = axs[0]
    ax2 = axs[1]
    ax.get_shared_x_axes().join(ax, ax2)
    rightax = ax.twinx()
    rightax2 = ax2.twinx()
    ax.get_shared_y_axes().join(ax, rightax)
    ax.get_shared_y_axes().join(ax2, rightax2)
    # plot same data on both axes
    sns.scatterplot(df.index,df.INS_Z,s=marksize,linewidth=0.1,ax=ax)
    sns.scatterplot(df.index,df.INS_Z,s=marksize,ax=ax2)
    #
    sns.scatterplot(df.loc[df['posterior_prob']>df.loc[lastprob_ind].posterior_prob].index,df.loc[df['posterior_prob']>df.loc[lastprob_ind].posterior_prob].INS_Z,color='orange',s=marksize,linewidth=0.1,ax=ax,label='95% CI')
    sns.scatterplot(df.loc[df['posterior_prob']>df.loc[lastprob_ind].posterior_prob].index,df.loc[df['posterior_prob']>df.loc[lastprob_ind].posterior_prob].INS_Z,color='orange',s=marksize,linewidth=0.1,ax=ax2)
    #
    sns.scatterplot(df.loc[df.INS_Z>(np.max(df.INS_Z)/10**.5)].index,df.loc[df.INS_Z>(np.max(df.INS_Z)/10**.5)].INS_Z,color='red',s=marksize,linewidth=0.1,ax=ax,label='relative likelihood CI')
    sns.scatterplot(df.loc[df.INS_Z>(np.max(df.INS_Z)/10**.5)].index,df.loc[df.INS_Z>(np.max(df.INS_Z)/10**.5)].INS_Z,color='red',s=marksize,linewidth=0.1,ax=ax2)
    # this should be setting the plot so only need to do once, after plotting all the ks and js
    # set where the breaks should be
    ax.set_yscale('log')
    ax2.set_yscale('log')
    rightax.set_yscale('log')
    rightax2.set_yscale('log')
    ax.set_ylim(0.075,df.INS_Z.max())
    ax2.set_ylim(1e-16,0.025)
    # set the ticks at the breaks
    ax.set_yticks(list(ax.get_yticks())[2:-1])
    ax2.set_yticks(list(ax2.get_yticks())[:-2][::2] + [0.0001])
    # hide the spines between ax and ax2
    ax.spines['bottom'].set_visible(False)
    ax2.spines['top'].set_visible(False)
    rightax.spines['bottom'].set_visible(False)
    rightax2.spines['top'].set_visible(False)
    # hide the ticks at the bottom of ax, ax2, and set them for ax3
    ax.set_xticks([])
    ax2.xaxis.tick_bottom()
    rightax.yaxis.set_ticks_position("right")
    rightax.yaxis.set_ticklabels([format_logging(x) for x in rightax.get_yticks() / np.sum(df.INS_Z)])
    rightax2.yaxis.set_ticks_position("right")
    rightax2.yaxis.set_ticklabels([format_logging(x) for x in rightax2.get_yticks() / np.sum(df.INS_Z)])
    # make the breaks
    d = .015  # how big to make the diagonal lines in axes coordinates
    # arguments to pass to plot, just so we don't keep repeating them
    kwargs = dict(transform=ax.transAxes, color='k', clip_on=False)
    ax.plot((-d, +d), (-d, +d), **kwargs)        # top-left diagonal
    ax.plot((1 - d, 1 + d), (-d, +d), **kwargs)  # top-right diagonal
    # ax2
    kwargs.update(transform=ax2.transAxes)  # switch to the middle axes
    ax2.plot((-d, +d), (1 - d, 1 + d), **kwargs)  # bottom-left diagonal
    ax2.plot((1 - d, 1 + d), (1 - d, 1 + d), **kwargs)
    ax2.set_ylabel('')
    ax.set_ylabel('')
    ax.legend(loc=1)
    fig.text(0.01,0.5,leftlabel,va='center',rotation='vertical')
    fig.text(0.99,0.5,rightlabel,va='center',rotation='vertical')
    fig.text(0.45,0.025,bottomlabel,va='center',rotation='horizontal')
    fig.text((.5-(len(toplabel)*0.0055)),0.96,toplabel,va='center',rotation='horizontal')
    #plt.title(toplabel)
    plt.subplots_adjust(left=left, right=right, bottom=bottom, top=top, wspace=wspace, hspace=hspace)
    if savedir:
        plt.savefig(savedir+dset+'_evidence_ordered.pdf',format='pdf')
    plt.show()

CInums = {}
for dset in ['TKO','RPM','clA']:
    df = pd.read_pickle(indir + '/results_fromNS_gathered_' + dset + '_addlanalyses.pickle')
    #
    df.sort_values('posterior_prob',ascending=False,inplace=True)
    df.reset_index(inplace=True)
    #
    lastprob_ind = 0
    while np.sum(df.loc[df.posterior_prob>df.loc[lastprob_ind].posterior_prob].posterior_prob) < 0.95:
        lastprob_ind += 1
    #
    # prep for Fig 4D
    CInums[dset] = {
                    'non 95% CI':len(df)-len(df.loc[df.posterior_prob>df.loc[lastprob_ind].posterior_prob]),
                    '95% CI':len(df) - len(df.loc[df.INS_Z > (np.max(df.INS_Z) / 10 ** .5)]),
                    'relative likelihood CI':len(df)
                    }
    ## Fig 4A-C
    add_to_lp = 200
    if len(df) / (lastprob_ind + add_to_lp) < 2:
        plot_with_y_breaks(df,lastprob_ind,toplabel=(dset if dset != 'clA' else 'SCLC-A cell lines'),bottomlabel='Model no.',
                           leftlabel='Evidence (marginal likelihood)',rightlabel='Posterior probability',
                           savedir=outdir)
    else:
        plot_with_x_and_y_breaks(df,lastprob_ind,toplabel=(dset if dset != 'clA' else 'SCLC-A cell lines'),bottomlabel='Model no.',
                                 leftlabel='Evidence (marginal likelihood)',rightlabel='Posterior probability',
                                 savedir=outdir)

####
## Fig 4D

# example from when i did this using both all-models group and 4-subtype only models
#df1 = pd.DataFrame(CInums['SCLC-A cell lines'],index=[0])#['all models'],index=[0])
#df1['models'] = 'all models'
#df2 = pd.DataFrame(CInums['SCLC-A cell lines']['4-subtype only'],index=[0])
#df2['models'] = '4-subtype only'
#df_c = pd.concat([df1,df2])
#df_c = df1
#df_c['dataset'] = 'SCLC-A cell lines'
#
df_c = pd.DataFrame(CInums['clA'],index=[0])
df_c['dataset'] = 'SCLC-A cell lines'
#
df_r = pd.DataFrame(CInums['RPM'],index=[0])
df_r['dataset'] = 'RPM'
#
df_t = pd.DataFrame(CInums['TKO'],index=[0])
df_t['dataset'] = 'TKO'
#
dfCIs = pd.concat([df_t,df_r,df_c],ignore_index=True)

colors = ["red", "orange","blue"]
colpal = sns.color_palette(colors)

plt.rcParams.update({'font.size': 24})
sns.axes_style("white")
sns.set_style("ticks")
sns.set_context("talk")

bar_width = 0.3
anyextra = 0.2
TKO_bar_positions = np.arange(1)*2
RPM_bar_positions = TKO_bar_positions + bar_width + anyextra
SCLCA_bar_positions = RPM_bar_positions + bar_width + anyextra
pos=[TKO_bar_positions,RPM_bar_positions,SCLCA_bar_positions]

fig,ax=plt.subplots(figsize=(8,8))
for n,j in enumerate(['TKO','RPM','SCLC-A cell lines']):
    if n==0:
        plt.bar(pos[n],
        (dfCIs['relative likelihood CI']).loc[dfCIs.dataset==j],
        bar_width,
        color='red',label='relative likelihood CI')
        plt.bar(pos[n],
        (dfCIs['95% CI']).loc[dfCIs.dataset==j],
        bar_width,
        color='orange',label='95% CI')
        plt.bar(pos[n],
        dfCIs['non 95% CI'].loc[dfCIs['dataset']==j],
        bar_width,color='royalblue',label='non 95% CI')
    else:
        plt.bar(pos[n],
        (dfCIs['relative likelihood CI']).loc[dfCIs.dataset==j],
        bar_width,
        color='red')
        plt.bar(pos[n],
        (dfCIs['95% CI']).loc[dfCIs.dataset==j],
        bar_width,
        color='orange')
        plt.bar(pos[n],
        dfCIs['non 95% CI'].loc[dfCIs['dataset']==j],
        bar_width,color='royalblue')

# to write the percentages over the bars
for n,r in enumerate(ax.patches):
    ind = int((n/3))
    size=14
    height = r.get_height()
    if n%3==0: #needs to be the number of stacks per bar
        lab = list((dfCIs['relative likelihood CI']-dfCIs['95% CI']) / dfCIs['relative likelihood CI'])[ind]
        ax.text(r.get_x() + r.get_width() / 2, height, str(np.round(lab*100,2))+'%', ha='center', va='bottom', fontsize=size)
    elif n%3==1:
        lab = list((dfCIs['95% CI']-dfCIs['non 95% CI']) / dfCIs['relative likelihood CI'])[ind]
        ax.text(r.get_x() + r.get_width() / 2, height-plt.rcParams['font.size']*5, str(np.round(lab*100,2))+'%', ha='center', va='top',fontsize=size)
    else:
        lab = list(dfCIs['non 95% CI'] / dfCIs['relative likelihood CI'])[ind]
        ax.text(r.get_x() + r.get_width() / 2, height-plt.rcParams['font.size']*5, str(np.round(lab*100,2))+'%', ha='center', va='top',fontsize=size)

plt.xticks([TKO_bar_positions[0],RPM_bar_positions[0],SCLCA_bar_positions[0]], ['TKO','RPM','SCLC-A'])
plt.legend(fontsize=14,loc='best')
plt.ylabel('# Models')
plt.xlabel('Dataset')
sns.despine()
#plt.subplots_adjust(left=left, right=right, bottom=bottom, top=top, wspace=wspace, hspace=hspace)
plt.tight_layout()
plt.savefig(outdir+'number_models_perCIs_bw_dataset.pdf',format='pdf')
plt.show()




