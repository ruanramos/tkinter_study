from tkinter import *
import player_class
from functools import partial
import mysql.connector
import tkinter.font
import collections

"""Creating a structure for return of a frame and buttons on menu for function create_frame()"""
Frame_Buttons = collections.namedtuple('Frame_Buttons', ['frame', 'list_alpha_button', 'list_register_button',
                                                         'update_button', 'add_button', 'delete_button'])


def create_frame():
    """Creating Frame"""
    frame = Frame(window)

    if not state == "add":
        frame["bg"] = "black"
    if not state == "main_menu":
        frame["padx"] = 20
        frame["pady"] = 20
    else:
        frame["pady"] = 100
    # Creating my font for buttons
    button_font = tkinter.font.Font(family='Arial', size=10)

    listPlayersAlphabeticalButton = Button(frame, text="List Players By Alphabetical Order", bd=5, bg="skyblue1", font=button_font)
    listPlayersAlphabeticalButton["command"] = partial(create_list_names_radiobuttons, 1)
    listPlayersAlphabeticalButton.pack(side=TOP, fill=X, padx=10, pady=10)
    listPlayersRegisterButton = Button(frame, text="List Players By Register Order", bd=5, bg="skyblue1", font=button_font)
    listPlayersRegisterButton["command"] = partial(create_list_names_radiobuttons, 0)
    listPlayersRegisterButton.pack(side=TOP, fill=X, padx=10, pady=10)

    add_player_button_var = Button(frame, text="Add A New Player", bd=5, bg="plum1", command=add_player_button, font=button_font)
    add_player_button_var.pack(side=BOTTOM, fill=X, padx=10, pady=8)

    if state == "add" or state == "menu":
        add_player_button_var.pack_forget()
        listPlayersAlphabeticalButton.pack_forget()
        listPlayersRegisterButton.pack_forget()
        listPlayersAlphabeticalButton.pack(side=BOTTOM, pady=0)
        listPlayersRegisterButton.pack(side=BOTTOM, pady=20)

    createdFrames.append(frame)
    frame.pack()
    result = Frame_Buttons(frame, listPlayersAlphabeticalButton, listPlayersRegisterButton, None,
                           add_player_button_var, None)
    return result


elos = {"unranked": -1, "bronze 5": 0, "bronze 4": 1, "bronze 3": 2, "bronze 2": 3, "bronze 1": 4, "silver 5": 5,
        "silver 4": 6, "silver 3": 7, "silver 2": 8, "silver 1": 9, "gold 5": 10, "gold 4": 11,
        "gold 3": 12, "gold 2": 13, "gold 1": 14, "platinum 5": 15, "platinum 4": 16, "platinum 3": 17, "platinum 2": 18,
        "platinum 1": 19, "diamond 5": 20, "diamond 4": 21, "diamond 3": 22, "diamond 2": 23, "diamond 1": 24,
        "master": 25, "challenger": 26}

"""Trying to create the connection to my db"""
mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="tICfQTeWoG1",
        database="lol_ufrj_draft_application"
    )
myCursor = mydb.cursor()

window = Tk()
window["bg"] = "black"
window.title("League of Legends Draft Platform")

# Gets the requested values of the height and width.
windowWidth = window.winfo_reqwidth()
windowHeight = window.winfo_reqheight()

# Gets both half the screen width/height and window width/height
positionRight = int(window.winfo_screenwidth() / 4 - windowWidth / 2)
positionDown = int(window.winfo_screenheight() / 5 - windowHeight / 2)

# Positions the window in the center of the page.
window.geometry("1000x700+{}+{}".format(positionRight, positionDown))

# Not needed after BD was implemented
"""
registeredPlayers = []
"""
state = "main_menu"
sub_title = Label(window, bg="black", fg="white", font="Helvetica, 16", anchor=W, justify=LEFT)


