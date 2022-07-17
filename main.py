"""Parking application"""
# from tkinter import *
from tkinter import Label, LabelFrame, Toplevel, StringVar, Entry, END, Button, messagebox, Tk, Canvas, TclError, Message
import customtkinter
import sqlite3
from time import strftime
import re
import time
from turtle import bgcolor
# from tkinter import Tk, Canvas
# from tkinter import messagebox
from PIL import ImageTk, Image

#customtkinter.set_appearance_mode("Light")  # Modes: system (default), light, dark
#customtkinter.set_default_color_theme("dark-blue")  # Themes: blue (default), dark-blue, green


# Create root window
root = Tk()
# root title
root.title("Parking application")
# root size and not resizable
root.geometry("620x650")
root.resizable(width=False, height=False)
# background color for window
root.configure(bg="#F5F5F5")
# icon for application window
root.iconbitmap('phouse.ico')

# Parking spaces variable
TOTAL_PARKING_SPACES = 50


# Function to show date and keep time dynamic at root
def current_time_date():
    """This function is for the main menu (root).

    It keeps the time dynamic and stores it in the time_label.

    The function also shows the current date and stores it in the date_label."""
    my_time = strftime(' Local time: %H:%M:%S')
    time_label.config(text=str(my_time), font=("Verdana", 10), fg="White", bg="black")
    time_label.after(1000, current_time_date)
    todays_date = strftime('Date: %d/%m/%y')
    date_label.config(text=str(todays_date), font=("Verdana", 10), fg="White", bg="black")


# Function to show info about prices (connected to the 'View price list'-button)
def prices():
    """This function shows the price list when the 'View price list'-button is clicked.
    The price list appears in a Message, the box automatically closes after 25 seconds"""

    from tkinter import Tk
    from tkinter.messagebox import Message 
    from _tkinter import TclError
    TIME_TO_WAIT = 25000
    root = Tk()
    root.withdraw()
    root.iconbitmap('phouse.ico')
    try:
        root.after(TIME_TO_WAIT, root.destroy) 
        Message(title="Price list", message="PRICE LIST:\nMinute 0-60 are FREE of charge.\n\n"
        "From minute 61 onwards the price is 0.25 SEK/min\n(15 SEK/hour).", master=root).show()
    except TclError:
        pass


