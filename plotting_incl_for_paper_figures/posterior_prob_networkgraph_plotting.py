import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.path as path
from matplotlib.patches import FancyArrowPatch, PathPatch
import copy
import pandas as pd
import numpy as np
import seaborn as sns
import math
import sys

pos = {'A':(1,4),
    'A_1': (1.5, 4.33),
    'A_2':(1.75,3.72),
    'A_3':(2.05,4.03), # not just 4.0?
    'A_4':(1.45,3.62),
    'A_div':(2.5,4.6),
    'A_die':(3.5,3.8),
    #'A_die':(3.4,4.5) # change to this for no effects
    #
    'AtoA2': (1.9, 3), # remove for no effects
    'A2': (4, 2),
    #'A2_1':(3.97,0.93),
    #'A2_1': (3.2, 2.2),
    'A2_1':(3.2,2.1),
    'A2_2': (3.16, 2.32),
    'A2_3': (4.85, 2.25),
    'A2_4': (5.04, 2),
    'A2_div': (1.65, 2.1),
    'A2_die': (2, 1.4),
    'A2toY': (7.75, 1.65),
    #
    'AtoN': (3.7, 4.25),
    'N': (8, 4),
    #'N_1':(10.65,4.35), #8.65,4.35
    'N_1': (8.9, 4.1),
    'N_2': (7, 4.1),
    #'N_2':(9,3.9) # change to this for no effects #7,3.9
    'N_3': (7.15, 3.76),
    'N_4': (8.4, 3.6),
    'N_div': (10.65, 4.15),
    'N_die': (10.5, 3.75),
    'NtoY': (10.15, 3.25),
    #
    'Y': (11, 2),
    #'Y_1':(13.8,1.3), #11.8,2.3
    'Y_1': (11.75, 2.25),
    'Y_2': (10, 1.85),
    'Y_3': (11, 2.45),
    #'Y_3':(12.4,1.45) # change to this for no effects #10.4,2.45
    'Y_4':(10.22,2.27),
    'Y_div': (12.2, 2.9),
    'Y_die': (12.7, 1.4)
}

def format_nodes_w_weights(G,edgeweight,parameter_importance,more_than_one_starting):
    node_sizelist = []
    nodecolors = []
    edgecolors = []
    linewidths = []
    importance_by_subtype = {
        'N':parameter_importance[45],
        'A2':parameter_importance[46],
        'Y':parameter_importance[47],
        'A':parameter_importance[48]
        }
    for n in G.nodes:
        if '_1' in n or '_2' in n or '_3' in n or '_4' in n:
            node_sizelist.append(0.1)
            nodecolors.append('gray')
            edgecolors.append('gray')
            linewidths.append(1) #the default
        else:
            if 'div' in n or 'to' in n:
                node_sizelist.append(0.1)
                nodecolors.append('white')
                edgecolors.append('white')
                linewidths.append(1) #the default
            elif 'die' in n:
                node_sizelist.append(10)
                nodecolors.append('black')
                edgecolors.append('black')
                linewidths.append(1) #the default
            else:
                node_sizelist.append(2000)
                nodecolors.append('gray')
                edgecolors.append('black')
                if more_than_one_starting:
                    linewidths.append(1)
                else:
                    linewidths.append(importance_by_subtype[n]*(2*edgeweight))
                # *2 bc my edges start out at 2
    return node_sizelist, nodecolors, edgecolors, linewidths

