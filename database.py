from base64 import b64encode, b64decode
from json import dump, load
from os.path import isfile
from security.encryption import Encryption


class Database:
    def __init__(self, filename):
        self.filename = filename
        self.PWs = {}
        self.hashedPW = None
        self.salt = None
        self.crypto = Encryption()

    def verifyPW(self, inputPW):
        if self.salt is None:
            self.crypto.verifyPW(inputPW, self.hashedPW, self.salt, isCreateInitial=True)
            self.hashedPW = self.crypto.hashing(inputPW)
            self.salt = self.crypto.salt
        else:
            self.crypto.verifyPW(inputPW, self.hashedPW, self.salt, isCreateInitial=False)

    def loadFile(self):
        if isfile(self.filename) is False:
            print('There is no file named as ' + self.filename)
            raise FileNotFoundError
        with open(self.filename, 'r', encoding='utf-8') as dataFile:
            temp = load(dataFile)
            if 'HPW' in temp:
                self.hashedPW = temp['HPW']
            if 'SALT' in temp:
                self.salt = b64decode(temp['SALT'])
            if 'PW' in temp:
                self.PWs = temp['PW']

    def saveFile(self):
        with open(self.filename, 'w', encoding='utf-8') as dataFile:
            totalData = {'HPW': self.hashedPW, 'SALT': b64encode(self.salt).decode('utf-8'), 'PW': self.PWs}
            dump(totalData, dataFile, indent=4)

    def delSite(self, siteName):
        site = self.findSiteName(siteName)
        if site is not False:
            self.PWs.pop(site)
        else:
            raise AttributeError

    def delID(self, siteName, ID):
        temp = self.find(siteName, ID)
        site = temp['siteName']
        i = temp['ID']
        if site is not None and i is not None:
            self.PWs[site].pop(i)

    def addSite(self, siteName):
        if self.findSiteName(siteName) is False:
            encryptedSiteName = self.crypto.encryptPW(siteName)
            self.PWs[encryptedSiteName] = {}
        else:
            raise AttributeError

    def addID(self, siteName, ID):
        try:
            i = self.findSiteID(siteName, ID)
            if i is False:
                # 해당 아이디가 존재하지 않는다면 새로 저장.
                self.PWs[self.findSiteName(siteName)][self.crypto.encryptPW(ID)] = ''
            else:
                # 존재하지 않는다면 그냥 종료
                print('there is already existed id ' + ID + ' in database.')
                return
        except TypeError:
            raise

    def addPW(self, siteName, ID, PW):
        temp = self.find(siteName, ID)
        if temp['siteName'] is not None and temp['ID'] is not None:
            self.PWs[temp['siteName']][temp['ID']] = self.crypto.encryptPW(PW)
        else:
            raise AttributeError

    def findSiteName(self, siteName):
        for i in self.PWs:
            if self.crypto.decryptPW(i) == siteName:
                return i
        return False

    def findSiteID(self, siteName, ID):
        for i in self.PWs[self.findSiteName(siteName)]:
            if self.crypto.decryptPW(i) == ID:
                return i
        return False

    def find(self, siteName, ID):
        if self.findSiteName(siteName) is not False:
            if self.findSiteID(siteName, ID) is not False:
                return {'siteName': self.findSiteName(siteName), 'ID': self.findSiteID(siteName, ID)}
            else:
                return {'siteName': self.findSiteName(siteName), 'ID': None}
        return {'siteName': None, 'ID': None}

    def getSiteList(self):
        result = []
        for i in self.PWs:
            result.append(self.crypto.decryptPW(i))
        return result

    def getIDList(self, siteName):
        site = self.findSiteName(siteName)
        if site is not False:
            result = []
            for i in self.PWs[site]:
                result.append(self.crypto.decryptPW(i))
            return result
        else:
            raise AttributeError

    def getPW(self, siteName, ID):
        temp = self.find(siteName, ID)
        site = temp['siteName']
        i = temp['ID']
        if site is not None and i is not None:
            return self.crypto.decryptPW(self.PWs[site][i])
        else:
            raise AttributeError