def save_player(variable1, variable2, variable3, main_frame):
    global state
    """Get the entries that were typed by the user"""
    name = main_frame.children["!entry"].get()
    nickname = main_frame.children["!entry2"].get()
    elo = variable1.get()
    elo_number = elos[str(elo)]
    first_role = variable2.get()
    second_role = variable3.get()

    # Not needed anymore
    """
    "Instantiate the player object"
    player = player_class.Player(name, nickname, elo, first_role, second_role)
    
    "Save the player object to the global list"
    registeredPlayers.append(player)
    """
    # Checking if already registered
    sql2 = "SELECT nickname FROM players"
    myCursor.execute(sql2)
    result = myCursor.fetchall()
    # Check if anything was typed
    if len(name) == 0 or len(nickname) == 0:
        msg = Message(createdFrames[-1], text="Error, no name or nickname typed")
        msg.pack()
        return
    # Check if nickname is repeated
    for i in result:
        if i[0].lower() == nickname.lower():
            msg = Message(createdFrames[-1], text="Error, nickname already registered")
            msg.pack()
            return

    """Create the tuple with the player infos, so we can insert into db table"""
    player_tuple = (name, nickname, elo, elo_number, first_role, second_role)

    """Insert player into db players table and commit change"""
    sql = "INSERT INTO players(name, nickname, elo, elo_number, first_role," \
          " second_role) VALUES (%s, %s, %s, %s, %s, %s)"
    myCursor.execute(sql, player_tuple)
    mydb.commit()

    """Resets the screen"""
    sub_title.pack_forget()
    state = "menu"
    createdFrames.remove(main_frame)
    main_frame.destroy()
    add_player_button()


def update_player_to_db(variable1, variable2, variable3, main_frame, id_player):
    global state
    """Get the entries that were typed by the user"""
    name = main_frame.children["!entry"].get()
    nickname = main_frame.children["!entry2"].get()
    elo = variable1.get()
    elo_number = elos[str(elo)]
    first_role = variable2.get()
    second_role = variable3.get()

    """Create the tuple with the player infos, so we can insert into db table"""
    player_tuple = (name, nickname, elo, elo_number, first_role, second_role, id_player)

    """Insert player into db players table and commit change"""
    sql = "UPDATE players SET name = %s, nickname = %s, elo = %s, elo_number = %s," \
          " first_role = %s, second_role = %s WHERE id = %s"
    myCursor.execute(sql, player_tuple)
    mydb.commit()

    """Resets the screen"""
    sub_title.pack_forget()
    state = "menu"
    createdFrames.remove(main_frame)
    main_frame.destroy()
    create_list_names_radiobuttons(0)
def get_name_from_player(player):
    """Function we will use to sort the players on alphabetical order"""
    return player.name.lower()


def get_elo_from_player(player):
    """Function we will use to sort the players on elo order"""
    return player.elo.lower()


def get_first_role_from_player(player):
    """Function we will use to sort the players on main role order"""
    return player.firstRole.lower()


def sort_players_by_name():
    return sorted(registeredPlayers, key=get_name_from_player)


def sort_players_by_elo():
    return sorted(registeredPlayers, key=get_elo_from_player)


def sort_players_by_first_role():
    return sorted(registeredPlayers, key=get_first_role_from_player())


