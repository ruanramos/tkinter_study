elos = {"unranked": -1, "bronze 5": 0, "bronze 4": 1, "bronze 3": 2, "bronze 2": 3, "bronze 1": 4, "silver 5": 5,
        "silver 4": 6, "silver 3": 7, "silver 2": 8, "silver 1": 9, "gold 5": 10, "gold 4": 11,
        "gold 3": 12, "gold 2": 13, "gold 1": 14, "platinum 5": 15, "platinum 4": 16, "platinum 3": 17, "platinum 2": 18,
        "platinum 1": 19, "diamond 5": 20, "diamond 4": 21, "diamond 3": 22, "diamond 2": 23, "diamond 1": 24,
        "master": 25, "challenger": 26}


class Player:

    def __init__(self, name, nickname, elo, first_role, second_role):
        global registerNumber
        self.name = name
        self.nickname = nickname
        self.elo = elo
        self.eloNumber = elos[str(elo)]
        self.firstRole = first_role
        self.secondRole = second_role

    def show_infos(self):
        print("Name: " + str(self.name))
        print("Nickname: " + str(self.nickname))
        print("Elo: " + str(self.elo))
        print("First Role: " + str(self.firstRole))
        print("Second Role: " + str(self.secondRole))

    def get_infos(self):
        infos = [str(self.name), str(self.nickname), str(self.elo), str(self.firstRole), str(self.secondRole), str(self.regNumber)]
        return infos
