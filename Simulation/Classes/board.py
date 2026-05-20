from Simulation.Classes import creatures as c, stations as s, champions as ch
import numpy as np
import random as rand
import collections
import copy

CREATURES = {"Empty": c.Empty, "Skeleton": c.Skeleton, "Zombie": c.Zombie,
             "Werewolf": c.Werewolf, "Shade": c.Shade, "Banshee": c.Banshee,
             "Imp": c.Imp, "Demon": c.Demon}

class Board:
    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.size = rows * columns
        self.contents = list(c.Empty(0) for i in range(self.size))
        self.championList = [ch.Peasant(), ch.Paladin(), ch.Rival()]

    def generate(self, station: s.Station):
        num = rand.random()

        for value in station.threshold:
            if num <= value:
                index = station.threshold.index(value)
                spawn = CREATURES[station.creatureTypeList[index]](station.creatureLevelList[index])
                position = self.contents.index(c.Empty(0))
                self.contents[position] = spawn
                break

    def strContents(self):
        contents = []
        for i in range(self.size):
            string = self.contents[i].name + "." + str(self.contents[i].level)
            contents.append(string)
        return contents

    def listContents(self):
        contents = []
        for i in range(self.size):
            list = [self.contents[i].name, self.contents[i].level]
            contents.append(list)
        return contents

    def nameContents(self):
        contents = []
        for i in range(self.size):
            name = self.contents[i].name
            contents.append(name)
        return contents

    # returns a counter of all creatures
    def info(self):
        info = collections.Counter(self.strContents())
        return info

    def reset(self):
        self.contents = list(c.Empty(0) for i in range(self.size))
        for champion in self.championList:
            champion.points = 0

    def mergeOnce(self):
        # discards any max lv creatures
        for i in range(len(self.contents)):
            if self.contents[i].level == self.contents[i].maxLv and self.contents[i] != c.Empty(0):
                self.contents[i] = c.Empty(0)

        mergedOnce = False
        # -1 means that last creature on board doesn't need to be checked
        for index in range(self.size-1):
            creature1 = self.contents[index]
            if creature1 == c.Empty(0):
                continue

            for loopIndex in range(index+1, self.size):
                creature2 = self.contents[loopIndex]
                if creature2 == c.Empty(0):
                    continue

                if creature1 == creature2:
                    spawn = CREATURES.get(creature1.name)(creature1.level+1)
                    self.contents[index] = spawn
                    self.contents[loopIndex] = c.Empty(0)

                    for champion in self.championList:
                        if spawn.name in champion.contributors:
                            champion.points += spawn.championPts
                            # print(champion.points)

                    mergedOnce = True
                    break

            if mergedOnce:
                break

    def mergeContinuous(self):
        canMerge = True
        while canMerge:
            previousContents = self.contents.copy()
            self.mergeOnce()
            #print(self.strContents())
            if all([a == b for a, b in zip(previousContents, self.contents)]):
                canMerge = False

    def indexHighestLv(self, name):
        sortedList = sorted(self.listContents())
        truncatedList = [list for list in sortedList if name in list]
        highestLv = truncatedList[-1][1]
        index = self.listContents().index([name, highestLv])
        return index

    def indexLowestLv(self, name):
        sortedList = sorted(self.listContents())
        truncatedList = [list for list in sortedList if name in list]
        lowestLv = truncatedList[0][1]
        index = self.listContents().index([name, lowestLv])
        return index

    def lowestLv(self, name):
        sortedList = sorted(self.listContents())
        truncatedList = [list for list in sortedList if name in list]
        lowestLv = truncatedList[0][1]
        return lowestLv

    # for both merge methods, discards creature if it attains max lv or if it doesn't contribute points to champion
    # merge method 1: ONE CREATURE TYPE: discards highest lv creature if board cannot be merged.
    #                 TWO CREATURE TYPES: discards highest lv creature of type that contributes fewer points
    def numChampHighDiscard(self, station: s.Station, resource, champion: ch.Champion):
        # nonCommonCreatures is a set of names
        nonCommonCreatures = set(station.creatureTypeList).difference(set(champion.contributors))

        maxCount = int(np.floor(resource/station.cost))
        count = 0
        while count < maxCount:
            # generates until board is full
            while c.Empty(0) in self.contents:
                self.generate(station)
                count += 1
                # print(self.strContents(), count)
                if count == maxCount:
                    break

            self.mergeContinuous()

            # no longer able to merge
            if c.Empty(0) not in self.contents:
                # finds name of lowest contributing creature currently on the board
                lowestName = None
                index = 100
                for name in set(self.nameContents()):
                    if name in champion.contributors:
                        # champion.contributors is ordered from fewest to most points
                        if champion.contributors.index(name) < index:
                            index = champion.contributors.index(name)
                            lowestName = champion.contributors[index]

                # discards any noncontributing creatures
                currentNonContrCr = set(self.nameContents()).intersection(nonCommonCreatures)
                if currentNonContrCr != set():
                    index = self.indexLowestLv(list(currentNonContrCr)[0])
                    self.contents[index] = c.Empty(0)
                    #print("discard non contr")
                # discards highest lv creature of type that contributes fewer points
                else:
                    highestIndex = self.indexHighestLv(lowestName)
                    self.contents[highestIndex] = c.Empty(0)
                    #print("discard high")
                # print(self.strContents())

        # checks points of inputted champion
        for i in range(len(self.championList)):
            if champion.name == self.championList[i].name:
                return self.championList[i].points / self.championList[i].spawnPoints

    # merge method 2: ONE CREATURE TYPE: if board cannot be merged, discards the lowest lv creature if the station has a chance of
    #                 generating a higher lv creature. Otherwise, discards highest lv creature
    #                 TWO CREATURE TYPES: discards highest lv creature of type that contributes fewer points
    def numChampLowDiscard(self, station: s.Station, resource, champion: ch.Champion):
        # nonCommonCreatures is a set of names
        nonCommonCreatures = set(station.creatureTypeList).difference(set(champion.contributors))

        maxCount = int(np.floor(resource / station.cost))
        count = 0
        while count < maxCount:
            # generates until board is full
            while c.Empty(0) in self.contents:
                self.generate(station)
                count += 1
                # print(self.strContents(), count)
                if count == maxCount:
                    break

            self.mergeContinuous()

            # no longer able to merge
            if c.Empty(0) not in self.contents:
                # finds name of lowest contributing creature currently on the board
                lowestName = None
                index = 100
                for name in set(self.nameContents()):
                    if name in champion.contributors:
                        # champion.contributors is ordered from fewest to most points
                        if champion.contributors.index(name) < index:
                            index = champion.contributors.index(name)
                            lowestName = champion.contributors[index]

                # discards any noncontributing creatures
                currentNonContrCr = set(self.nameContents()).intersection(nonCommonCreatures)
                if currentNonContrCr != set():
                    index = self.indexLowestLv(list(currentNonContrCr)[0])
                    self.contents[index] = c.Empty(0)
                    #print("discard non contr")

                # two creature case: discards highest lv creature of type that contributes fewer points
                elif len(list(set(self.nameContents()))) > 1:
                    highestIndex = self.indexHighestLv(lowestName)
                    self.contents[highestIndex] = c.Empty(0)
                    #print("discard low")
                # one creature case
                else:
                    lowestIndex = self.indexLowestLv(lowestName)
                    lowestLvCr = self.contents[lowestIndex].level
                    # gets lv0 index of relevant creature from station's lists
                    lv0Index = [i for i in range(len(station.creatureTypeList)) if
                                         station.creatureTypeList[i] == lowestName and station.creatureLevelList[i] == 0][0]

                    # checks if station can produce a higher lv creature than current lowest lv creature --> discards
                    # lowest lv creature if merge is possible
                    if lowestLvCr == -1 and CREATURES[lowestName](0) in self.contents and station.chance[lv0Index] > 0 :
                        self.contents[lowestIndex] = c.Empty(0)
                        #print("discard -1")
                    # discards highest lv creature
                    else:
                        highestIndex = self.indexHighestLv(lowestName)
                        self.contents[highestIndex] = c.Empty(0)
                        #print("discard high")

                #print(self.strContents())

        # checks points of inputted champion
        for i in range(len(self.championList)):
            if champion.name == self.championList[i].name:
                return self.championList[i].points / self.championList[i].spawnPoints

    def highDiscardSim(self, station: s.Station, resource, champion: ch.Champion):
        # nonCommonCreatures is a set of names
        nonCommonCreatures = set(station.creatureTypeList).difference(set(champion.contributors))

        resourceLeft = resource
        maxCount = int(np.floor(resource/station.cost))
        count = 0
        while count < maxCount:
            # generates until board is full
            while c.Empty(0) in self.contents:
                self.generate(station)
                resourceLeft -= station.cost
                count += 1
                yield [copy.deepcopy(self.contents), copy.deepcopy(self.championList), resourceLeft]
                if count == maxCount:
                    break

            canMerge = True
            while canMerge:
                # discards any max lv creatures
                for i in range(len(self.contents)):
                    if self.contents[i].level == self.contents[i].maxLv and self.contents[i] != c.Empty(0):
                        self.contents[i] = c.Empty(0)
                        yield [copy.deepcopy(self.contents), copy.deepcopy(self.championList), resourceLeft]
                        continue
                previousContents = self.contents.copy()
                self.mergeOnce()
                yield [copy.deepcopy(self.contents), copy.deepcopy(self.championList), resourceLeft]
                if self.contents == previousContents:
                    canMerge = False

            # no longer able to merge
            if c.Empty(0) not in self.contents:
                # finds name of lowest contributing creature currently on the board
                lowestName = None
                index = 100
                for name in set(self.nameContents()):
                    if name in champion.contributors:
                        # champion.contributors is ordered from fewest to most points
                        if champion.contributors.index(name) < index:
                            index = champion.contributors.index(name)
                            lowestName = champion.contributors[index]

                # discards any noncontributing creatures
                currentNonContrCr = set(self.nameContents()).intersection(nonCommonCreatures)
                if currentNonContrCr != set():
                    index = self.indexLowestLv(list(currentNonContrCr)[0])
                    self.contents[index] = c.Empty(0)
                    yield [copy.deepcopy(self.contents), copy.deepcopy(self.championList), resourceLeft]
                # discards highest lv creature of type that contributes fewer points
                else:
                    highestIndex = self.indexHighestLv(lowestName)
                    self.contents[highestIndex] = c.Empty(0)
                    yield [copy.deepcopy(self.contents), copy.deepcopy(self.championList), resourceLeft]

    def lowDiscardSim(self, station: s.Station, resource, champion: ch.Champion):
        # nonCommonCreatures is a set of names
        nonCommonCreatures = set(station.creatureTypeList).difference(set(champion.contributors))

        resourceLeft = resource
        maxCount = int(np.floor(resource / station.cost))
        count = 0
        while count < maxCount:
            # generates until board is full
            while c.Empty(0) in self.contents:
                self.generate(station)
                resourceLeft -= station.cost
                count += 1
                yield [copy.deepcopy(self.contents), copy.deepcopy(self.championList), resourceLeft]
                if count == maxCount:
                    break

            canMerge = True
            while canMerge:
                # discards any max lv creatures
                for i in range(len(self.contents)):
                    if self.contents[i].level == self.contents[i].maxLv and self.contents[i] != c.Empty(0):
                        self.contents[i] = c.Empty(0)
                        yield [copy.deepcopy(self.contents), copy.deepcopy(self.championList), resourceLeft]
                        continue
                previousContents = self.contents.copy()
                self.mergeOnce()
                yield [copy.deepcopy(self.contents), copy.deepcopy(self.championList), resourceLeft]
                if self.contents == previousContents:
                    canMerge = False

            # no longer able to merge
            if c.Empty(0) not in self.contents:
                # finds name of lowest contributing creature currently on the board
                lowestName = None
                index = 100
                for name in set(self.nameContents()):
                    if name in champion.contributors:
                        # champion.contributors is ordered from fewest to most points
                        if champion.contributors.index(name) < index:
                            index = champion.contributors.index(name)
                            lowestName = champion.contributors[index]

                # discards any noncontributing creatures
                currentNonContrCr = set(self.nameContents()).intersection(nonCommonCreatures)
                if currentNonContrCr != set():
                    index = self.indexLowestLv(list(currentNonContrCr)[0])
                    self.contents[index] = c.Empty(0)
                    yield [copy.deepcopy(self.contents), copy.deepcopy(self.championList), resourceLeft]

                # two creature case: discards highest lv creature of type that contributes fewer points
                elif len(list(set(self.nameContents()))) > 1:
                    highestIndex = self.indexHighestLv(lowestName)
                    self.contents[highestIndex] = c.Empty(0)
                    yield [copy.deepcopy(self.contents), copy.deepcopy(self.championList), resourceLeft]
                # one creature case
                else:
                    lowestIndex = self.indexLowestLv(lowestName)
                    lowestLvCr = self.contents[lowestIndex].level
                    # gets lv0 index of relevant creature from station's lists
                    lv0Index = [i for i in range(len(station.creatureTypeList)) if
                                station.creatureTypeList[i] == lowestName and station.creatureLevelList[i] == 0][0]

                    # checks if station can produce a higher lv creature than current lowest lv creature --> discards
                    # lowest lv creature if merge is possible
                    if lowestLvCr == -1 and CREATURES[lowestName](0) in self.contents and station.chance[lv0Index] > 0 :
                        self.contents[lowestIndex] = c.Empty(0)
                        yield [copy.deepcopy(self.contents), copy.deepcopy(self.championList), resourceLeft]
                    # discards highest lv creature
                    else:
                        highestIndex = self.indexHighestLv(lowestName)
                        self.contents[highestIndex] = c.Empty(0)
                        yield [copy.deepcopy(self.contents), copy.deepcopy(self.championList), resourceLeft]