def get_edge_color(e,colormap=None):
    (u,v,d) = e
    edge_color='purple'
    addn = ''
    try:
        if e[2]['name'] == 'A2_and_Y':
            addn='dark'
    except KeyError:
        pass
    if e[0] == 'Y':
        # in any of the if statements, it's an effect
        if 'div' in e[1] and not 'Y' in e[1]:
            if addn=='dark':
                addn+='olive'
            edge_color=addn+'green'
        elif 'die' in e[1] and not 'Y' in e[1]:
            edge_color=addn+'red'
        elif 'to' in e[1]:
            if addn=='dark':
                addn+='olive'
            edge_color=addn+'green'
        # in the else statement, it's a differentiation
        else:
            edge_color='black'
        if colormap:
            if edge_color=='black': # if it is a differentiation but we wanted to use the colormap
                edge_color=colormap['cmap_diff'](d['weight'])
            else:                  # if it is an effect but we wanted to use the colormap
                edge_color=colormap['cmap_eff'](d['weight'])

    elif e[0] == 'A2':
        if 'div' in e[1] and not 'A2' in e[1] and e[2]['name'] == 'A2_and_Y':
            if addn=='dark':
                addn+='olive'
            edge_color=addn+'green'
        elif 'div' in e[1] and not 'A2' in e[1] and e[2]['name'] == 'Y_only':
            # if it's A2 to A,N,or Y and "Y only"
            # but if it's "Y only" there isn't an edge between A2 and A or N
            # so this just represents edge between A2 and Y
            edge_color=addn+'red'
        elif 'die' in e[1] and not 'A2' in e[1]and e[2]['name'] == 'A2_and_Y':
            edge_color=addn+'red'
        elif 'die' in e[1] and not 'A2' in e[1] and e[2]['name'] == 'Y_only':
            # if it's A2 to A,N,or Y and "Y only"
            # but if it's "Y only" there isn't an edge between A2 and A or N
            # so this just represents edge between A2 and Y
            edge_color=addn + 'green'
        elif 'to' in e[1]:
            if addn=='dark':
                addn+='olive'
            edge_color=addn+'green'
        else:
            edge_color='black'
        # same logic as above
        if colormap:
            if edge_color=='black':
                edge_color=colormap['cmap_diff'](d['weight'])
            else:
                edge_color=colormap['cmap_eff'](d['weight'])
    else:
        if 'div' in e[1] and (not 'A_' in e[1] and not 'N' in e[1]):
            edge_color=addn+'red'
        elif 'die' in e[1] and (not 'A_' in e[1] and not 'N' in e[1]):
            #this condition doesnt exist atm but why not have it in here in case
            if addn=='dark':
                addn+='olive'
            edge_color=addn+'green'
        else:
             edge_color='black'
        # same logic
        if colormap:
            if edge_color=='black':
                edge_color=colormap['cmap_diff'](d['weight'])
            else:
                edge_color=colormap['cmap_eff'](d['weight'])
    return edge_color