# Function that takes user to new window after clicking on start parking in root menu (connected to 'Start parking'-button)
def start_parking():
    """The start_parking function is activated when the user clicks on start parking button in the main menu.
    The purpose of the function is to insert a registration number into the tables and start parking session for a car.

    First it creates a new window, named start_pop_up. While inside start_pop_up the root buttons gets disabled.

    In this window the user has to type in a registration number that is limited to 6 upper case characters in the entrybox.
    If the reg num is valid and unique it gets inserted into to car and parked_cars table with reg num and start time.
    If the reg num is invalid --> messagebox(showerror).
    If the reg num is valid and not unique --> messagebox(showerror).

    When the parking session is started successfully, start_pop_up closes, root button gets activated and parking spaces decreases by 1.
    """
    # Create new window called start_pop_up for start parking-button
    start_pop_up = Toplevel(root)
    start_pop_up.iconbitmap('phouse.ico')
    start_pop_up.title("Start parking")
    start_pop_up.geometry("400x200")
    start_pop_up.resizable(width=False, height=False)
    start_pop_up.config(bg="#F5F5F5")

    # Disable root menu buttons while inside start_pop_up
    def disable_main_buttons():
        start_parking_button.config(state='disabled')
        stop_parking_button.config(state='disabled')
        status_parking_button.config(state='disabled')
    disable_main_buttons()

    # function to activate root menu buttons
    def activate_root_buttons():
        start_parking_button.config(state='normal')
        stop_parking_button.config(state='normal')
        status_parking_button.config(state='normal')

    startlabelframe = LabelFrame(start_pop_up, background='#F5F5F5')
    startlabelframe.pack(pady=15)

    # Label with the text that asks for users reg num.
    def create_labels():
        regnum_label = Label(startlabelframe, text="Please enter your registration number", font=("Verdana 11 bold"), fg="black", bg='#F5F5F5')
        regnum_label.pack(pady=20)
    create_labels()

    # Entry box for user to type in reg num
    entry_text = StringVar()
    entry_regnum = Entry(startlabelframe, width=30, borderwidth=4, font=("Verdana", 9), textvariable=entry_text)
    entry_regnum.pack()

    # Function that limits reg num entry to 6 upper case characters.
    def character_limit(entry_text):
        if len(entry_text.get()) > 0:
            entry_text.set(entry_text.get().upper()[:6])
    entry_text.trace("w", lambda *args: character_limit(entry_text))

    # Function for when start button inside start_pop_up is clicked
    def start_click():
        global TOTAL_PARKING_SPACES
        date_time = strftime("%m/%d/%Y, %H:%M:%S")

        # Create a connection to DB
        connection = sqlite3.connect('park.db')

        # Create cursor
        cursor = connection.cursor()

        # Enable foreign keys
        # cur.execute("PRAGMA foreign_keys=1")

        # Check if reg num is valid
        regnum = entry_text.get()
        if re.match(r"^[A-Za-z]{3}[0-9]{2}[0-9A-Za-z]{1}$", regnum):
            # Check if reg num is already in the database, if yes -> showerror.
            cursor.execute("SELECT car_id FROM car WHERE car_id=?", (regnum,))
            result = cursor.fetchone()
            if result:
                messagebox.showerror(title='Already in use,', message=f'{regnum} is already in use!\nPlease try again with a different registration number.')
                start_pop_up.destroy()
                activate_root_buttons()
            # If reg num is valid and unique insert into car and parked_cars table
            else:
                cursor.execute("INSERT INTO car (car_id) VALUES (?)", (regnum,))
                cursor.execute("INSERT INTO parked_cars (parked_car) VALUES (?)", (regnum,))
                TOTAL_PARKING_SPACES -= 1
            # Commit changes
                connection.commit()
            # Clear entry box
                entry_regnum.delete(0, END)
                park_space_label.config(text='Available spots: ' + str(TOTAL_PARKING_SPACES))
                messagebox.showinfo(title='Park started', message=f'Parking for {regnum} started at {date_time}')
        else:
            messagebox.showerror(title='Not valid', message=f'{regnum} is not a valid registration number\nPlease try again.')
            entry_regnum.delete(0, END)
        # Close window and activate root menu buttons
        start_pop_up.destroy()
        activate_root_buttons()

    # Create start button for start_pop_up
    start_button = Button(startlabelframe, command=start_click, height=0, width=30, relief="solid", text="Start parking", font=('Verdana', 10), fg='#F5F5F5', bg='#2E8B57')
    start_button.pack(pady=20)

    # Activate root buttons and close start_pop_up page when clicking 'X' on Windows Manager
    def on_close():
        start_parking_button.config(state='normal')
        stop_parking_button.config(state='normal')
        status_parking_button.config(state='normal')
        start_pop_up.destroy()

    start_pop_up.protocol("WM_DELETE_WINDOW", on_close)


