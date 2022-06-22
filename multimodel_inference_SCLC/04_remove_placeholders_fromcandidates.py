import sys
import numpy as np

# run command: python 04_remove_placeholders_fromcandidates.py dir_with_candidate_models a b
#   where a is the model to start with and b is the model to end with (e.g., a=0 b=9327)
#   more specifically: python 04_remove_placeholders_fromcandidates.py /home/beiksp/Bayes-MMI/candidate_models/ 0 5890

args = sys.argv

filedir = args[1]
start_modelnum = args[2]
end_modelnum = args[3]

print ('\nRunning on models: from number '+str(start_modelnum)+' to '+str(end_modelnum)+'.\n')

for j in range(int(start_modelnum),int(end_modelnum)+1):
    outfile=filedir+'/model_'+str(j)+'.py'
    print (outfile)
    # check for whatever
    with open(outfile,"r") as f:
        lines = f.readlines()
    if lines[0]=='#fixed_initial\n':
        print('done already '+outfile)
        continue
    #initval=0.0
    initval = []
    # Do all the collection you need to do
    NE_initline = np.inf
    NEv1_initline = np.inf
    NEv2_initline = np.inf
    NonNE_initline = np.inf
    placeholder_lines = []
    finalline = np.inf
    for n,line in enumerate(lines):
        finalline = n
        if "Parameter('division_0_placeholder_" in line:
            initval.append(float(line.split(',')[1].split(')')[0]))
        if "Parameter('NE_0'," in line:
            NE_initline = n
        if "Parameter('NEv1_0'," in line:
            NEv1_initline = n
        if "Parameter('NEv2_0'," in line:
            NEv2_initline = n
        if "Parameter('NonNE_0'," in line:
            NonNE_initline = n
        if "placeholder" in line:
            placeholder_lines.append(n)
    needs_zeroNE = NE_initline == np.inf
    needs_zeroNEv1 = NEv1_initline == np.inf
    needs_zeroNEv2 = NEv2_initline == np.inf
    needs_zeroNonNE = NonNE_initline == np.inf
    needs_zero = []
    lastinit = -1
    for n,i in enumerate([needs_zeroNE,needs_zeroNEv1,needs_zeroNEv2,needs_zeroNonNE]):
        if i:
            if n == 0:
                needs_zero.append('NE')
            elif n == 1:
                needs_zero.append('NEv1')
            elif n == 2:
                needs_zero.append('NEv2')
            elif n == 3:
                needs_zero.append('NonNE')
            else:
                raise ValueError('Something wrong in the code, cannot appropriately assess what needs to have a zero value, check what is going on.')
        else:
            if n == 0:
                lastinit = NE_initline #this could never happen basically but whatever
            elif n == 1:
                lastinit = NEv1_initline
            elif n == 2:
                lastinit = NEv2_initline
            elif n == 3:
                lastinit = NonNE_initline
    if len(initval)==0: #this shouldnt happen
        raise ValueError('No results from the original file '+str(outfile)+' for which subtype(s) has the initial value, check what is going on.')
    # now if we have moved on:
    if not initval==[4.0]: #initval of [4.0] is the baseline, all models will act like they start at NE with 100 cells
                           #so if that isnt the case, we want to prepare to change it
        try:
            lines[NE_initline] = "Parameter('NE_0', 0.0)\n"
        except TypeError:
            if needs_zeroNE:
                #print (outfile+' : going to assign all NE values to zero.')
                pass
            else:
                print ('Check: '+outfile+' does not have NE initial value and not assigning NEs to zero...')
        # now we have prepared, so then actually change it
        startnum = np.floor(100.0/len(initval))
        #print (startnum)
        for j in initval:
            if j==1.0:
                try:
                    lines[NEv1_initline] = "Parameter('NEv1_0', "+str(startnum)+")\n"
                except TypeError:
                    print (str(outfile)+' cannot determine the initial values line for NEv1, even though command was input that that should be a starting subtype')
                    raise
            elif j==2.0:
                try:
                    lines[NEv2_initline] = "Parameter('NEv2_0', "+str(startnum)+")\n"
                except TypeError:
                    print (str(outfile)+' cannot determine the initial values line for NEv2, even though command was input that that should be a starting subtype')
                    raise
            elif j==3.0:
                try:
                    lines[NonNE_initline] = "Parameter('NonNE_0', "+str(startnum)+")\n"
                except TypeError:
                    print (str(outfile)+' cannot determine the initial values line for NonNE, even though command was input that that should be a starting subtype')
                    raise
            elif j==4.0:
                # dont need try/except bc would have been raised already if didnt have a value for NE_initline
                lines[NE_initline] = "Parameter('NE_0', "+str(startnum)+")\n"
            else: #some other number...
                raise ValueError('Something wrong with reading which subtype(s) has the initial value for '+str(outfile)+', check what is going on.')
    # Determine the new model file lines and print them out
    altlines = set([x for x in range(finalline+1)]).difference(set(placeholder_lines))
    with open(outfile,'w') as f:
        f.write('#fixed_initial\n')
        for i,l in enumerate(lines):
            if i in altlines:
                f.write(l)
            if i==lastinit:
                if len(needs_zero) > 0:
                    f.write("\n#Adding species that will always be zero (no rules)\n")
                    for j in needs_zero:
                        f.write("Monomer('"+j+"')\n")
                        f.write("Parameter('"+j+"_0', 0.0)\n")
                        f.write("Observable('"+j+"_obs', "+j+"())\n")
                        f.write("Initial("+j+"(), "+j+"_0)\n")



