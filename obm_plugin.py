'''
Created on 2010-10-11

@author: zsc

A sample plugin file.

We start from potentially wrong object files and gradually replace with correct ones.
We stop upon seeing the symptom gone.

User need to define alt, compileCommand, canContinue, procResult in this file.

alt: tells where the alternative good objects files reside in.
compileCommand: tells how to link the object files
canContinue: whether we should continue the search.
procResult: how we handle the found results.
'''

import os
from subprocess import Popen, PIPE

searchType = "Binary"
#searchType = "Exhaustive"
#searchType = "Random"

def alt(s):
    return "../../gcc4.4-build.O0/gcc/"+s

compileCommand = "loongcc -static -G0 -Gspace0  -O2 -DIN_GCC   -W -Wall -Wwrite-strings -Wstrict-prototypes -Wmissing-prototypes -Wcast-qual -Wc++-compat -Wmissing-format-attribute -pedantic -Wno-long-long -Wno-variadic-macros -Wno-overlength-strings   -DHAVE_CONFIG_H  -o xgcc gcc.o opts-common.o gcc-options.o gccspec.o           intl.o prefix.o version.o driver-native.o ../libcpp/libcpp.a   ../libiberty/libiberty.a ../libdecnumber/libdecnumber.a" 

def canContinue(bin):
    cmd = ["./"+bin, "-v"]
    p = Popen(cmd, stdout=PIPE, stderr=PIPE)
    out, err = p.communicate()
    print out,err
    return (err.find("Segmentation")!=-1)
##    p = Popen(cmd, shell=True)
##    sts = os.waitpid(p.pid, 0)[1]
#    sts = os.system(cmd)
#    print "cancontinue",sts
#    return (sts==35584)

def procResult(r):
    print r.next ()