# Function to see parked car status (connected to 'See status for parked car'-button)
def car_status():
    """The car_status function is activated when the user clicks on see status for parked button in the main menu.
    The purpose of the function is to look for a registration number in the db-tables and show value for the chosen reg num.

    First it creates a new window, named status_pop_up. While inside status_pop_up the root buttons gets disabled.
    After the user click on 'check status'-button the 'check status'-button gets disabled.

    In this window the user has to type in a registration number that is limited to 6 upper case characters in the entrybox.
    If the reg num is valid and in the db --> reg num, start time, stop time, total time and price will be shown for the chosen reg num.
    If the reg num is invalid --> messagebox(showerror).
    If the reg num is valid and not in the db --> messagebox(showerror).
    """
    # global status_pop_up
    status_pop_up = Toplevel(root)

    # Remove Windows Manager bar
    # status_pop_up.overrideredirect(True)

    status_pop_up.iconbitmap('phouse.ico')
    status_pop_up.title("Car status")
    status_pop_up.geometry("400x380")
    status_pop_up.resizable(width=False, height=False)
    status_pop_up.config(bg="#F5F5F5")

    start_parking_button.config(state='disabled')
    stop_parking_button.config(state='disabled')
    status_parking_button.config(state='disabled')

    statuslabelframe = LabelFrame(status_pop_up, background='#F5F5F5')
    statuslabelframe.pack(pady=15)

    # function to activate root menu buttons
    def activate_root_buttons():
        start_parking_button.config(state='normal')
        stop_parking_button.config(state='normal')
        status_parking_button.config(state='normal')

    # Label for the text that asks for users reg num.
    regnum_label = Label(statuslabelframe, text="Please enter your registration number", font=("Verdana 11 bold"), fg="black", bg='#F5F5F5')
    regnum_label.pack(pady=20)

    # Entry for reg num.
    # global entry_text_status
    # global entry_regnum_status
    entry_text_status = StringVar()
    entry_regnum_status = Entry(statuslabelframe, width=30, borderwidth=4, font=("Verdana", 9), textvariable=entry_text_status)
    entry_regnum_status.pack()

    # Function that limits reg num entry to 6 upper case characters.
    def character_limit(entry_text):
        if len(entry_text.get()) > 0:
            entry_text.set(entry_text.get().upper()[:6])
    entry_text_status.trace("w", lambda *args: character_limit(entry_text_status))

    # Funcion when 'check status'-button is clicked.
    def status_click():
        # Disable 'check status'-button when info about car is shown
        status_button.config(state='disabled')
        # Create a connection to DB
        con = sqlite3.connect('park.db')

        # Create cursor
        curs = con.cursor()

        # Variable to store inputed reg num
        regnum = entry_text_status.get()

        # Check if regnum has valid format
        if re.match(r"^[A-Za-z]{3}[0-9]{2}[0-9A-Za-z]{1}$", regnum):
            # Get total parked time for a parked_car and store it in variable parked_time
            #curs.execute("SELECT CAST ((JulianDay('now','localtime') - JulianDay(start_time)) * 24 * 60 AS Integer) FROM parked_cars WHERE parked_car=?", (regnum,))
            curs.execute("SELECT (JulianDay('now','localtime') - JulianDay(start_time)) * 24 * 60 FROM parked_cars WHERE parked_car=?", (regnum,))
            
            # Query below is to pause parking time and price
            #curs.execute("SELECT ((JulianDay(stop_time) - JulianDay(start_time)) * 24) * 60 FROM parked_cars WHERE parked_car=?", (regnum,))
            #curs.execute("SELECT JULIANDAY(stop_time) - JULIANDAY(start_time) * 1440 FROM parked_cars WHERE parked_car=?", (regnum,))
            parked_time = curs.fetchone()
            # Select the right car by its regnum to check its status
            curs.execute("SELECT * FROM parked_cars WHERE parked_car=?", (regnum,))
            car_info = curs.fetchone()
            # If regnum is in db
            if car_info:
                # Variables to store reg num, start/stop time and price
                car_reg = "Registration number: " + str(car_info[0])
                start_time = "Start date and time: " + str(car_info[1])
                stop_time = "Stop date and time: " + str(car_info[2])
                # Show total parking time, if time < 60min ---> show in minutes, if time > 60min ---> show in hours
                if parked_time[0] <= 59:
                    total_time = "Total parking time: " + str(round(parked_time[0])) + ' minutes'
                    print(total_time)
                elif parked_time[0] >= 60:
                    #try:
                        #total_time = "Total parking time: " + str(round(parked_time[0] / 60, 2)) + ' hours'
                    a = (round(parked_time[0] / 60, 2))
                    b = a - int(a)
                    #print(round(b * 60))
                    #except ValueError:
                        #pass
                    #a = int(total_time) 
                    #c = int(a) - int(a)
                    #print(c)
                    #print((a*60) % 60)
                    total_time = "Total parking time: " + str(int(parked_time[0] / 60)) + " hours & " + str(round(b*60)) + " minutes"

                # Variable for pricing for a parked car (0-60min FREE)
                if parked_time[0] <= 60:
                    price = "Current price: " + str(round(parked_time[0] * 0)) + ' SEK'
                # Price for 61 min onwards ---> 0.25kr/min, REMOVES FIRST FREE HOUR)
                elif parked_time[0] >= 61:
                    price = "Current price: " + str(round((parked_time[0] - 60) * (0.25), 1)) + ' SEK'
                    print(price)

                # Labels for the variables above
                parking_summary = LabelFrame(status_pop_up, text="Car status", bg='#F5F5F5', font=('Verdana 11 bold'), pady=5, labelanchor='n')
                parking_summary.pack(pady=5)
                car_reg_label = Label(parking_summary, text=car_reg, bg='#F5F5F5', font=("Verdana", 11))
                car_reg_label.pack(anchor="w")
                start_time_label = Label(parking_summary, text=start_time, bg='#F5F5F5', font=("Verdana", 11))
                start_time_label.pack(anchor="w")
                stop_time_label = Label(parking_summary, text=stop_time, bg='#F5F5F5', font=("Verdana", 11))
                stop_time_label.pack(anchor="w")
                total_time_label = Label(parking_summary, text=total_time, bg='#F5F5F5', font=("Verdana", 11))
                total_time_label.pack(anchor="w")
                price_label = Label(parking_summary, text=price, bg='#F5F5F5', font=("Verdana", 11))
                price_label.pack(anchor="w")

                # Clear entry box after click on 'check status'
                entry_regnum_status.delete(0, END)
            # If regnum is valid but not in db, show error message.
            elif not car_info:
                messagebox.showerror(title='Car not found', message=f'Car with registration number: {regnum} not found')
                status_pop_up.destroy()
                activate_root_buttons()
        # If regnum is not in valid format, show error message.
        else:
            messagebox.showerror(title='Not valid', message=f'{regnum} is not a valid registration number\nPlease try again.')
            entry_regnum_status.delete(0, END)
            status_pop_up.destroy()
            activate_root_buttons()
        # Commit changes
        con.commit()

    # Create status button for status_pop_up
    status_button = Button(statuslabelframe, command=status_click, height=0, width=30, relief="solid", text="Check status", font=('Verdana', 10), fg='#F5F5F5', bg='#3466a5')
    status_button.pack(pady=20)

    # Function to activate root buttons and close status_pop_up page when clicking 'X' on the Windows Manager.
    def on_close():
        start_parking_button.config(state='normal')
        stop_parking_button.config(state='normal')
        status_parking_button.config(state='normal')
        status_pop_up.destroy()
    status_pop_up.protocol("WM_DELETE_WINDOW", on_close)

