'''
사용자마다 다른 키를 생성하기 위한 키 생성기다.
TOTP_KEY는 반드시 사용자마다 반드시 달라야 하며
절대 유출되어서는 안된다. 키를 포함한 배포판은
이를 반드시 암호화 해야 한다.
'''

from pyotp import random_base32

TOTP_KEY = 'NP6HWRMEIOGDQ2VXPS3U7ZZXCTBUGS6O'


def generateKey():
    return random_base32()


if __name__ == '__main__':
    print(generateKey())