def add_to_nx_graph_w_weights(G,parameter_importance,more_than_one_starting):
    has_A = len([x for x in parameter_importance if
                 parameter_importance[1] > 0 or parameter_importance[2] > 0 or parameter_importance[3] > 0]) > 0
    has_N = len([x for x in parameter_importance if
                 parameter_importance[7] > 0 or parameter_importance[8] > 0 or parameter_importance[9] > 0]) > 0
    has_A2 = len([x for x in parameter_importance if
                  parameter_importance[13] > 0 or parameter_importance[14] > 0 or parameter_importance[15] > 0]) > 0
    has_Y = len([x for x in parameter_importance if
                 parameter_importance[19] > 0 or parameter_importance[20] > 0 or parameter_importance[21] > 0]) > 0
    # #for i in parameter_importance:
    if parameter_importance[1]>0:
        if has_A and has_Y:
            G.add_edge('Y', 'A_div', weight=parameter_importance[1],name='Y_only')
    if parameter_importance[2]>0:
        if has_A:
            if has_Y:
                G.add_edge('Y', 'A_div', weight=parameter_importance[2],name='A2_and_Y')
            if has_A2:
                G.add_edge('A2', 'A_div', weight=parameter_importance[2],name='A2_and_Y')
        else:
            print ('param importance for A div > 0 but no N?')
    # don't include death effects to simplify the graph
    # if parameter_importance[4]>0:
    #    if has_A and has_Y:
    #        G.add_edge('Y', 'A_die', weight=parameter_importance[4],name='Y_only')
    # if parameter_importance[5]>0:
    #     if has_A and has_Y:
    #        G.add_edge('Y', 'A_die', weight=parameter_importance[5],name='A2_and_Y')
    #     # same
    #     # ALSO NO ^
    #     if has_A and has_A2:
    #        G.add_edge('A2', 'A_die', weight=parameter_importance[5],name='A2_and_Y')
    if parameter_importance[7]>0:
        if has_N and has_Y:
            G.add_edge('Y', 'N_div', weight=parameter_importance[7],name='Y_only')
    if parameter_importance[8]>0:
        if has_N:
            if has_Y:
                G.add_edge('Y', 'N_div', weight=parameter_importance[8],name='A2_and_Y')
            if has_A2:
                G.add_edge('A2', 'N_div', weight=parameter_importance[8],name='A2_and_Y')
        else:
            print ('param importance for N div > 0 but no N?')
    # not incl death effects
    # if parameter_importance[10]>0:
    #    if has_N and has_Y:
    #        G.add_edge('Y', 'N_die', weight=parameter_importance[10],name='Y_only')
    # if parameter_importance[11]>0:
    #    if has_N and has_Y:
    #        G.add_edge('Y', 'N_die', weight=parameter_importance[11],name='A2_and_Y')
    #    if has_N and has_A2:
    #        G.add_edge('A2', 'N_die', weight=parameter_importance[11],name='A2_and_Y')
    if parameter_importance[13]>0:
        if has_A2 and has_Y:
            G.add_edge('Y', 'A2_div', weight=parameter_importance[13],name='Y_only')
    ## dont include decreasing effects either, to simplify
    # the below are A and N decreasing A2 division
    # if parameter_importance[14]>0:
    #     if has_A and has_A2:
    #         G.add_edge('A', 'A2_div', weight=parameter_importance[14],name='A2_and_Y')
    #     if has_N and has_A2:
    #         G.add_edge('N', 'A2_div', weight=parameter_importance[14],name='A2_and_Y')
    # no death effects
    # if parameter_importance[16]>0:
    #    if has_A2 and has_Y:
    #        G.add_edge('Y', 'A2_die', weight=parameter_importance[16],name='Y_only')
    # if parameter_importance[17]>0:
    #    if has_A and has_A2:
    #        G.add_edge('A', 'A2_die', weight=parameter_importance[17],name='A2_and_Y')
    #    if has_N and has_A2:
    #        G.add_edge('N', 'A2_die', weight=parameter_importance[17],name='A2_and_Y')
    ## no decreasing effects, 19 and 20 are only that
    # if parameter_importance[19]>0:
    #     if has_A and has_Y:
    #         G.add_edge('A', 'Y_div', weight=parameter_importance[19],name='Y_only')
    #     if has_A2 and has_Y:
    #         G.add_edge('A2', 'Y_div', weight=parameter_importance[19],name='Y_only')
    #     if has_N and has_Y:
    #         G.add_edge('N', 'Y_div', weight=parameter_importance[19],name='Y_only')
    # if parameter_importance[20]>0:
    #     if has_A and has_Y:
    #         G.add_edge('A', 'Y_div', weight=parameter_importance[20],name='A2_and_Y')
    #     if has_N and has_Y:
    #         G.add_edge('N', 'Y_div', weight=parameter_importance[20],name='A2_and_Y')
    ## No death effects
    # if parameter_importance[22]>0:
    #     if has_A and has_Y:
    #         G.add_edge('A', 'Y_die', weight=parameter_importance[22],name='Y_only')
    #         print ('adding this edge')
    #     if has_A2 and has_Y:
    #         G.add_edge('A2', 'Y_die', weight=parameter_importance[22],name='Y_only')
    #     if has_N and has_Y:
    #         G.add_edge('N', 'Y_die', weight=parameter_importance[22],name='Y_only')
    # if parameter_importance[23]>0:
    #     if has_A and has_Y:
    #         G.add_edge('A', 'Y_die', weight=parameter_importance[23],name='A2_and_Y')
    #     if has_N and has_Y:
    #         G.add_edge('N', 'Y_die', weight=parameter_importance[23],name='A2_and_Y')
    if parameter_importance[25]>0:
        G.add_node('AtoA2')
        if more_than_one_starting:
            G.add_edge('A', 'A2_2',weight=(1-parameter_importance[50])) #50 is for A->A2
        else:
            G.add_edge('A', 'A2_2')
        if has_Y:
            G.add_edge('Y', 'AtoA2', weight=parameter_importance[25],name='Y_only')
    if parameter_importance[26]>0:
        G.add_node('AtoA2')
        if len([x for x in G.edges if x[0] == 'A' and x[1] == 'A2_2'])==0:
            if more_than_one_starting:
                G.add_edge('A', 'A2_2',weight=(1-parameter_importance[50])) #50 is for A->A2
            else:
                G.add_edge('A', 'A2_2')
        if has_Y:
            G.add_edge('Y', 'AtoA2', weight=parameter_importance[26],name='A2_and_Y')
        if has_A2:
            G.add_edge('A2', 'AtoA2', weight=parameter_importance[26],name='A2_and_Y')
    if parameter_importance[27]>0:
        if len([x for x in G.edges if x[0] == 'A' and x[1] == 'A2_2'])==0:
            if more_than_one_starting:
                G.add_edge('A', 'A2_2',weight=(1-parameter_importance[50])) #50 is for A->A2
            else:
                G.add_edge('A', 'A2_2')
    if parameter_importance[28]>0:
        G.add_node('AtoN')
        if more_than_one_starting:
            G.add_edge('A', 'N_2',weight=(1-parameter_importance[49])) #49 is for A->N)
        else:
            G.add_edge('A', 'N_2')
        if has_Y:
            G.add_edge('Y', 'AtoN', weight=parameter_importance[28],name='Y_only')
    if parameter_importance[29]>0:
        G.add_node('AtoN')
        if len([x for x in G.edges if x[0] == 'A' and x[1] == 'N_2'])==0:
            if more_than_one_starting:
                G.add_edge('A', 'N_2',weight=(1-parameter_importance[49])) #49 is for A->N)
            else:
                G.add_edge('A', 'N_2')
        if has_Y:
           G.add_edge('Y', 'AtoN', weight=parameter_importance[29],name='A2_and_Y')
        if has_A2:
            G.add_edge('A2', 'AtoN', weight=parameter_importance[29],name='A2_and_Y')
    if parameter_importance[30]>0:
        if len([x for x in G.edges if x[0] == 'A' and x[1] == 'N_2']) == 0:
            if more_than_one_starting:
                G.add_edge('A', 'N_2',weight=(1-parameter_importance[49])) #49 is for A->N)
            else:
                G.add_edge('A', 'N_2')
    if parameter_importance[31]>0:
        G.add_node('A2toY')
        if more_than_one_starting:
            G.add_edge('A2', 'Y_2',weight=(1-parameter_importance[52])) #52 is for A2->Y
        else:
            G.add_edge('A2', 'Y_2')
        if has_Y:
            G.add_edge('Y', 'A2toY', weight=parameter_importance[31],name='Y_only')
    if parameter_importance[32]>0:
        G.add_node('A2toY')
        if len([x for x in G.edges if x[0] == 'A2' and x[1] == 'Y_2'])==0:
            if more_than_one_starting:
                G.add_edge('A2', 'Y_2',weight=(1-parameter_importance[52])) #52 is for A2->Y
            else:
                G.add_edge('A2', 'Y_2')
        if has_Y:
           G.add_edge('Y', 'A2toY', weight=parameter_importance[32],name='A2_and_Y')
        if has_A2:
            G.add_edge('A2', 'A2toY', weight=parameter_importance[32],name='A2_and_Y')
    if parameter_importance[33]>0:
        if len([x for x in G.edges if x[0] == 'A2' and x[1] == 'Y_2'])==0:
            if more_than_one_starting:
                G.add_edge('A2', 'Y_2',weight=(1-parameter_importance[52])) #52 is for A2->Y
            else:
                G.add_edge('A2', 'Y_2')
    if parameter_importance[34]>0:
        G.add_node('NtoY')
        if more_than_one_starting:
            G.add_edge('N', 'Y_3',weight=(1-parameter_importance[51])) #51 is for N->Y
        else:
            G.add_edge('N', 'Y_3')
        if has_Y:
            G.add_edge('Y', 'NtoY', weight=parameter_importance[34],name='Y_only')
    if parameter_importance[35]>0:
        G.add_node('NtoY')
        if len([x for x in G.edges if x[0] == 'N' and x[1] == 'Y_3']) == 0:
            if more_than_one_starting:
                G.add_edge('N', 'Y_3',weight=(1-parameter_importance[51])) #51 is for N->Y
            else:
                G.add_edge('N', 'Y_3')
        if has_Y:
           G.add_edge('Y', 'NtoY', weight=parameter_importance[35],name='A2_and_Y')
        if has_A2:
            G.add_edge('A2', 'NtoY', weight=parameter_importance[35],name='A2_and_Y')

    if parameter_importance[36]>0:
        if len([x for x in G.edges if x[0] == 'N' and x[1] == 'Y_3']) == 0:
            if more_than_one_starting:
                G.add_edge('N', 'Y_3',weight=(1-parameter_importance[51])) #51 is for N->Y
            else:
                G.add_edge('N', 'Y_3')
    # now incl backwards
    if parameter_importance[37]>0:
        G.add_edge('N', 'A2_3', weight=parameter_importance[37])  # 37
    if parameter_importance[38]>0:
        G.add_edge('A', 'Y_4', weight=parameter_importance[38])  # 38
    if parameter_importance[39]>0:
        G.add_edge('A2', 'N_3', weight=parameter_importance[39])  # 39
    if parameter_importance[40]>0:
        G.add_edge('Y', 'A_2', weight=parameter_importance[40])  # 40
    if parameter_importance[41]>0:
        G.add_edge('N', 'A_3', weight=parameter_importance[41])  # 41
    if parameter_importance[42]>0:
        G.add_edge('Y', 'N_4', weight=parameter_importance[42])  # 42
    if parameter_importance[43]>0:
        G.add_edge('A2', 'A_4', weight=parameter_importance[43])  # 43
    if parameter_importance[44]>0:
        G.add_edge('Y', 'A2_4', weight=parameter_importance[44])  # 44

