#!/usr/bin/env python
import os

def findFiles(path, flist):
    """Find all files under the given path"""
    if os.path.isdir(path):
        fnames = [ os.path.join(path, p)
                   for p in os.listdir(path)
                   if not p.startswith('.') and p != u'extern']
        for fname in fnames:
            findFiles(fname, flist)
    elif path.endswith(u".py"):
        flist.append(path)

if __name__ == '__main__':
    # Generate the file list
    path = u"../../src/"
    cbrowser = u"../../plugins/codebrowser/codebrowser/"
    fbrowser = u"../../plugins/filebrowser/filebrowser/"
    launch = u"../../plugins/Launch/Launch/"
    pshell = u"../../plugins/PyShell/PyShell/"

    flist = list()
    for p in (path, cbrowser, fbrowser, launch, pshell):
        findFiles(p, flist)

    f = open(u'app.fil', 'wb')
    f.write("\n".join(flist))
    f.close()