def stop_parking():

    # global status_pop_up
    stop_pop_up = Toplevel(root)

    # Remove Windows Manager bar
    # status_pop_up.overrideredirect(True)

    stop_pop_up.iconbitmap('phouse.ico')
    stop_pop_up.title("Stop parking")
    stop_pop_up.geometry("400x450")
    stop_pop_up.resizable(width=False, height=False)
    stop_pop_up.config(bg="#F5F5F5")

    start_parking_button.config(state='disabled')
    stop_parking_button.config(state='disabled')
    status_parking_button.config(state='disabled')
    
    # function to activate root menu buttons
    def activate_root_buttons():
        start_parking_button.config(state='normal')
        stop_parking_button.config(state='normal')
        status_parking_button.config(state='normal')

    stoplabelframe = LabelFrame(stop_pop_up, background='#F5F5F5')
    stoplabelframe.pack(pady=15)

    # Label for the text that asks for users reg num.
    regnum_label = Label(stoplabelframe, text="Please enter your registration number", font=("Verdana 11 bold"), fg="black", bg='#F5F5F5')
    regnum_label.pack(pady=20)

    
    # Entry for reg num.
    # global entry_text_status
    # global entry_regnum_status
    entry_text_stop = StringVar()
    entry_regnum_stop = Entry(stoplabelframe, width=30, borderwidth=4, font=("Verdana", 9), textvariable=entry_text_stop)
    entry_regnum_stop.pack()

    # Function that limits reg num entry to 6 upper case characters.
    def character_limit(entry_text):
        if len(entry_text.get()) > 0:
            entry_text.set(entry_text.get().upper()[:6])
    entry_text_stop.trace("w", lambda *args: character_limit(entry_text_stop))

    # Funcion when 'stop parking'-button is clicked.
    def stop_click():
        global TOTAL_PARKING_SPACES

        # Disable 'stop parking'-button when button is pressed
        stop_button.config(state='disabled')
        # Create a connection to DB
        con = sqlite3.connect('park.db')

        # Create cursor
        curs = con.cursor()

        # Variable to store inputed reg num
        regnum = entry_text_stop.get()

        # Check if regnum has valid format
        if re.match(r"^[A-Za-z]{3}[0-9]{2}[0-9A-Za-z]{1}$", regnum):
            curs.execute("SELECT car_id FROM car WHERE car_id=?", (regnum,))
            result = curs.fetchone()
            if not result:
                messagebox.showerror(title='Not in use', message=f'Car: {regnum} not found!\nPlease try again with a different registration number.')
                stop_pop_up.destroy()
                activate_root_buttons()
            # If reg num is valid and unique insert into car and parked_cars table
            else:
                curs.execute("""UPDATE parked_cars SET stop_time = datetime(julianday('now', 'localtime')) WHERE parked_car=?""", (regnum,))
                curs.execute("""UPDATE parked_cars SET total_time = ROUND(((julianday(stop_time) - julianday(start_time)) * 24 * 60) / 60, 2.00)""")
                curs.execute("""UPDATE parked_cars SET price = CASE
                                                               WHEN (total_time) BETWEEN 0 AND 1 THEN 0
                                                               ELSE ROUND((total_time - 1.00) * (15.00), 1)
                                                               END
                                WHERE parked_car = ?""", (regnum,))

                # Parking summary shows after user stops parking session
                curs.execute("""SELECT * FROM parked_cars WHERE parked_car=?""", (regnum,))
                car_info = curs.fetchone()
                park_summary = (f'Parking summary')
                car_reg = "Registration number: " + str(car_info[0])
                start_time = "Start date and time: " + str(car_info[1])
                stop_time = "Stop date and time: " + str(car_info[2])
                total_time = str(car_info[3])
                if total_time < "1":
                    total_time = "Total parking time: " + str(round(car_info[3] * 60, 1)) + " minutes"
                elif total_time >= "1":
                    a = car_info[3]
                    b = a - int(a)
                    total_time = "Total parking time: " + str(int(car_info[3])) + " hours & " + str((round((b * 60) % 60))) + " minutes"  
                price = "Total price: " + str(car_info[4]) + " SEK"
                
                # Labels for the variables above
                parking_summary = LabelFrame(stop_pop_up, text=park_summary, bg='#F5F5F5', font=('Verdana 11 bold'), pady=5, labelanchor='n')
                parking_summary.pack(pady=5)
                car_reg_label = Label(parking_summary, text=car_reg, bg='#F5F5F5', font=("Verdana", 11))
                car_reg_label.pack(padx= 8, anchor='w')
                start_time_label = Label(parking_summary, text=start_time, bg='#F5F5F5', font=("Verdana", 11))
                start_time_label.pack(padx= 8, anchor='w')
                stop_time_label = Label(parking_summary, text=stop_time, bg='#F5F5F5', font=("Verdana", 11))
                stop_time_label.pack(padx= 8, anchor='w')
                total_time_label = Label(parking_summary, text=total_time, bg='#F5F5F5', font=("Verdana", 11))
                total_time_label.pack(padx= 8, anchor='w')
                price_label = Label(parking_summary, text=price, bg='#F5F5F5', font=("Verdana", 11))
                price_label.pack(padx= 8, anchor='w')

                #frame1= Tk.Frame(stop_pop_up, width=50)
                #frame1.pack()

                receipt_label = Label(stop_pop_up, text='Do you wish to get the receipt?', bg='#F5F5F5', font=("Verdana", 11))
                receipt_label.pack(padx= 8, pady=8, anchor='w')

                

                #yes_button = Button(stop_pop_up, command='', height=0, width=30, relief="solid", text="Yes", font=('Verdana', 10), fg='#F5F5F5', bg='#8f1d21')
                #yes_button.pack(pady=20)

                TOTAL_PARKING_SPACES += 1

                # Destroy stop_pop_up after 5 minutes and activate root buttons.
                stop_pop_up.after(300000, lambda: stop_pop_up.destroy()) #activate_root_buttons())
                start_parking_button.after(300000, lambda: start_parking_button.config(state='normal'))
                stop_parking_button.after(300000, lambda: stop_parking_button.config(state='normal'))
                status_parking_button.after(300000, lambda: status_parking_button.config(state='normal'))

                # Commit changes
                con.commit()
            # Clear entry box
                entry_regnum_stop.delete(0, END)
                park_space_label.config(text='Available spots: ' + str(TOTAL_PARKING_SPACES))
                # messagebox.showinfo(title='Park started', message=f'Parking for {regnum} started at {date_time}')
        else:
            messagebox.showerror(title='Not valid', message=f'{regnum} is not a valid registration number\nPlease try again.')
            entry_regnum_stop.delete(0, END)
            stop_pop_up.destroy()
            activate_root_buttons()

    # Create stop button for stop_pop_up
    stop_button = Button(stoplabelframe, command=stop_click, height=0, width=30, relief="solid", text="Stop parking", font=('Verdana', 10), fg='#F5F5F5', bg='#8f1d21')
    stop_button.pack(pady=20)

    # Function to activate root buttons and close status_pop_up page when clicking 'X' on the Windows Manager.
    def on_close():
        start_parking_button.config(state='normal')
        stop_parking_button.config(state='normal')
        status_parking_button.config(state='normal')
        stop_pop_up.destroy()
    stop_pop_up.protocol("WM_DELETE_WINDOW", on_close)

