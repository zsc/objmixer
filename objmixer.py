'''
Created on 2010-10-11

@author: zsc

objmixer is a script to allow identifying wrong object files, especially useful for debugging a compiler.

Suppose code produced by a compiler with "-O0" is OK, but code produced by "-O2" fails. 
Then we can try to mix the object files from "-O0" and "-O2" to find the wrong object files.

The user need to adapt the obm_plugin.py file to use objmixer.
'''

from subprocess import Popen, PIPE
import os,sys
import random
     
def randomHalve(l):
    a,a_=[],[]
    for e in l:
        if random.randint(0,1)==0:a+=[e]
        else:a_+=[e]
    return (a,a_)

def list_diff(l1,l2):return [e for e in l1 if e not in l2]

def binSearch(test,l):
    def work(acc,l):
        if len(l)<=1:yield l
        l1,l2 = randomHalve(l)
        for _ in range(3):
            if test((l2,acc+l1)):
                for e in work (acc+l2,l1):yield e
            elif test((l1,acc+l2)):
                for e in work (acc+l1,l2):yield e
        assert False
    for l_ in work ([],l):
        yield (l_,list_diff(l,l_))

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
    def combine((a,b)):return map(alt,a)+b
    def names(name):
        i=1
        while True:
            yield name+"_"+str(i)
            i+=1
    def objs_gen(objs,alt):
        for i in splits(objs):
            yield combine(i)
    def doCompile(objs,bin):
        cmd = compile(objs,bin)
        if (os.system(cmd)!=0):
            print ("CompileFail",objs,bin)
    if searchType=="Exhaustive":
        og = objs_gen(objs,alt)
        for bin in names(name):
            objs = og.next()
            doCompile(objs,bin)
            if(canContinue(bin)):
                print ("NotFound",objs,bin)
            else:
                yield ("Found",objs,bin)
    elif searchType=="Binary":
        ns = names(name)
        def test(l):
            bin = ns.next()
            doCompile(combine(l),bin)
            return canContinue(bin)
        for e in binSearch(test,objs):yield e
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
    print "hi, objmixer"
    try:plugin = open(sys.argv[1])
    except:
        print "Usage:%s path-to-plugin-file"%sys.argv[0]
        exit(-1)
    exec (plugin)
    compile,objs,name = parse(compileCommand)
    procResult(step(compile,objs,alt,canContinue,name,searchType))

if __name__ == '__main__':
    main ()
