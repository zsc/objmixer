'''
Created on 2010-10-11

@author: zsc

objmixer is a script to allow diagnosing wrong object files, especially useful for debugging a compiler.

Suppose code produced by a compiler with "-O0" is OK, but code produced by "-O2" fails. 
Then we can try to mix the object files from "-O0" and "-O2" to find the wrong object files.

The user need to adapt the obm_plugin.py file to use objmixer.
'''

from subprocess import Popen, PIPE
import os
import random

def random_vector(n):
    for i in range(n):
        yield random.randint(0,1)

def mixByVector(vec,l1,l2):
    if vec==[]:pass
    else:
        v,vs=vec[0],vec[1:]
        x,xs=l1[0],l1[1:]
        y,ys=l2[0],l2[1:]
        if v!=0:
            yield x
        else:
            yield y
        for e in mixByVector(vs,xs,ys):yield e

def splits(l):
    def splitsAux(l):
        if l==[]:yield [([],[])]
        else:
            x,xs = l[0],l[1:]
            pre = []
            for l_ in splitsAux(xs):
                l2 = map(lambda (a,b):(a,[x]+b),l_)
                yield l2+pre
                pre = map(lambda (a,b):([x]+a,b),l_)
            yield pre
    for e in splitsAux(l):
        for i in e:
            yield i
            
def step (compile,objs,alt,canContinue,name,searchType):
    def names(name):
        i=1
        while True:
            yield name+"_"+str(i)
            i+=1
    def objs_gen(objs,alt):
        for (a,b) in splits(objs):
            yield map(alt,a)+b
    if searchType=="Exhaustive":
        og = objs_gen(objs,alt)
        for bin in names(name):
            objs = og.next()
            cmd = compile(objs,bin)
            if (os.system(cmd)!=0):
                print ("CompileFail",objs,bin)
            if(canContinue(bin)):
                print ("NotFound",objs,bin)
            else:
                yield ("Found",objs,bin)
    elif searchType=="Random":
        assert False
    else:
        assert False

def parse(cmd):
    l = cmd.split()
    objs = filter (lambda s:s.endswith(".o"),l)
    libs = filter (lambda s:s.endswith(".a"),l)
    cmdBody = []
    i =0
    while (i<len(l)):
        s = l[i] 
        if s=="-o":
            i+=1
            name = l[i]
        elif s.endswith(".o") or s.endswith(".a"):
            pass
        else:
            cmdBody += [s]
        i+=1
    def compile(objs,bin):
        return " ".join(cmdBody + ["-o",bin] + objs + libs)
    return compile,objs,name
 
def main ():
    print "hi, pydev"
    exec (open("obm_plugin.py"))
    compile,objs,name = parse(compileCommand)
    procResult(step(compile,objs,alt,canContinue,name,searchType))

if __name__ == '__main__':
    main ()
