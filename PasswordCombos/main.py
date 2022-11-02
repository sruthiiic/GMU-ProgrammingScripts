import itertools

from itertools import permutations

f = open("wordlist.txt", "w")


def allCases(stringName):
    return list(map(''.join, itertools.product(*zip(stringName.upper(), stringName.lower()))))


def writePasswordCombos(firstList, secondList):
    for a in firstList:
        for b in secondList:
            if a.isupper() and b.isupper():
                continue
            lst1 = list(permutations([z, t, a, b]))
            for i in lst1:
                s = ''.join(i)
                s += "\n"
                f.write(s)


z, t = "22", "20"


writePasswordCombos(allCases("cyse"), allCases("mason"))
writePasswordCombos(allCases("gmu"), allCases("mason"))
writePasswordCombos(allCases("gmu"), allCases("cyse"))

# Any combination of the following password hints:
# -Two of the three words: GMU, MASON, CYSE
# -Always have these numbers: 20, 22
# This includes upper-case and lower-case permutations (ex. cYse, MASon, Gmu)
# No special characters

