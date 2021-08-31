from pyotp import random_base32

TOTP_KEY = 'NP6HWRMEIOGDQ2VXPS3U7ZZXCTBUGS6O'


def generateKey():
    return random_base32()


if __name__ == '__main__':
    print(generateKey())