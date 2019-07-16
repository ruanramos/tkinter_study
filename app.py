from tkinter import *
import player_class
from functools import partial
import mysql.connector
import collections
import csv
import team_randomizer
import time
start_time = time.time()



class Application:
    def __init__(self, master=None):
        self.fonte = ("Verdana", "15")
  
        self.container1 = Frame(master)
        self.container1["pady"] = 10
        self.container1.pack()
        self.container2 = Frame(master)
        self.container2["padx"] = 20
        self.container2["pady"] = 5
        self.container2.pack()
        self.container3 = Frame(master)
        self.container3["padx"] = 20
        self.container3["pady"] = 5
        self.container3.pack()
        self.container4 = Frame(master)
        self.container4["padx"] = 20
        self.container4["pady"] = 5
        self.container4.pack()
        self.container5 = Frame(master)
        self.container5["padx"] = 20
        self.container5["pady"] = 5
        self.container5.pack()
        self.container6 = Frame(master)
        self.container6["padx"] = 20
        self.container6["pady"] = 5
        self.container6.pack()
        self.container7 = Frame(master)
        self.container7["padx"] = 20
        self.container7["pady"] = 5
        self.container7.pack()
        self.container8 = Frame(master)
        self.container8["padx"] = 20
        self.container8["pady"] = 10
        self.container8.pack()
        self.container9 = Frame(master)
        self.container9["pady"] = 15
        self.container9.pack()
  
        self.titulo = Label(self.container1, text="Informe os dados :")
        self.titulo["font"] = ("Calibri", "9", "bold")
        self.titulo.pack ()
  
        self.btnBuscar = Button(self.container2, text="Buscar", font=self.fonte, width=10)
        #self.btnBuscar["command"] = self.buscarUsuario
        self.btnBuscar.pack(side=RIGHT)
  
        self.bntInsert = Button(self.container8, text="Inserir", font=self.fonte, width=12)
        #self.bntInsert["command"] = self.inserirUsuario
        self.bntInsert.pack (side=LEFT)
  
        self.bntAlterar = Button(self.container8, text="Alterar", font=self.fonte, width=12)
        #self.bntAlterar["command"] = self.alterarUsuario
        self.bntAlterar.pack (side=LEFT)
  
        self.bntExcluir = Button(self.container8, text="Excluir", font=self.fonte, width=12)
        #self.bntExcluir["command"] = self.excluirUsuario
        self.bntExcluir.pack(side=LEFT)
  
        self.lblmsg = Label(self.container9, text="")
        self.lblmsg["font"] = ("Verdana", "9", "italic")
        self.lblmsg.pack()

"""Trying to create the connection to my db"""
mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="tICfQTeWoG1",
        database="lol_ufrj_draft_application"
    )

myCursor = mydb.cursor()
myCursor.execute("SELECT * FROM players")
my_results = myCursor.fetchall()


#with open('SalesJan2009.csv') as csvfile:
    #readCSV = csv.reader(csvfile, delimiter = ',')
    #for row in readCSV:
        


#Query to add the opgg link to the database
#link = 'http://br.op.gg/summoner/userName='
"""
for i in my_results:
    fullSql = "UPDATE players SET op_gg_link = \'{0}{1}\' WHERE id = {2}".format(link, str.lower((i[2]).replace(' ', '+')), i[0])
    print(fullSql)
    myCursor.execute(fullSql)

    mydb.commit()
"""

#a = team_randomizer.TeamRandomizer(10, myCursor).GetMediumEloFlexQueue()
#b = team_randomizer.TeamRandomizer(10, myCursor).GetMediumEloSoloQueue()
#c = team_randomizer.TeamRandomizer(10, myCursor).test()

a = team_randomizer.TeamRandomizer(10, myCursor).NaiveRandomizer()

print("--- %s seconds ---" % (time.time() - start_time))
root = Tk()
Application(root)

root.mainloop()