# This function is unused since I created the radio button funcion
def list_players_alphabetical_button():
    """Function called when we click on the list players by alphabetical order button"""
    global state
    if not state == "list_alphabetical":
        """Changing state and subtitle and showing on screen"""
        state = "list_alphabetical"
        sub_title["text"] = "LIST OF PLAYERS"
        sub_title.pack()

        clear_frames()

        """Creating a new frame for showing the widgets"""
        list_frame = Frame(window)
        list_frame["padx"] = 30
        list_frame["pady"] = 30
        createdFrames.append(list_frame)
        list_frame.pack()

        """Creating the labels to show the info on screen"""
        lb_number = Label(list_frame, text="REGISTER NUMBER")
        lb_name = Label(list_frame, text="NAME")
        lb_nickname = Label(list_frame, text="NICKNAME")
        lb_elo = Label(list_frame, text="ELO")
        lb_first_role = Label(list_frame, text="FIRST ROLE")
        lb_second_role = Label(list_frame, text="SECOND ROLE")
        lbi = [lb_number, lb_name, lb_nickname, lb_elo, lb_first_role, lb_second_role]
        for j in range(len(lbi)):
            lbi[j].grid(row=0, column=j)


        #used this when i had no bd on my program
        """
        sorted_players = sort_players_by_name()
        for i in range(len(sorted_players)):
            lb_number = Label(list_frame, text=sorted_players[i].get_infos()[5].center(5, " "))
            lb_name = Label(list_frame, text=sorted_players[i].get_infos()[0].center(40, " "))
            lb_nickname = Label(list_frame, text=sorted_players[i].get_infos()[1].center(40, " "))
            lb_elo = Label(list_frame, text=sorted_players[i].get_infos()[2].center(40, " "))
            lb_first_role = Label(list_frame, text=sorted_players[i].get_infos()[3].center(40, " "))
            lb_second_role = Label(list_frame, text=sorted_players[i].get_infos()[4].center(40, " "))
            lbi = [lb_number, lb_name, lb_nickname, lb_elo, lb_first_role, lb_second_role]
            for j in range(len(lbi)):
                lbi[j].grid(row=i+1, column=j)
        """

        myCursor.execute("SELECT * FROM players ORDER BY name")
        my_results = myCursor.fetchall()
        for i in range(len(my_results)):
            lb_number = Label(list_frame, text=str(my_results[i][0]).center(5, " "))
            lb_name = Label(list_frame, text=str(my_results[i][1]).center(40, " "))
            lb_nickname = Label(list_frame, text=str(my_results[i][2]).center(40, " "))
            lb_elo = Label(list_frame, text=str(my_results[i][3]).center(40, " "))
            lb_first_role = Label(list_frame, text=str(my_results[i][4]).center(40, " "))
            lb_second_role = Label(list_frame, text=str(my_results[i][5]).center(40, " "))
            lbi = [lb_number, lb_name, lb_nickname, lb_elo, lb_first_role, lb_second_role]
            for j in range(len(lbi)):
                lbi[j].grid(row=i+1, column=j)


# This function is unused since I created the radio button funcion
def list_players_register_button():
    """Function called when we click on the list players by register order button"""
    global state
    if not state == "list_register":
        """Changing state and subtitle and showing on screen"""
        state = "list_register"
        sub_title["text"] = "LIST OF PLAYERS"
        sub_title.pack()

        clear_frames()

        """Creating a new frame for showing the widgets"""
        list_frame = Frame(window)
        list_frame["padx"] = 30
        list_frame["pady"] = 30
        createdFrames.append(list_frame)
        list_frame.pack()

        """Creating the labels to show the info on screen"""
        lb_number = Label(list_frame, text="REGISTER NUMBER")
        lb_name = Label(list_frame, text="NAME")
        lb_nickname = Label(list_frame, text="NICKNAME")
        lb_elo = Label(list_frame, text="ELO")
        lb_first_role = Label(list_frame, text="FIRST ROLE")
        lb_second_role = Label(list_frame, text="SECOND ROLE")
        lbi = [lb_number, lb_name, lb_nickname, lb_elo, lb_first_role, lb_second_role]
        for j in range(len(lbi)):
            lbi[j].grid(row=0, column=j)

        #This was before i had the bd working
        """
        for i in range(len(registeredPlayers)):
            lb_number = Label(list_frame, text=registeredPlayers[i].get_infos()[5].center(5, " "))
            lb_name = Label(list_frame, text=registeredPlayers[i].get_infos()[0].center(40, " "))
            lb_nickname = Label(list_frame, text=registeredPlayers[i].get_infos()[1].center(40, " "))
            lb_elo = Label(list_frame, text=registeredPlayers[i].get_infos()[2].center(40, " "))
            lb_first_role = Label(list_frame, text=registeredPlayers[i].get_infos()[3].center(40, " "))
            lb_second_role = Label(list_frame, text=registeredPlayers[i].get_infos()[4].center(40, " "))
            lbi = [lb_number, lb_name, lb_nickname, lb_elo, lb_first_role, lb_second_role]
            for j in range(len(lbi)):
                lbi[j].grid(row=i+1, column=j)
        """
        myCursor.execute("SELECT * FROM players ORDER BY id")
        my_results = myCursor.fetchall()
        for i in range(len(my_results)):
            lb_number = Label(list_frame, text=str(my_results[i][0]).center(5, " "))
            lb_name = Label(list_frame, text=str(my_results[i][1]).center(40, " "))
            lb_nickname = Label(list_frame, text=str(my_results[i][2]).center(40, " "))
            lb_elo = Label(list_frame, text=str(my_results[i][3]).center(40, " "))
            lb_first_role = Label(list_frame, text=str(my_results[i][4]).center(40, " "))
            lb_second_role = Label(list_frame, text=str(my_results[i][5]).center(40, " "))
            lbi = [lb_number, lb_name, lb_nickname, lb_elo, lb_first_role, lb_second_role]
            for j in range(len(lbi)):
                lbi[j].grid(row=i + 1, column=j)


