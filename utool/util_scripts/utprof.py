#!/usr/bin/env python2.7
"""
provides a python script interface into utprof.sh
"""
from __future__ import absolute_import, division, print_function
import os
import sys

if __name__ == '__main__':
    import utool as ut
    # Allow for -m to be specified on the command line
    modname = ut.get_argval('-m', help_='specify module name to profile')
    if modname is not None:
        modpath = ut.get_modpath_from_modname(modname)
        #print(modpath)
        argvx = sys.argv.index(modname) + 1
        argv = [modpath] + sys.argv[argvx:]
    else:
        argvx = sys.argv.index('utprof.py')
        argv = sys.argv[argvx:]
    cmd = 'utprof.sh ' + ' '.join(argv)
    print(cmd)
    os.system(cmd)