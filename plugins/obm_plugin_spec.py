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
    return "correct/"+s

compileCommand = "gcc bc-emit.o bc-optab.o c-aux-info.o c-common.o c-convert.o c-decl.o c-iterate.o c-lang.o c-lex.o c-parse.o c-pragma.o c-typeck.o caller-save.o calls.o combine.o convert.o cse.o dbxout.o dwarfout.o emit-rtl.o explow.o expmed.o expr.o final.o flow.o fold-const.o function.o getpwd.o global.o insn-attrtab.o insn-emit.o insn-extract.o insn-opinit.o insn-output.o insn-peep.o insn-recog.o integrate.o jump.o local-alloc.o loop.o m88k.o obstack.o optabs.o print-rtl.o print-tree.o real.o recog.o reg-stack.o regclass.o reload.o reload1.o reorg.o rtl.o rtlanal.o sched.o sdbout.o stmt.o stor-layout.o stupid.o toplev.o tree.o unroll.o varasm.o version.o xcoffout.o  -static -O3 -lm     -o cc1" 

'''
  Key content of the cmd script is the time limit set by ulimit
     ulimit -t 1;cd /home/cpu/CPU2000/benchspec/CINT2000/176.gcc/exe;./cc1_base.godson_linux ../data/ref/input/166.i -o 166.s > 166.out 2>> 166.err
'''

def canContinue(bin):
    ret = os.system("/usr/bin/scp %s cpu@10.3.0.214:CPU2000/benchspec/CINT2000/176.gcc/exe/cc1_base.godson_linux"%bin)
    if ret!=0:return False
    #cmd = "/usr/bin/ssh -l root 10.3.0.214 cd CPU2000; source shrc; ulimit -s unlimited;ulimit -c unlimited;runspec -I -c godson -n 1 -i ref gcc"
    cmd = 'ssh cpu@10.3.0.214 "LC_ALL=C LC_LANG=C sh cmd"'
    p = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
    out, err = p.communicate()
    print out,err
    return ((out+err).find("Aborted")!=-1)
##    p = Popen(cmd, shell=True)
##    sts = os.waitpid(p.pid, 0)[1]
#    sts = os.system(cmd)
#    print "cancontinue",sts
#    return (sts==35584)

def procResult(r):
    print r.next ()