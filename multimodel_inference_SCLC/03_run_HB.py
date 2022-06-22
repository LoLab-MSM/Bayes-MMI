# to run an example just uncomment the appropriate line and run this file

import sys

# append the directory containing HypBuilder to the path so you can import it
sys.path.append('/home/')
from HypBuilder.HypBuilder import ModelAssembler

# assign the hypbuilder directory to a variable
hb_dir = '/home/'

## This script will make a directory called 'output' in whatever directory you run this script in
#   (unless there's an 'output' directory there already)
# then, within 'output', it will generate a directory(ies) with
#  whatever text comes before .csv (the second argument to ModelAssembler)
# so if you direct ModelAssembler to a csv file in another location, it will use
#  the name(s) of the other location(s) and make those directories in 'output'
# for example, if the csv file is in another directory and denoted as '/home/beiksp/example_csv.csv',
#  in the directory you gave the run command, it will create (or use if it exists) 'output/home/beiksp/example_csv/'
#  and put all generated model files there

ModelAssembler(hb_dir+'/HB_library.txt', '02_sclc_multimodelinference_models_updatedjun2022.csv')
# ModelAssembler(hb_dir+'/HB_library.txt', hb_dir+'/earm_example.csv')
# ModelAssembler(hb_dir+'/HB_library.txt', hb_dir+'/optional_reactions_example.csv')
# ModelAssembler(hb_dir+'/HB_library.txt', hb_dir+'/initial_binding_example.csv')
# ModelAssembler(hb_dir+'/HB_library.txt', hb_dir+'/initial_values_example.csv')
# ModelAssembler(hb_dir+'/HB_library.txt', hb_dir+'/dwdc_example.csv')
ModelAssembler(hb_dir+'/HB_library.txt', hb_dir+'/binding_sites_example.csv')
# ModelAssembler(hb_dir+'/HB_library.txt', hb_dir+'/expression_and_text_examples.csv')
# ModelAssembler(hb_dir+'/HB_library.txt', hb_dir+'/listed_reactions_example.csv')
# ModelAssembler(hb_dir+'/HB_library.txt', hb_dir+'/Boolean_filter_example.csv')
