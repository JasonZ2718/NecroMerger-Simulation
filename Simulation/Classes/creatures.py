class Creature:
    name = None
    dmgList = None
    foodList = None
    imagePathList = None
    championList = None

    def __init__(self, level):
        self.level = level
        self.maxLv = None
        self.dmg = None
        self.food = None
        self.championPts = None
        self.imagePath = None
        self.updateValues()

    def updateValues(self):
        levelIndex = self.level + 1

        self.maxLv = len(self.championList) - 2
        self.dmg = self.dmgList[levelIndex]
        self.food = self.foodList[levelIndex]
        self.championPts = self.championList[levelIndex]
        self.imagePath = self.imagePathList[levelIndex]

    def __eq__(self, other):
        if type(self) == type(other) and self.level == other.level:
            return True
        else:
            return False

class Empty(Creature):
    name = "Empty"
    dmgList = [0,0]
    foodList = [0,0]
    championList = [0,0]
    imagePathList = [None, None]

class Skeleton(Creature):
    name = "Skeleton"
    dmgList = [0,0,5,10,25,50,100,225,500]
    foodList = [1,2,10,25,60,140,300,700,1500]
    championList = [0,0,1000,1200,1500,2000,2500,3000,4000]
    imagePathList = ["Images/Skeleton/" + str(i) + ".png" for i in range(-1, 8)]

class Zombie(Creature):
    name = "Zombie"
    dmgList = [0,0,10,25,50,125,300,700]
    foodList = [1,2,30,75,175,400,1000,2500]
    championList = [0,0,3000,3500,4000,4500,5000,6000]
    imagePathList = ["Images/Zombie/" + str(i) + ".png" for i in range(-1, 7)]

class Werewolf(Creature):
    name = "Werewolf"
    dmgList = [0, 0, 25, 60, 150, 400, 1000]
    foodList = [1, 2, 20, 50, 125, 300, 700]
    championList = [0, 0, 1750, 2000, 2500, 3000, 4000]
    imagePathList = ["Images/Werewolf/" + str(i) + ".png" for i in range(-1, 6)]

class Shade(Creature):
    name = "Shade"
    dmgList = [0, 0, 0, 0, 0, 0]
    foodList = [0, 1, 0, 0, 0, 0]
    championList = [0, 0, 1500, 2000, 2500, 3000]
    imagePathList = [None] + ["Images/Shade/" + str(i) + ".png" for i in range(0, 5)]

class Banshee(Creature):
    name = "Banshee"
    dmgList = [0, 0, 125, 300, 750, 1750]
    foodList = [1, 2, 150, 400, 1000, 2500]
    championList = [0, 0, 1500, 2000, 2500, 3000]
    imagePathList = ["Images/Banshee/" + str(i) + ".png" for i in range(-1, 5)]

class Imp(Creature):
    name = "Imp"
    dmgList = [0, 0, 0, 0, 0, 0]
    foodList = [1, 2, 150, 350, 900, 2000]
    championList = [0, 0, 1300, 1600, 1900, 2200]
    imagePathList = ["Images/Imp/" + str(i) + ".png" for i in range(-1, 5)]

class Demon(Creature):
    name = "Demon"
    dmgList = [0, 0, 500, 1250, 3500]
    foodList = [1, 2, 250, 600, 1500]
    championList = [0, 0, 1300, 1600, 1900]
    imagePathList = ["Images/Demon/" + str(i) + ".png" for i in range(-1, 4)]