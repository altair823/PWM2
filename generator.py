from random import randint


LowerCase = {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'}
UpperCase = {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'}
SpecialChar = {'!', '@', '#', '$', '%', '&', '*'}
Num = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}
SimilarChar = {'i', 'I', 'l', 'L', '1', 'o', 'O', '0'}


class Generator:
    def __init__(self, pwDigit, isSpecialCharInclude=False, isUpperOnly=False, isLowerOnly=False, isNumInclude=True,
                 isSimilarNotInclude=True):
        self.pwDigit = pwDigit
        self.isSpecialCharInclude = isSpecialCharInclude
        self.isUpperOnly = isUpperOnly
        self.isLowerOnly = isLowerOnly
        if self.isUpperOnly is True and self.isLowerOnly is True:
            raise AttributeError('There is collision in options isUpperOnly and isLowerOnly.')
        self.isNumInclude = isNumInclude
        self.isSimilarNotInclude = isSimilarNotInclude

    def makePW(self):
        pool = set()
        if self.isSpecialCharInclude is True:
            pool = pool.union(SpecialChar)
        if self.isUpperOnly is False:
            pool = pool.union(LowerCase)
        if self.isLowerOnly is False:
            pool = pool.union(UpperCase)
        if self.isNumInclude is True:
            pool = pool.union(Num)
        if self.isSimilarNotInclude is True:
            pool = pool.difference(SimilarChar)

        result = []
        population = list(pool)
        for i in range(self.pwDigit):
            result.append(population[randint(0, len(population)-1)])

        return ''.join(result)
