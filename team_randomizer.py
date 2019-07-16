import itertools as itt


class TeamRandomizer():

	maximumDifference = 10;
	playersPerTeam = 5
	eloAcceptance = 0.5

	def __init__(self, numberOfPlayersRegistred, sqlCursor):
		self.numberOfPlayersRegistred = numberOfPlayersRegistred
		self.sqlCursor = sqlCursor
		self.numberOfTeams = numberOfPlayersRegistred // self.__class__.playersPerTeam
		self.numberOfRemainingPlayers = numberOfPlayersRegistred % self.__class__.playersPerTeam

	def CreateListOfPlayers(self):
		self.sqlCursor.execute("SELECT * FROM players ORDER BY rand()")

		return self.sqlCursor.fetchall()



	def GetAverageEloSoloQueue(self):
		self.sqlCursor.execute("SELECT avg(elo_solo_number) FROM players")
		return self.sqlCursor.fetchone()[0]



	def GetAverageEloFlexQueue(self):
		self.sqlCursor.execute("SELECT avg(elo_flex_number) FROM players")
		return self.sqlCursor.fetchone()[0]



	# média de elo flex e solo se forem parecidos
	def CalculatePlayerAverageElo(self, playerSoloElo, playerFlexElo):
		if abs(playerSoloElo - playerFlexElo) <= self.__class__.maximumDifference:
			return (playerFlexElo + playerSoloElo) / 2
		else:
			return max(playerFlexElo, playerSoloElo)


	def GetPlayerElosIndex(self, player):
		return (player[4], player[6])


	def Calculate5PermutationAvarageElo(self, comb):
		total = 0
		for i in comb:
			elos = self.GetPlayerElosIndex(i)
			total += self.CalculatePlayerAverageElo(*elos)

		return total / self.__class__.playersPerTeam


	def WritePlayerToTxt(self, player, txt):
		for i in player:
			txt.write("{0} |  ".format(str(i)))
		txt.write('\n')


	def WritePlayerIdToTxt(self, player, txt):
		txt.write("{0} |  ".format(player[0]))
		txt.write('\n')


	def WritePermToTxt(self, comb, txt):
		for i in comb:
			self.WritePlayerIdToTxt(i, txt)
		txt.write('AvarageElo: {0}'.format(self.Calculate5PermutationAvarageElo(comb)))
		txt.write('\n----------------------------\n')


	def PrintTeam(self, team):
		for i in team:
			print('ID: {0}   |   Nickname: {1}   |   Elo Solo: {2}   |   Elo Flex: {3}  |  Role 1: {4}   |   Role 2: {5}'.format(i[0], i[2], i[3], i[5], i[7], i[8]))
		print("Team Avarage Elo: {0}".format(self.Calculate5PermutationAvarageElo(team)))


	def WriteTeamToFile(self, team, file):
		for i in team:
			file.write('ID: {0}   |   Name: {1}'.format(i[0], i[1]))
		file.write('\n')

	def NaiveRandomizer(self):
		formedTeams = []
		playersAllocated = set()

		averageSoloElo = self.GetAverageEloSoloQueue()
		averageFlexElo = self.GetAverageEloFlexQueue()

		a = open('test.txt', 'w+')

		averageElo = float((self.GetAverageEloFlexQueue() + self.GetAverageEloSoloQueue())) / 2		

		

		while(len(playersAllocated) < 170):

			comb = itt.combinations(self.CreateListOfPlayers(), self.__class__.playersPerTeam)
			# checks if the team in the combination has elo average and has no player already has team
			for team in comb:
				if abs(self.Calculate5PermutationAvarageElo(team) - averageElo) <= self.__class__.eloAcceptance:
					allNewPlayers = True
					for player in team:
						 if player[0] in playersAllocated:
						 	allNewPlayers = False
						 	break
					if allNewPlayers:
						formedTeams.append(team)
						for player in team:
							playersAllocated.add(player[0])
					else:
						break
				else:
					break
		266
		
		for i in formedTeams:
			self.PrintTeam(i)
			self.WriteTeamToFile(i, a)

		a.close()
		print("Players allocated: {0}\nPlayers Remaining: {1}\nTeams Formed: {2}\nRegistered Players Average Elo: {3}".format(len(playersAllocated), 206-len(playersAllocated), len(formedTeams), averageElo))
		

numberOfPlayersRegistred = 206

if __name__ == "__main__":
	randomizer = TeamRandomizer(numberOfPlayersRegistred)