def remove_player(name_entry, feedback_label):
    feedback_label.pack_forget()

    """Deleting name from database"""
    name_to_delete = name_entry.get().lower()
    sql = "DELETE FROM players WHERE name = %s"
    sql2 = "SELECT COUNT(*) FROM players WHERE name = %s"
    nms = ("" + name_to_delete,)
    myCursor.execute(sql2, nms)
    number_of_entries = myCursor.fetchone()
    if number_of_entries[0] > 0:
        myCursor.execute(sql, nms)
        feedback_label["text"] = " " + name_entry.get() + " was removed"
        feedback_label.pack()
        name_entry.delete(0, 'end')
        mydb.commit()
        return True
    feedback_label["text"] = " " + name_entry.get() + " was not found"
    feedback_label.pack()
    return False
    """
    for i in range(len(registeredPlayers)):
        if registeredPlayers[i].get_infos()[0].lower() == name_to_delete:
            registeredPlayers.remove(registeredPlayers[i])
            feedback_label["text"] = " " + name_entry.get() + " was removed"
            feedback_label.pack()
            name_entry.delete(0, 'end')
            return True
    feedback_label["text"] = " " + name_entry.get() + " was not found"
    feedback_label.pack()
    return False
    """


def remove_player_button():
    """Function called when we press remove player button"""
    global state
    if not state == "remove":
        state = "remove"
        sub_title["text"] = "REMOVE PLAYER"
        sub_title.pack()

        clear_frames()

        """Creating a new frame for showing the widgets"""
        frame = Frame(window)
        frame["padx"] = 30
        frame["pady"] = 30
        createdFrames.append(frame)
        frame.pack()

        """Creating the widgets"""
        name_lb = Label(frame, text="Name of the player")
        name_lb.pack()
        name_entry = Entry(frame)
        name_entry.focus()
        name_entry.pack()
        feedback_label = Label(frame)

        """Creating the confirm button"""
        confirm_button = Button(frame, text="Confirm")
        confirm_button["command"] = partial(remove_player, name_entry, feedback_label)
        confirm_button.pack()


def update_player_button():
    """Function called when we press update player button"""
    global state
    if not state == "update":
        state = "update"
        sub_title["text"] = "UPDATE PLAYER"
        sub_title.pack()

        create_list_names_radiobuttons(1)


