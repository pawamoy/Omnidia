def hashfile(afile, hasher, blocksize=65536):
    buf = afile.read(blocksize)
    while len(buf) > 0:
        hasher.update(buf)
        buf = afile.read(blocksize)
    return hasher.digest()

# [(fname, hashfile(open(fname, 'rb'), hashlib.sha256()))
#  for fname in fnamelst]


