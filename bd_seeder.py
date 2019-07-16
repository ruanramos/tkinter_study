import string
import random
import mysql.connector

elos = {"unranked": -1, "bronze 5": 0, "bronze 4": 1, "bronze 3": 2, "bronze 2": 3, "bronze 1": 4, "silver 5": 5,
        "silver 4": 6, "silver 3": 7, "silver 2": 8, "silver 1": 9, "gold 5": 10, "gold 4": 11,
        "gold 3": 12, "gold 2": 13, "gold 1": 14, "platinum 5": 15, "platinum 4": 16, "platinum 3": 17, "platinum 2": 18,
        "platinum 1": 19, "diamond 5": 20, "diamond 4": 21, "diamond 3": 22, "diamond 2": 23, "diamond 1": 24,
        "master": 25, "challenger": 26}

elos_inverted = {v: k for k, v in elos.items()}

class Seeder():

	def __init__(self, numberOfEntries = None):
		self.numberOfEntries = numberOfEntries
	
	def GetNamesFromFile(self):
		textFile = open('/home/ruanramos/Dropbox/Codes and Projects/TkInter LoL UFRJ DB/'\
			'tkinter_study/random_names.txt', 'r')
		names = textFile.readlines()
		textFile.close()
		return names


	def GetNicknamesFromFile(self):
		textFile = open('/home/ruanramos/Dropbox/Codes and Projects/TkInter LoL UFRJ DB/'\
			'tkinter_study/random_nicknames.txt', 'r')
		nicknames = textFile.readlines()
		textFile.close()
		return nicknames


	def GetRandomElo(self):
		rndNum = random.randint(-1, 26)
		return elos_inverted[rndNum]

	def GetEloNumber(self, elo):
		return elos[elo]

	def GetRandomRole(self):
		roles = ["Top Laner", "Jungler", "Mid Laner", "Adc or BottomCarry", "Support"]
		return roles[random.randint(0, 4)]


def seed():
		mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="tICfQTeWoG1",
        database="lol_ufrj_draft_application"
	    )
		seeder = Seeder(200)
		myCursor = mydb.cursor()
		names = seeder.GetNamesFromFile()
		nicknames = seeder.GetNicknamesFromFile()
		for i in range(1, 7):
			elo = seeder.GetRandomElo()
			eloNumber = seeder.GetEloNumber(elo)
			#role1 = seeder.GetRandomRole()
			#role2 = seeder.GetRandomRole()
			#opggLink = 'http://br.op.gg/summoner/userName={0}'.format(str.lower(nicknames[i].strip().replace(' ', '+')))
			querry = "UPDATE players SET elo_flex = '{0}', elo_flex_number = {1} WHERE id = {2}".format(elo, eloNumber, i)

			print(querry, "_____________________________________________")

			myCursor.execute(querry)

		mydb.commit()
		#descobrir o que tá rolando de errado na minha querry aqui....


if __name__ == "__main__":
	seed()
	print("FINISHED SEEDING")