def update_player(name_entered, feedback_label):
    feedback_label.pack_forget()
    sql = "SELECT * FROM players WHERE name = %s"
    sql2 = "SELECT COUNT(*) FROM players WHERE name = %s"
    nms = ("" + name_entered, )
    myCursor.execute(sql2, nms)
    number = myCursor.fetchone()
    if number > 0:
        myCursor.execute(sql, nms)
        result = myCursor.fetchone()[1]
        if result.lower() == name_entered.lower():
            clear_frames()
            frame = Frame(window)
            frame["padx"] = 30
            frame["pady"] = 30
            frame.pack()
            createdFrames.append(frame)

            """Adding all the widgets"""
            name = Label(frame, text="name: ")
            name.grid(row=0, column=0)
            name_entry = Entry(frame)
            name_entry.focus()
            name_entry.insert(END, registeredPlayers[i].name)
            name_entry.grid(row=0, column=1)

            nickname = Label(frame, text="nickname: ")
            nickname.grid(row=1, column=0)
            nickname_entry = Entry(frame)
            nickname_entry.grid(row=1, column=1)
            nickname_entry.insert(END, registeredPlayers[i].nickname)

            elo = Label(frame, text="elo: ")
            elo.grid(row=2, column=0)
            variable1 = StringVar(frame)
            variable1.set(registeredPlayers[i].elo)
            elo_menu = OptionMenu(frame, variable1, "unranked", "bronze 5", "bronze 4", "bronze 3", "bronze 2",
                                  "bronze 1",
                                  "silver 5", "silver 4", "silver 3", "silver 2", "silver 1", "gold 5", "gold 4",
                                  "gold 3", "gold 2", "gold 1", "platinum 5", "platinum 4", "platinum 3", "platinum 2",
                                  "platinum 1", "diamond 5", "diamond 4", "diamond 3", "diamond 2", "diamond 1",
                                  "master", "challenger")
            elo_menu.grid(row=2, column=1)

            first_role = Label(frame, text="first role: ")
            first_role.grid(row=3, column=0)
            variable2 = StringVar(frame)
            variable2.set(registeredPlayers[i].firstRole)
            first_role_menu = OptionMenu(frame, variable2, "Top Laner", "Jungler", "Mid Laner",
                                         "Adc or BottomCarry", "Support")
            first_role_menu.grid(row=3, column=1)

            second_role = Label(frame, text="second role: ")
            second_role.grid(row=4, column=0)
            variable3 = StringVar(frame)
            variable3.set(registeredPlayers[i].secondRole)
            second_role_menu = OptionMenu(frame, variable3, "Top Laner", "Jungler", "Mid Laner",
                                          "Adc or BottomCarry", "Support")
            second_role_menu.grid(row=4, column=1)

            send_button = Button(frame, text="Update")
            send_button["command"] = partial(save_updated_player, variable1, variable2, variable3,
                                             frame, registeredPlayers[i].regNumber)
            send_button.grid(row=5, column=1)

            return True

        feedback_label["text"] = " " + name_entered + " was not found"
        feedback_label.pack()
        return False

    #this was before i had the bd implemented
    """
    for i in range(len(registeredPlayers)):
        if registeredPlayers[i].get_infos()[0].lower() == name_entered.lower():
            clear_frames()
            frame = Frame(window)
            frame["padx"] = 30
            frame["pady"] = 30
            frame.pack()
            createdFrames.append(frame)

            "Adding all the widgets"
            name = Label(frame, text="name: ")
            name.grid(row=0, column=0)
            name_entry = Entry(frame)
            name_entry.focus()
            name_entry.insert(END, registeredPlayers[i].name)
            name_entry.grid(row=0, column=1)

            nickname = Label(frame, text="nickname: ")
            nickname.grid(row=1, column=0)
            nickname_entry = Entry(frame)
            nickname_entry.grid(row=1, column=1)
            nickname_entry.insert(END, registeredPlayers[i].nickname)

            elo = Label(frame, text="elo: ")
            elo.grid(row=2, column=0)
            variable1 = StringVar(frame)
            variable1.set(registeredPlayers[i].elo)
            elo_menu = OptionMenu(frame, variable1, "unranked", "bronze 5", "bronze 4", "bronze 3", "bronze 2", "bronze 1",
                                  "silver 5", "silver 4", "silver 3", "silver 2", "silver 1", "gold 5", "gold 4",
                                  "gold 3", "gold 2", "gold 1", "platinum 5", "platinum 4", "platinum 3", "platinum 2",
                                  "platinum 1", "diamond 5", "diamond 4", "diamond 3", "diamond 2", "diamond 1",
                                  "master", "challenger")
            elo_menu.grid(row=2, column=1)

            first_role = Label(frame, text="first role: ")
            first_role.grid(row=3, column=0)
            variable2 = StringVar(frame)
            variable2.set(registeredPlayers[i].firstRole)
            first_role_menu = OptionMenu(frame, variable2, "Top Laner", "Jungler", "Mid Laner",
                                         "Adc or BottomCarry", "Support")
            first_role_menu.grid(row=3, column=1)

            second_role = Label(frame, text="second role: ")
            second_role.grid(row=4, column=0)
            variable3 = StringVar(frame)
            variable3.set(registeredPlayers[i].secondRole)
            second_role_menu = OptionMenu(frame, variable3, "Top Laner", "Jungler", "Mid Laner",
                                          "Adc or BottomCarry", "Support")
            second_role_menu.grid(row=4, column=1)

            send_button = Button(frame, text="Update")
            send_button["command"] = partial(save_updated_player, variable1, variable2, variable3,
                                             frame, registeredPlayers[i].regNumber)
            send_button.grid(row=5, column=1)

            return True
    feedback_label["text"] = " " + name_entry.get() + " was not found"
    feedback_label.pack()
    return False
"""


