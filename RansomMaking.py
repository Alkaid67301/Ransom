from Crypto.Cipher import AES
from Crypto.Hash import SHA256 as sha
import os

ksize = 1024

class myAES():
    def __init__(self, keytext, ivtext):
        hash = sha.new()
        hash.update(keytext.encode('utf-8'))
        key = hash.digest()
        self.key = key[:16]

        hash.update(ivtext.encode('utf-8'))
        iv = hash.digest()
        self.iv = iv[:16]

    def makeEncInfo(self, filename):
        fillersize = 0
        filesize = os.path.getsize(filename)
        if filesize % 16 != 0:
            fillersize = 16 - filesize % 16

        filler = '0'*fillersize
        header = ' %d' %(fillersizie)
        gap = 16 - len(header)
        header += '#' * gap

        return header, filler

    def enc(self, filename):
        endfilename = filename + '.sasya'
        header, filler = self.makeEncInfo(filename)
        aes = AES.new(self.key, AES.MODE_CBC, self.iv)

        h = open(filename, 'rb')
        hh = open(encfilename, 'wb+')
        
