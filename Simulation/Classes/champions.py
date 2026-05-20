class Champion:
    name = None
    spawnPoints = None
    contributors = []

    def __init__(self):
        self.points = 0

# contributors are ordered from fewest to most points
class Peasant(Champion):
    name = "Peasant"
    spawnPoints = 150000
    contributors = ["Skeleton", "Zombie", "Mummy"]

class Paladin(Champion):
    name = "Paladin"
    spawnPoints = 200000
    contributors = ["Ghoul", "Imp", "Banshee"]

class Rival(Champion):
    name = "Rival"
    spawnPoints = 100000
    contributors = ["Abomination", "Demon", "Golden Goose"]