def save_updated_player(variable1, variable2, variable3, frame):
    """Get the entries that were typed by the user"""
    name = frame.children["!entry"].get()
    nickname = frame.children["!entry2"].get()
    elo = variable1.get()
    first_role = variable2.get()
    second_role = variable3.get()

    updated_player = player_class.Player(name, nickname, elo, first_role, second_role)

    for k in range(len(registeredPlayers)):
        if registeredPlayers[k].regNumber == updated_player.regNumber:
            registeredPlayers[k] = updated_player
    clear_frames()
    frame = Frame(window)
    frame.pack()
    createdFrames.append(frame)
    lb = Label(frame, text="Update successful", bg="black", fg="white")
    lb.pack()


# Clear all frames on the screen
def clear_frames():
    """Deleting old frames"""
    for i in createdFrames:
        i.destroy()

# Function to delete from de db using the radiobuttons system
def delete_player_db(player, order):
    sql = "DELETE FROM players WHERE LOWER(name) = %s"
    nms = (player.get().lower(),)
    myCursor.execute(sql, nms)
    mydb.commit()
    create_list_names_radiobuttons(order)
    return


def add_player_button():
    """This function is called when we click the add player button"""
    global state
    if not state == "add":
        clear_frames()

        """Changing state global variable and subtitle and showing on screen"""
        state = "add"
        sub_title["text"] = "ADD PLAYER"
        sub_title.pack()
        """Create a new frame for showing the widgets that are specific for
                this form"""
        frame_buttons = create_frame()
        """Adding all the widgets"""
        # Creating font for labels
        label_font = tkinter.font.Font(family='Arial', size=10)
        name = Label(frame_buttons[0], text="name: ", font=label_font)
        name.pack(fill=X)
        name_entry = Entry(frame_buttons[0], width=25, font=label_font)
        name_entry.focus()
        name_entry.pack()

        nickname = Label(frame_buttons[0], text="nickname: ", font=label_font)
        nickname.pack(fill=X)
        nickname_entry = Entry(frame_buttons[0], width=25, font=label_font)
        nickname_entry.pack()

        elo = Label(frame_buttons[0], text="elo: ", font=label_font)
        elo.pack(fill=X)
        variable1 = StringVar(frame_buttons[0])
        variable1.set("bronze 5")
        elo_menu = OptionMenu(frame_buttons[0], variable1, "unranked", "bronze 5", "bronze 4", "bronze 3", "bronze 2", "bronze 1",
                              "silver 5", "silver 4","silver 3", "silver 2", "silver 1", "gold 5", "gold 4",
                              "gold 3", "gold 2", "gold 1","platinum 5", "platinum 4", "platinum 3", "platinum 2",
                              "platinum 1", "diamond 5","diamond 4", "diamond 3", "diamond 2", "diamond 1",
                              "master", "challenger")
        elo_menu["font"] = label_font
        elo_menu.pack(fill=X)

        first_role = Label(frame_buttons[0], text="first role: ", font=label_font)
        first_role.pack(fill=X)
        variable2 = StringVar(frame_buttons[0])
        variable2.set("Top Laner")
        first_role_menu = OptionMenu(frame_buttons[0], variable2, "Top Laner", "Jungler", "Mid Laner",
                                     "Adc or BottomCarry", "Support")
        first_role_menu["font"] = label_font
        first_role_menu.pack(fill=X)

        second_role = Label(frame_buttons[0], text="second role: ", font=label_font)
        second_role.pack(fill=X)
        variable3 = StringVar(frame_buttons[0])
        variable3.set("Jungler")
        second_role_menu = OptionMenu(frame_buttons[0], variable3, "Top Laner", "Jungler", "Mid Laner",
                                      "Adc or BottomCarry", "Support")
        second_role_menu["font"] = label_font
        second_role_menu.pack(fill=X)

        send_button = Button(frame_buttons[0], text="Save", bg="dodgerblue2", bd=10, fg='white', font=label_font)
        send_button["command"] = partial(save_player, variable1, variable2, variable3, frame_buttons[0])
        send_button.pack(fill=X, padx=10, pady=10)