# Create picture for header
park_image = Image.open("phouse.png")
# resize picture to fit for the window
resized = park_image.resize((190, 140), Image.ANTIALIAS)
new_image = ImageTk.PhotoImage(resized)
# Create label for picture and place it on the grid
lab = Label(root, image=new_image, borderwidth=0)
lab.grid(row=0, column=0, sticky='n')

# Create main menu (root) buttons and their location on the grid
see_prices_button = Button(root, command=prices, height=1, width=70, relief="solid", text="View price list", font=('Verdana', 10), fg='#F5F5F5', bg='#36454F')
see_prices_button.grid(padx=30, pady=5, row='4', column='0', sticky='w')

start_parking_button = Button(root, command=start_parking, height=2, width=20, relief="solid", text="Start parking", font=('Verdana', 10), fg='#F5F5F5', bg='#2E8B57')
start_parking_button.grid(padx=30, pady=15, row='5', column='0', sticky='w')

status_parking_button = Button(root, command=car_status, height=2, width=22, relief="solid", text="Parked car status", font=('Verdana', 10), fg='#F5F5F5', bg='#3466a5')
status_parking_button.grid(padx=30, pady=15, row='5', column='0', sticky='n')

stop_parking_button = Button(root, command=stop_parking, height=2, width=20, relief="solid", text="Stop parking", font=('Verdana', 10), fg='#F5F5F5', bg='#8f1d21')
stop_parking_button.grid(padx=30, pady=15, row='5', column='0', sticky='e')