### much of split_arrow() is from https://stackoverflow.com/questions/47180328/pyplot-dotted-line-with-fancyarrowpatch
##  further adapted to get nicer looking arrowhead shapes given the strange x-to-y ratio i end up with
##  code for those adaptations from https://stackoverflow.com/questions/57065080/draw-perpendicular-line-of-fixed-length-at-a-point-of-another-line
##   and math from https://stackoverflow.com/questions/7740507/extend-a-line-segment-a-specific-distance
def split_arrow(arrow, color_tail="C0",color_head="C0",
                ls_tail="-", ls_head="-",lw_tail=1.5, lw_head=1.5,
                reqd_width=20, reqd_height=60, y_offset=6,
                alpha_both=0.5):
    reqd_height = reqd_height/100
    reqd_width = reqd_width/100
    v1 = arrow.get_path().vertices[0:3,:]
    c1 = arrow.get_path().codes[0:3]
    p1 = path.Path(v1,c1)
    pp1 = PathPatch(p1, edgecolor=color_tail, facecolor='white', linestyle=ls_tail,
                            fill=False, lw=lw_tail, alpha=alpha_both)
    arrow.axes.add_patch(pp1)
    # figure out the alternate slope with the y offset (ack)
    # and then use that to make the offset arrowheads
    slope = ((v1[-1][1] - v1[-2][1])*y_offset) / (v1[-1][0] - v1[-2][0])
    dy = math.sqrt((reqd_width/2) ** 2 / (slope ** 2 + 1))
    #dy = dy/y_offset
    dx = -slope * dy
    C = [0, 0]
    D = [0, 0]
    C[0] = v1[-1][0] + dx
    C[1] = (v1[-1][1] + dy)#/y_offset
    D[0] = v1[-1][0] - dx
    D[1] = (v1[-1][1] - dy)#/y_offset
    # looks better this way...
    reqd_height = reqd_height/2
    lenAB = np.sqrt((v1[-1][0] - v1[-2][0]) ** 2 + (v1[-1][1] - v1[-2][1]) ** 2)
    new_x = v1[-1][0] + (v1[-1][0] - v1[-2][0]) / lenAB * reqd_height
    new_y = v1[-1][1] + (v1[-1][1] - v1[-2][1]) / lenAB * reqd_height
    #new_y = new_y/y_offset
    mid1 = [((new_x + C[0]) / 2), ((new_y + C[1]) / 2)]#/y_offset]
    mid2 = [((new_x + D[0]) / 2), ((new_y + D[1]) / 2)]#/y_offset]
    v2 = arrow.get_path().vertices[3:8,:]
    c2 = arrow.get_path().codes[3:8]
    if len(c2)==5:
        v2 = [D,mid2,(new_x,new_y),mid1,C]
    else:
        v2 = [D,(new_x,new_y),C]
    c2[0] = 1
    p2 = path.Path(v2,c2)
    pp2 = PathPatch(p2, edgecolor=color_head, facecolor=color_head, lw=lw_head, linestyle=ls_head, alpha=alpha_both)
    arrow.axes.add_patch(pp2)
    arrow.remove()

