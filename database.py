from json import dump, load
from os.path import isfile


class Database:
    def __init__(self, filename):
        self.filename = filename
        self.PWs = {}
        self.hashedPW = None
        self.salt = None

    def loadFile(self):
        if isfile(self.filename) is False:
            print('There is no file named as ' + self.filename)
            raise FileNotFoundError
        with open(self.filename, 'r', encoding='utf-8') as dataFile:
            temp = load(dataFile)
            if 'HPW' in temp:
                self.hashedPW = temp['HPW']
            if 'SALT' in temp:
                self.salt = temp['SALT']
            if 'PW' in temp:
                self.PWs = temp['PW']

    def saveFile(self):
        with open(self.filename, 'w', encoding='utf-8') as dataFile:
            dump(self.PWs, dataFile, indent=4)

    def delSite(self, encryptedSiteName):
        if encryptedSiteName in self.PWs:
            self.PWs.pop(encryptedSiteName)
