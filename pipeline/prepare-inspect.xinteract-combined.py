#!/usr/bin/python 
import os
import sys
import stat
import massspec_toolbox_config as conf

path_xinteract = conf.get_TPP_path('xinteract')
path_prot_prophet = conf.get_TPP_path('ProteinProphet')

path_APEX_parser = conf.get_TPP2APEX_parser()
TPP_cutoff = 0.05

filename_script = 'run-inspect.xinteract-combined.sh';
f_script = open(filename_script,'w')
f_script.write('#!/bin/bash\n')
f_script.write('SAMPLE_NAME="tmp"\n')

for filename_pepxml in os.listdir('inspect'):
    filename_pepxml = filename_pepxml.strip()
    if( not filename_pepxml.endswith('.inspect.pepxml') ):
        continue
    
    filename_base = filename_pepxml.replace('.pepxml','')
    filename_pepxml = os.path.join('inspect',filename_pepxml)

    f_script.write('cp %s %s\n'%(filename_pepxml,'tmp/'))

filename_base = os.path.join('inspect.xinteract','$SAMPLE_NAME')
filename_xinteract = filename_base+'.xinteract.xml'
filename_prot = filename_base+'.xinteract.prot.xml'
filename_summary = filename_base+'.xinteract.summary'

filename_prot_nonsp = filename_base+'.xinteract_NOSP.prot.xml'
filename_summary_nonsp = filename_base+'.xinteract_NONSP.summary'

f_script.write("%s -N%s -Op -dxf_ tmp/*.pepxml\n"%(path_xinteract,filename_xinteract))
f_script.write("%s %s %.2f %s\n"%(path_APEX_parser,filename_prot,TPP_cutoff,filename_summary))
f_script.write("%s NONSP %s %s\n"%(path_prot_prophet,filename_xinteract,filename_prot_nonsp))
f_script.write("%s %s %.2f %s\n"%(path_APEX_parser,filename_prot_nonsp,TPP_cutoff,filename_summary_nonsp))

f_script.write('rm -f tmp/*')
f_script.close()
os.chmod(filename_script,stat.S_IRWXU)