def make_plots_for_datasets_in_a_row(throughdict,more_than_one_starting=True,colormap=None,savedir=None,
                                     same_edge_weight=True):
    for structnum in throughdict:
        parameter_importance = throughdict[structnum]
        print(structnum)
        parameter_importance.update({y:0 for y in set(range(1,52+1)).difference(set([x for x in parameter_importance]))})
        #
        #
        G = nx.MultiDiGraph(self_loops=True)
        # for node adding with <= 4 subtypes
        has_A = len([x for x in parameter_importance if parameter_importance[1]>0 or parameter_importance[2]>0 or parameter_importance[3]>0])>0
        has_N = len([x for x in parameter_importance if parameter_importance[7]>0 or parameter_importance[8]>0 or parameter_importance[9]>0])>0
        has_A2 = len([x for x in parameter_importance if parameter_importance[13]>0 or parameter_importance[14]>0 or parameter_importance[15]>0])>0
        has_Y = len([x for x in parameter_importance if parameter_importance[19]>0 or parameter_importance[20]>0 or parameter_importance[21]>0])>0
        labels_toshow = {}
        node_inds = {}
        nind = 0
        # taking out death edges and nodes to simplify the graph
        if has_A:
            G.add_nodes_from(['A', 'A_div', 'A_2', 'A_3', 'A_4'])
            G.add_edges_from([('A','A_1')])
            labels_toshow['A'] = 'A'
            node_inds['A'] = nind
            nind += 7
        if has_A2:
            G.add_nodes_from(['A2','A2_div','A2_2','A2_3','A2_4'])
            G.add_edges_from([('A2','A2_1')])
            labels_toshow['A2'] = 'A2'
            node_inds['A2'] = nind
            nind += 7
        if has_N:
            G.add_nodes_from(['N', 'N_div', 'N_2', 'N_3', 'N_4'])
            G.add_edges_from([('N', 'N_1')])
            labels_toshow['N'] = 'N'
            node_inds['N'] = nind
            nind += 7
        if has_Y:
            G.add_nodes_from(['Y', 'Y_div', 'Y_2', 'Y_3', 'Y_4'])
            G.add_edges_from([('Y','Y_1')])
            labels_toshow['Y'] = 'Y'
            node_inds['Y'] = nind
            #nind += 7
        #
        add_to_nx_graph_w_weights(G,parameter_importance,more_than_one_starting)
        #
        #print(G.edges(data=True))
        edges_by_size = {}
        edges_that_change = [] # need to get this before we can get all the plots in general
        remaining_edges = []   # also need this in that case
        for i in np.linspace(0,1,21):
            for j in G.edges(data=True):
                (u,v,d) = j
                try:
                    if d['weight'] > i and d['weight'] <= i + 0.05:
                        if np.round(i,2) in edges_by_size:
                            edges_by_size[np.round(i,2)].append((u,v,d))
                        else:
                            edges_by_size[np.round(i,2)] = [(u,v,d)]
                    edges_that_change.append((u,v,d))
                except KeyError:
                    remaining_edges.append((u,v,d))
        #
        # nodes
        edgeweight = 7.5
        node_sizelist, nodecolors, edgecolors, linewidths = format_nodes_w_weights(G,edgeweight,parameter_importance,more_than_one_starting)
        divlinedetails = {
        'A':{'angleA':90,'angleB':20,'armA':50,'armB':35,'rad':28},
        'A2':{'angleA':195,'angleB':160,'armA':55,'armB':35,'rad':17},
        'N':{'angleA':45,'angleB':0,'armA':50,'armB':40,'rad':22},
        'Y':{'angleA':67.5,'angleB':10,'armA':55,'armB':35,'rad':24}
        }
        #
        difflinedetails = {
         'A,N_2':{'rad':-0.2},#-0.08
        'A,A2_2':{'rad':0.25},
        'N,Y_3':{'rad':-0.2},
        'A2,Y_2':{'rad':0.2} #0.08
        }
        #
        uni_diff_dict = {
        'posv0':{'A2_2':3.5,'Y_3':10.5,'N_2':7.0,'Y_2':10.0},
        'posv1':{'A2_2':2.4,'Y_3':2.45,'N_2':3.92,'Y_2':2.0}
        }
        #
        uni_diffeff_dict = {
        'posv0':{'AtoN':5,'A2toY':7.0,'NtoY':9.55,'AtoA2':2.75},
        'posv1':{'AtoN':3.85,'A2toY':2,'NtoY':3.1,'AtoA2':3}
        }
        #
        # plotting
        ax = plt.gca()
        nx.draw_networkx_nodes(G, pos, node_size=node_sizelist,node_color=nodecolors,edgecolors=edgecolors,linewidths=linewidths,ax=ax)
        to_be_averaged = []
        for i in edges_by_size:
            curvedlines = []
            straightlines = []
            for j in edges_by_size[i]:
                if j[0] == 'A2' or j[0] == 'Y':
                    if 'to' in j[1] or 'div' in j[1] or 'die' in j[1]:
                        curvedlines.append(j)
                    elif j[0]=='A2' and 'Y' in j[1]:
                        curvedlines.append(j)
                    else:
                        straightlines.append(j)
                else:
                    if 'div' in j[1] or 'die' in j[1]:
                        curvedlines.append(j)
                    elif (j[0]=='A' and 'A2' in j[1]) or (j[0]=='A' and 'N' in j[1]) or (j[0]=='N' and 'Y' in j[1]):
                        curvedlines.append(j)
                    else:
                        straightlines.append(j)
                    #if 'die' in j[1]:
                    #    curvedlines.pop()
            curvecolors = []
            if same_edge_weight:
                i = (4/edgeweight) # for control plot
            for k in curvedlines:
                curvecolors.append(get_edge_color(k,colormap))
                to_be_averaged.append(i*edgeweight)
            for n in [n for n,i in enumerate(curvecolors)]:# if i != 'black']:
                u,v,d = curvedlines[n]
                x = (float(pos[u][0]), float(pos[u][1]))
                y = (float(pos[v][0]), float(pos[v][1]))
                extracurve=0
                try:
                    if d['name'] == 'A2_and_Y':
                        extracurve=0.2
                except KeyError:
                    pass
                radval = 0.2+extracurve
                if 'to' in v:
                    # if there is a not a Y -> A2 (which means you want to aim for straight)
                    # and etc
                    if (v == 'AtoN' and not len([x for x in G.edges if x[0] == 'N' and x[1] == 'A_3']) > 0) or (
                            v == 'AtoA2' and not len([x for x in G.edges if x[0] == 'A2' and x[1] == 'A_4']) > 0) or (
                            v == 'NtoY' and not len([x for x in G.edges if x[0] == 'Y' and x[1] == 'N_4']) > 0) or (
                            v == 'A2toY' and not len([x for x in G.edges if x[0] == 'Y' and x[1] == 'A2_4']) > 0):
                        x = (float(pos[u][0]), float(pos[u][1]))
                        y = (float(uni_diffeff_dict['posv0'][v]), float(uni_diffeff_dict['posv1'][v]))
                    if ('Y' in u and 'Y' in v) or ('A2' in u and 'A2' in v):
                        radval = 0.4+extracurve
                    else:
                        radval = 0.1+extracurve
                line_alpha = 0.15
                try: # this try except block with the difflinedetails dict eliminates the need for separation based on assigned colors
                    radval = difflinedetails[str(u) + ',' + str(v)]['rad']
                    line_alpha = 0.65
                except KeyError:
                    pass
                if colormap:
                    line_alpha = 0.8
                l=FancyArrowPatch(x, y, fill='False', linewidth=(i*edgeweight), mutation_scale=5,
                                                      alpha=line_alpha,#alpha=0.15,
                                                      edgecolor=curvecolors[n], facecolor='white', joinstyle='miter',
                                    connectionstyle='arc3,rad=' + str(radval))
                ax.add_line(l)
            #for n in [n for n,i in enumerate(curvecolors) if i=='black']:
            #    u,v,d = curvedlines[n]
            #    x = (float(pos[u][0]),float(pos[u][1]))
            #    y = (float(pos[v][0]),float(pos[v][1]))
            #    # only will be black if it's a differentiation line
            #    # since division lines aren't "edges that change"
            #    radval = difflinedetails[str(u) + ',' + str(v)]['rad']
            #    l = FancyArrowPatch(x,y,fill='False',linewidth=(i*edgeweight),mutation_scale=5,alpha=0.65,
            #        edgecolor=curvecolors[n],facecolor='white',joinstyle='miter',
            #        connectionstyle='arc3,rad=' + str(radval))
            #    ax.add_line(l)
            straightcolors = []
            for k in straightlines:
                straightcolors.append(get_edge_color(k,colormap))
                to_be_averaged.append(i*edgeweight)
            line_alpha = 0.65
            if colormap:
                line_alpha = 0.8
            for n in [n for n,i in enumerate(straightcolors)]:
                u,v,d = straightlines[n]
                x = (float(pos[u][0]),float(pos[u][1]))
                y = (float(pos[v][0]),float(pos[v][1]))
                l = FancyArrowPatch(x,y,fill='False',linewidth=(i*edgeweight),mutation_scale=5,alpha=line_alpha,#alpha=0.65,
                   edgecolor=straightcolors[n],facecolor='white',joinstyle='miter'
                   )
                ax.add_line(l)
        #
        curvedlines = []
        divlines = []
        straightlines = []
        #
        for j in set([(e[0],e[1]) for e in G.edges]).intersection(set([(e[0],e[1]) for e in remaining_edges])):
            if j[1].split('_1')[0] == j[0]:
                divlines.append(j)
            # remaining edges include the forward transitions
            # forward lines should only be curved if the corresponding backward transition is present
            # A to N_2, A to A2_2, A2 to Y_2, N to Y_3
            elif (j[0] == 'A' and j[1] == 'N_2' and len(
                   [x for x in G.edges if x[0] == 'N' and x[1] == 'A_3']) > 0) or (
                                j[0] == 'A' and j[1] == 'A2_2' and len(
                         [x for x in G.edges if x[0] == 'A2' and x[1] == 'A_4']) > 0) or (
                             j[0] == 'N' and j[1] == 'Y_3' and len(
                         [x for x in G.edges if x[0] == 'Y' and x[1] == 'N_4']) > 0) or (
                            j[0] == 'A2' and j[1] == 'Y_2' and len(
                         [x for x in G.edges if x[0] == 'Y' and x[1] == 'A2_4']) > 0):
                curvedlines.append(j)
            else:
                straightlines.append(j)
        #
        for u,v in divlines:
            x = (float(pos[u][0]),float(pos[u][1]))
            y = (float(pos[v][0]),float(pos[v][1]))
            connectionstring = ('arc,angleA='+str(divlinedetails[u]['angleA'])+
                                   ',angleB='+str(divlinedetails[u]['angleB'])+
                                   ',armA=' + str(divlinedetails[u]['armA'])+
                                   ',armB=' + str(divlinedetails[u]['armB'])+
                                   ',rad=' + str(divlinedetails[u]['rad']))
            l = FancyArrowPatch(x,y,fill='False',linewidth=2.5,mutation_scale=5,alpha=1,
                edgecolor='black',facecolor='white',joinstyle='miter',arrowstyle='->',
                connectionstyle=connectionstring)
            ax.add_line(l)
        #
        for u,v in curvedlines:
            x = (float(pos[u][0]),float(pos[u][1]))
            y = (float(pos[v][0]),float(pos[v][1]))
            radval = difflinedetails[str(u)+','+str(v)]['rad']
            l = FancyArrowPatch(x,y,fill='False',linewidth=2,mutation_scale=5,alpha=1,
                edgecolor='black',facecolor='white',joinstyle='miter',
                connectionstyle='arc3,rad='+str(radval))
            ax.add_line(l)
        #
        for u,v in straightlines:
            if not 'die' in v:
                x = (float(pos[u][0]),float(pos[u][1]))
                y = (float(uni_diff_dict['posv0'][v]),float(uni_diff_dict['posv1'][v]))
                l = FancyArrowPatch(x,y,fill='False',linewidth=2,mutation_scale=5,alpha=1,
                    edgecolor='black',facecolor='white',joinstyle='miter')
            else:
                x = (float(pos[u][0]),float(pos[u][1]))
                y = (float(pos[v][0]),float(pos[v][1]))
                l = FancyArrowPatch(x,y,fill='False',linewidth=2,mutation_scale=5,alpha=1,
                    edgecolor='black',facecolor='white',joinstyle='miter')
            ax.add_line(l)
        nx.draw_networkx_labels(G, pos, labels=labels_toshow, font_size=10, font_family='sans-serif')
        plt.xlim(-1,17)
        plt.ylim(0,5.5)
        plt.title(structnum)
        print(savedir+'_'.join(structnum.split())+'.pdf')
        if savedir:
            plt.savefig(savedir+'_'.join(structnum.split())+'.pdf', format='pdf')
        plt.show()
        plt.close()
