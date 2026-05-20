from enum import Enum

class HackedState(Enum):
    NORMAL = 0
    HACKED = 1

class Station:
    costList = None
    chanceList = None
    thresholdList = None
    creatureLevelList = None
    creatureTypeList = None

    def __init__(self, level, hackedState: HackedState):
        self.level = level
        self.hacked = hackedState
        self.cost = None
        self.chance = None
        self.threshold = None
        self.updateValues()

    def updateValues(self):
        hackedIndex = self.hacked.value
        levelIndex = self.level - 1

        self.cost = self.costList[hackedIndex][levelIndex]
        self.chance = self.chanceList[hackedIndex][levelIndex]
        self.threshold = self.thresholdList[hackedIndex][levelIndex]

class Grave(Station):
    costList = [[250, 300, 400, 500, 700], [250, 400, 400, 500, 1000]]
    chanceList = [
        [[1,0,0,0], [.6,.4,0,0], [.4,.3,.3,0], [.25,.25,.3,.2], [.1,.1,.4,.4]],
        [[1,0,0,0], [ 0, 1,0,0], [.4,.3,.3,0], [.25,.25,.3,.2], [ 0,.1, 0,.9]]
    ]
    thresholdList = [
        [[1,1,1,1], [.6, 1,1,1], [.4,.7, 1,1], [.25, .5,.8, 1], [.1,.2,.6, 1]],
        [[1,1,1,1], [ 0, 1,1,1], [.4,.7, 1,1], [.25, .5,.8, 1], [ 0,.1,.1, 1]]
    ]
    creatureLevelList = [-1, 0, -1, 0]
    creatureTypeList = ["Skeleton", "Skeleton", "Zombie", "Zombie"]

class Lectern(Station):
    costList = [[500, 750, 1000, 1250, 1500], [250, 1000, 400, 500, 2500]]
    chanceList = [
        [[.7,.3,0,0], [.4,.6,0,0], [.3,.5,.2,0], [.2,.4,.3,.1], [.1,.3,.4,.2]],
        [[.7,.3,0,0], [.1,.9,0,0], [.3,.5,.2,0], [.2,.4,.3,.1], [.1,.2,0,.7]]
    ]
    thresholdList = [
        [[.7,1,1,1], [.4,1,1,1], [.3,.8,1,1], [.2,.6,.9, 1], [.1,.4,.8,1]],
        [[.7,1,1,1], [.1,1,1,1], [.3,.8,1,1], [.2,.6,.9, 1], [.1,.3,.3,1]]
    ]
    creatureLevelList = [0, 0, -1, 0]
    creatureTypeList = ["Skeleton", "Shade", "Banshee", "Banshee"]

class Portal(Station):
    costList = [[500, 750, 1000, 1250, 1500], [250, 1000, 1750, 500, 2500]]
    chanceList = [
        [[.7, .3, 0, 0, 0], [.4, .6, 0, 0, 0], [.3, .4, .3, 0, 0], [.2, .3, .25, .25, 0], [.1, .2, .2, .3, .2]],
        [[.7, .3, 0, 0, 0], [.4, .6, 0, 0, 0], [.1, 0, .9, 0, 0], [.2, .3, .25, .25, 0], [.1, 0, .2, 0, .7]]
    ]
    thresholdList = [
        [[.7, 1, 1, 1, 1], [.4, 1, 1, 1, 1], [.3, .7, 1, 1, 1], [.2, .5, .75, 1, 1], [.1, .3, .5, .8, 1]],
        [[.7, 1, 1, 1, 1], [.4, 1, 1, 1, 1], [.1, .1, 1, 1, 1], [.2, .5, .75, 1, 1], [.1, .1, .3, .3, 1]]
    ]
    creatureLevelList = [0, -1, 0, -1, 0]
    creatureTypeList = ["Werewolf", "Imp", "Imp", "Demon", "Demon"]
