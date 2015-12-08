import os
import subprocess
import sys


def convertDotGraph(dotFile, outputType):
    base, _ext = os.path.splitext(dotFile)
    outfile = os.path.basename(base + "." + outputType)
    dotexe = r"C:\Program Files (x86)\Graphviz2.38\bin\dot.exe"
    if not os.path.exists(dotexe):
        print "error: cannot find dot executable at '%s'" % dotexe
        sys.exit(1)
    print "converting: %s" % outfile
    command = [dotexe, "-Kdot", "-T%s" % outputType, os.path.basename(dotFile), "-o", outfile]
    proc = subprocess.Popen(command)
    #proc = subprocess.Popen(command, cwd=os.path.dirname(dotFile), stdout=subprocess.PIPE)
    _out, _err = proc.communicate()
    if _err:
        print _err
        sys.exit(1)