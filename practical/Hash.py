
def RSHash(s):
    a, b = 63689, 378511
    hash = 0
    for _ in s:
        hash = hash*a+ord(_)
        a = a*b
    return hash&0x7FFFFFF

def JSHash(s):
    hash = 1315423911
    for _ in s:
        hash = (hash << 5) + ord(_) + (hash >> 2)
    return hash&0x7FFFFFF

def PJWHash(s):
   BitsInUnsignedInt = 4 * 8
   ThreeQuarters     = int(BitsInUnsignedInt  * 3 / 4)
   OneEighth         = int(BitsInUnsignedInt / 8)
   HighBits          = (0xFFFFFFFF) << int(BitsInUnsignedInt - OneEighth)
   hash              = 0
   test              = 0

   for _ in s:
     hash = (hash << OneEighth) + ord(_)
     test = hash & HighBits
     if test != 0:
       hash = (( hash ^ (test >> ThreeQuarters)) & (~HighBits))
   return (hash & 0x7FFFFFFF)

def ELFHash(s):
    hash = 0
    x = 0
    for _ in s:
        hash = (hash<<4) + ord(_)
        x = hash&0xF000000
        if x != 0 :
            hash ^= x>>24
            hash &= ~x
    return hash&0x7FFFFFF


def BKDRHash(s):
    seed = 131 # 31 131 1313 13131 131313 ...
    hash = 0
    for _ in s:
      hash = (hash * seed) + ord(_)
    return (hash & 0x7FFFFFFF)


def SDBMHash(s):
    hash = 0
    for _ in s:
      hash = ord(_) + (hash << 6) + (hash << 16) - hash
    return (hash & 0x7FFFFFFF)


def DJBHash(s):
    hash = 5381
    for _ in s:
       hash = ((hash << 5) + hash) + ord(_)
    return (hash & 0x7FFFFFFF)


def DEKHash(s):
    hash = len(s);
    for i in s:
      hash = ((hash << 5) ^ (hash >> 27)) ^ ord(i)
    return (hash & 0x7FFFFFFF)


def APHash(s):
    hash = 0
    for k, i in enumerate(s):
      if ((k & 1) == 0):
        hash ^= ((hash <<  7) ^ ord(i) ^ (hash >> 3))
      else:
        hash ^= (~((hash << 11) ^ ord(i) ^ (hash >> 5)))
    return (hash & 0x7FFFFFFF)

if __name__ == '__main__':
    print(
    RSHash('abcdefghijklmnopqrstuvwxyz1234567890'))
    print(
    JSHash('abcdefghijklmnopqrstuvwxyz1234567890'))
    print(
    PJWHash('abcdefghijklmnopqrstuvwxyz1234567890'))
    print(
    ELFHash('abcdefghijklmnopqrstuvwxyz1234567890'))
    print(
    BKDRHash('abcdefghijklmnopqrstuvwxyz1234567890'))
    print(
    SDBMHash('abcdefghijklmnopqrstuvwxyz1234567890'))
    print(
    DJBHash('abcdefghijklmnopqrstuvwxyz1234567890'))
    print(
    DEKHash('abcdefghijklmnopqrstuvwxyz1234567890'))
    print(
    APHash('abcdefghijklmnopqrstuvwxyz1234567890'))