# Create black line below logo
c = Canvas(root, height=22, width=620, bg="black")
c.grid(row=1, column=0, pady=0)

# Create labels
welcome_label = Label(root, text="Welcome to YourPark!", font=('Verdana 12 bold'), bg='#F5F5F5', fg="black")
welcome_label.grid(row=3, column=0, sticky='n', padx=10, pady=16)
time_label = Label(root)
time_label.grid(row=1, column=0, sticky='w')
date_label = Label(root)
date_label.grid(row=1, column=0, sticky='e', padx=13)
park_space_label = Label(root, text='Available spots: ' + str(TOTAL_PARKING_SPACES), font=('Verdana', 10), fg="#FFBF00", bg='black')
park_space_label.grid(row=1, column=0, sticky='')

# Call time and date function for root menu
current_time_date()

# Create a connection to DB
conn = sqlite3.connect('park.db')

# Create cursor
cur = conn.cursor()

# Update total parking spaces depending on amount of parked cars stored i the db.
cur.execute("SELECT COUNT (*) FROM parked_cars")
parked_cars_amount = cur.fetchall()
TOTAL_PARKING_SPACES = TOTAL_PARKING_SPACES - parked_cars_amount[0][0]
park_space_label.config(text='Available spots: ' + str(TOTAL_PARKING_SPACES))

# Enable foreign keys
cur.execute("PRAGMA foreign_keys=1")


# SQL COMMANDS: Create the tables for database
def create_tables():
    """This function is used to create the tables for db"""
    # Driver table

    cur.execute("""CREATE TABLE IF NOT EXISTS driver (
        email TEXT PRIMARY KEY NOT NULL
            )""")

    # Car table
    cur.execute("""CREATE TABLE IF NOT EXISTS car (
        car_id TEXT(6) PRIMARY KEY NOT NULL,
        email TEXT,
        FOREIGN KEY (email) REFERENCES driver(email)
            )""")

    # Parked cars table
    cur.execute("""CREATE TABLE IF NOT EXISTS parked_cars (
        parked_car TEXT(6) UNIQUE NOT NULL,
        start_time timestamp DATETIME DEFAULT (datetime('now','localtime')),
        stop_time DATETIME DEFAULT 'ACTIVE',
        total_time INT,
        price INT,
        FOREIGN KEY (parked_car) REFERENCES car (car_id)
            )""")

# def clear_table():
#     cur.execute("DELETE FROM parked_cars")
#     cur.execute("DELETE FROM car;")

# clear_table()
# Call the create tables function
# create_tables()

# Commit changes
conn.commit()

# Close connection
conn.close()

# Run tkinter window
root.mainloop()
