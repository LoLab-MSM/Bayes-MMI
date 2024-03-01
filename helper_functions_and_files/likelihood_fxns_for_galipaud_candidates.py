import numpy as np
import pandas as pd

df = pd.read_csv('galipaud_sim_dat.csv')
chisquare_denom = np.var(df.y)  # np.std(df.y)**2

def likelihood_beta(position):
    # position is the param values... not using logs because beta should be negative
    chisquare_num = (df.y -
                        (
#                         df.x1*position[0] +
#                         df.x2*position[1] +
#                         df.x3*position[2] +
#                         df.x4*position[3] +
                         position[0]
                        )
                     )**2
    cost_df = chisquare_num / chisquare_denom
    total_cost = -np.sum(cost_df)
    return total_cost

def likelihood_x1(position):
    # position is the param values... not using logs because beta should be negative
    chisquare_num = (df.y -
                        (
                         df.x1*position[0] +
#                         df.x2*position[1] +
#                         df.x3*position[2] +
#                         df.x4*position[3] +
                         position[1]
                        )
                     )**2
    cost_df = chisquare_num / chisquare_denom
    total_cost = -np.sum(cost_df)
    return total_cost

def likelihood_x2(position):
    # position is the param values... not using logs because beta should be negative
    chisquare_num = (df.y -
                        (
#                         df.x1*position[0] +
                         df.x2*position[0] +
#                         df.x3*position[2] +
#                         df.x4*position[3] +
                         position[1]
                        )
                     )**2
    cost_df = chisquare_num / chisquare_denom
    total_cost = -np.sum(cost_df)
    return total_cost

def likelihood_x3(position):
    # position is the param values... not using logs because beta should be negative
    chisquare_num = (df.y -
                        (
#                         df.x1*position[0] +
#                         df.x2*position[1] +
                         df.x3*position[0] +
#                         df.x4*position[3] +
                         position[1]
                        )
                     )**2
    cost_df = chisquare_num / chisquare_denom
    total_cost = -np.sum(cost_df)
    return total_cost

def likelihood_x4(position):
    # position is the param values... not using logs because beta should be negative
    chisquare_num = (df.y -
                        (
#                         df.x1*position[0] +
#                         df.x2*position[1] +
#                         df.x3*position[2] +
                         df.x4*position[0] +
                         position[1]
                        )
                     )**2
    cost_df = chisquare_num / chisquare_denom
    total_cost = -np.sum(cost_df)
    return total_cost

def likelihood_x1x2(position):
    # position is the param values... not using logs because beta should be negative
    chisquare_num = (df.y -
                        (
                         df.x1*position[0] +
                         df.x2*position[1] +
#                         df.x3*position[2] +
#                         df.x4*position[3] +
                         position[2]
                        )
                     )**2
    cost_df = chisquare_num / chisquare_denom
    total_cost = -np.sum(cost_df)
    return total_cost

def likelihood_x1x3(position):
    # position is the param values... not using logs because beta should be negative
    chisquare_num = (df.y -
                        (
                         df.x1*position[0] +
#                         df.x2*position[1] +
                         df.x3*position[1] +
#                         df.x4*position[3] +
                         position[2]
                        )
                     )**2
    cost_df = chisquare_num / chisquare_denom
    total_cost = -np.sum(cost_df)
    return total_cost

def likelihood_x1x4(position):
    # position is the param values... not using logs because beta should be negative
    chisquare_num = (df.y -
                        (
                         df.x1*position[0] +
#                         df.x2*position[1] +
#                         df.x3*position[2] +
                         df.x4*position[1] +
                         position[2]
                        )
                     )**2
    cost_df = chisquare_num / chisquare_denom
    total_cost = -np.sum(cost_df)
    return total_cost

def likelihood_x2x3(position):
    # position is the param values... not using logs because beta should be negative
    chisquare_num = (df.y -
                        (
#                         df.x1*position[0] +
                         df.x2*position[0] +
                         df.x3*position[1] +
#                         df.x4*position[3] +
                         position[2]
                        )
                     )**2
    cost_df = chisquare_num / chisquare_denom
    total_cost = -np.sum(cost_df)
    return total_cost

def likelihood_x2x4(position):
    # position is the param values... not using logs because beta should be negative
    chisquare_num = (df.y -
                        (
#                         df.x1*position[0] +
                         df.x2*position[0] +
#                         df.x3*position[2] +
                         df.x4*position[1] +
                         position[2]
                        )
                     )**2
    cost_df = chisquare_num / chisquare_denom
    total_cost = -np.sum(cost_df)
    return total_cost

def likelihood_x3x4(position):
    # position is the param values... not using logs because beta should be negative
    chisquare_num = (df.y -
                        (
#                         df.x1*position[0] +
#                         df.x2*position[1] +
                         df.x3*position[0] +
                         df.x4*position[1] +
                         position[2]
                        )
                     )**2
    cost_df = chisquare_num / chisquare_denom
    total_cost = -np.sum(cost_df)
    return total_cost

def likelihood_x1x2x3(position):
    # position is the param values... not using logs because beta should be negative
    chisquare_num = (df.y -
                        (
                         df.x1*position[0] +
                         df.x2*position[1] +
                         df.x3*position[2] +
#                         df.x4*position[3] +
                         position[3]
                        )
                     )**2
    cost_df = chisquare_num / chisquare_denom
    total_cost = -np.sum(cost_df)
    return total_cost

def likelihood_x1x2x4(position):
    # position is the param values... not using logs because beta should be negative
    chisquare_num = (df.y -
                        (
                         df.x1*position[0] +
                         df.x2*position[1] +
#                         df.x3*position[2] +
                         df.x4*position[2] +
                         position[3]
                        )
                     )**2
    cost_df = chisquare_num / chisquare_denom
    total_cost = -np.sum(cost_df)
    return total_cost


def likelihood_x1x3x4(position):
    # position is the param values... not using logs because beta should be negative
    chisquare_num = (df.y -
                        (
                         df.x1*position[0] +
#                         df.x2*position[1] +
                         df.x3*position[1] +
                         df.x4*position[2] +
                         position[3]
                        )
                     )**2
    cost_df = chisquare_num / chisquare_denom
    total_cost = -np.sum(cost_df)
    return total_cost

def likelihood_x2x3x4(position):
    # position is the param values... not using logs because beta should be negative
    chisquare_num = (df.y -
                        (
#                         df.x1*position[0] +
                         df.x2*position[0] +
                         df.x3*position[1] +
                         df.x4*position[2] +
                         position[3]
                        )
                     )**2
    cost_df = chisquare_num / chisquare_denom
    total_cost = -np.sum(cost_df)
    return total_cost

####

def likelihood_all(position):
    # position is the param values... not using logs because beta should be negative
    chisquare_num = (df.y -
                        (
                         df.x1*position[0] +
                         df.x2*position[1] +
                         df.x3*position[2] +
                         df.x4*position[3] +
                         position[4]
                        )
                     )**2
    cost_df = chisquare_num / chisquare_denom
    total_cost = -np.sum(cost_df)
    return total_cost