def update_player_db(player):
    global state
    sql = "SELECT * FROM players WHERE LOWER(name) = %s"
    nms = (player.get().lower(),)
    myCursor.execute(sql, nms)
    result = myCursor.fetchone()
    state = "update"

    clear_frames()
    sub_title["text"] = "UPDATE PLAYER"
    sub_title.pack()
    """Create a new frame for showing the widgets that are specific for
            this form"""
    frame_buttons = create_frame()

    label_font = tkinter.font.Font(family='Arial', size=10)
    name = Label(frame_buttons[0], text="name: ", font=label_font)
    name.pack(fill=X)
    name_entry = Entry(frame_buttons[0], width=25, font=label_font)
    name_entry.focus()
    name_entry.insert(END, result[1])
    name_entry.pack()

    nickname = Label(frame_buttons[0], text="nickname: ", font=label_font)
    nickname.pack(fill=X)
    nickname_entry = Entry(frame_buttons[0], width=25, font=label_font)
    nickname_entry.insert(END, result[2])
    nickname_entry.pack()

    elo = Label(frame_buttons[0], text="elo: ", font=label_font)
    elo.pack(fill=X)
    variable1 = StringVar(frame_buttons[0])
    variable1.set(result[3])
    elo_menu = OptionMenu(frame_buttons[0], variable1, "unranked", "bronze 5", "bronze 4", "bronze 3", "bronze 2",
                          "bronze 1",
                          "silver 5", "silver 4", "silver 3", "silver 2", "silver 1", "gold 5", "gold 4",
                          "gold 3", "gold 2", "gold 1", "platinum 5", "platinum 4", "platinum 3", "platinum 2",
                          "platinum 1", "diamond 5", "diamond 4", "diamond 3", "diamond 2", "diamond 1",
                          "master", "challenger")
    elo_menu["font"] = label_font
    elo_menu.pack(fill=X)

    first_role = Label(frame_buttons[0], text="first role: ", font=label_font)
    first_role.pack(fill=X)
    variable2 = StringVar(frame_buttons[0])
    variable2.set(result[5])
    first_role_menu = OptionMenu(frame_buttons[0], variable2, "Top Laner", "Jungler", "Mid Laner",
                                 "Adc or BottomCarry", "Support")
    first_role_menu["font"] = label_font
    first_role_menu.pack(fill=X)

    second_role = Label(frame_buttons[0], text="second role: ", font=label_font)
    second_role.pack(fill=X)
    variable3 = StringVar(frame_buttons[0])
    variable3.set(result[6])
    second_role_menu = OptionMenu(frame_buttons[0], variable3, "Top Laner", "Jungler", "Mid Laner",
                                  "Adc or BottomCarry", "Support")
    second_role_menu["font"] = label_font
    second_role_menu.pack(fill=X)

    send_button = Button(frame_buttons[0], text="Update", bg="dodgerblue2", bd=10, fg='white', font=label_font)
    send_button["command"] = partial(update_player_to_db, variable1, variable2, variable3, frame_buttons[0], result[0])
    send_button.pack(fill=X, padx=10, pady=10)

# Function to show list of registered players on the bd as a listbox, using SUNKEN state
def create_list_names_radiobuttons(order):
    global state
    state = "menu"
    clear_frames()
    frame_buttons = create_frame()

    # Creating my font to use on radiobuttons
    radio_button_font = tkinter.font.Font(family='Arial', size=10)

    name = StringVar()
    sql1 = "SELECT COUNT(*) FROM players"
    myCursor.execute(sql1)
    total_registered = myCursor.fetchone()[0]
    sql2 = "SELECT name FROM players"
    sql3 = "SELECT nickname FROM players"
    sql4 = "SELECT id FROM players"
    if order == 0:
        sql4 += " ORDER BY id"
        sql3 += " ORDER BY id"
        sql2 += " ORDER BY id"
    elif order == 1:
        sql4 += " ORDER BY name"
        sql3 += " ORDER BY name"
        sql2 += " ORDER BY name"
    myCursor.execute(sql2)
    names = myCursor.fetchall()
    myCursor.execute(sql3)
    nicknames = myCursor.fetchall()
    myCursor.execute(sql4)
    registers = myCursor.fetchall()
    for i in range(total_registered):
        name_i = names[i][0]
        nickname_i = nicknames[i][0]
        register_i = registers[i][0]
        radio_i = Radiobutton(frame_buttons[0], text=str(register_i) + " - " + str(name_i) + " - " + str(nickname_i),
                              variable=name, value=str(name_i.lower()), indicatoron=0, width=70, fg="black",
                              height=2, font=radio_button_font)
        radio_i["highlightbackground"] = "blue"
        if i % 2 == 0:
            radio_i["bg"] = "indianred1"
        else:
            radio_i["bg"] = "rosybrown2"
        radio_i.pack(fill=X, pady=3)

    """Creating the buttons"""
    # Creating my font to use on radiobuttons
    button_font = tkinter.font.Font(family='Arial', size=10)
    update_button_var = Button(frame_buttons[0], text="Update Player", bg="plum1", bd=5, font=button_font, width=30)
    update_button_var["command"] = partial(update_player_db, name)
    update_button_var.pack(padx=20, pady=5)
    add_player_button_var = Button(frame_buttons[0], text="Add Player", command=add_player_button, bg="plum1", bd=5,
                                   font=button_font, width=30)
    add_player_button_var.pack(padx=20, pady=5)
    delete_player_button_var = Button(frame_buttons[0], text="Delete Player", bg="plum1", bd=5, font=button_font, width=30)
    delete_player_button_var["command"] = partial(delete_player_db, name, order)
    delete_player_button_var.pack(padx=20, pady=5)


# This was a function i tried to use to make use of listboxes, didn't work really well
def create_players_listbox(frame):
    players_box = Listbox(frame, width=100, selectmode=BROWSE)
    players_box.pack()
    for i in range(len(registeredPlayers)):
        players_box.insert(END, " " * 40 + "Name: " + registeredPlayers[i].get_infos()[0] +
                           " " * 40 + "Nickname: " + registeredPlayers[i].get_infos()[1])
    return players_box


title = Label(window, text="LEAGUE OF LEGENDS DRAFT PLATFORM", bg="black", fg="white", font="Helvetica, 16",
              bd=5, anchor=W, justify=LEFT)
owner = Label(window, text="Made by Ruan da Fonseca Ramos, with love", bg="black", fg="white", font="Helvetica, 11",
              anchor=W, justify=LEFT)
title.pack()
owner.pack()

"""Variable to save all created frames globally"""
createdFrames = []

"""Creating the main menu buttons"""
create_frame()

window.mainloop()
