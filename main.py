from string import hexdigits
from tkinter import *
import sqlite3
from time import strftime
import re
from tkinter import Tk, Frame, Canvas
from tkinter import messagebox
from venv import create
from PIL import ImageTk,Image

# Create root window
root=Tk()
# name
root.title("Parking application")
# size, not resizable
root.geometry("620x650")
root.resizable(width=False, height=False)
# bg color for window
root.configure(bg="#F5F5F5")
# icon for application window
root.iconbitmap('phouse.ico')

# Parking spaces variable
total_parking_spaces=50

# Function to show date and keep time dynamic at root
def current_time_date():
    my_time=strftime(' Local time: %H:%M:%S')
    time_label.config(text=str(my_time), font=("Verdana", 10), fg="White",bg="black")
    time_label.after(1000, current_time_date)
    todays_date= strftime('Date: %d/%m/%y')
    date_label.config(text=str(todays_date), font=("Verdana", 10), fg="White",bg="black")

# Function to show info about prices (connected to the 'View price list'-button)
def prices():
    messagebox.showinfo("Price list", "Minute 0-60 are FREE of charge.\n\n"
                        "From minute 61 onwards the price is 0.25 SEK/min\n(15 SEK/hour).")

# Function that takes user to new window after clicking on start parking in root menu (connected to 'Start parking'-button)
def start_parking():
    global start_pop_up
    start_pop_up = Toplevel(root)
    start_pop_up.iconbitmap('phouse.ico')
    start_pop_up.title("Start parking")
    start_pop_up.geometry("400x200")
    start_pop_up.resizable(width=False,height=False)
    start_pop_up.config(bg="#F5F5F5")

    # Disable root menu buttons while inside start_pop_up
    if start_pop_up:
        start_parking_button.config(state='disabled')
        stop_parking_button.config(state='disabled')
        status_parking_button.config(state='disabled')

    # function to activate root menu buttons
    def activate_root_buttons():
        start_parking_button.config(state='normal')
        stop_parking_button.config(state='normal')
        status_parking_button.config(state='normal')

    # Function with messagebox(yes/no) before exiting start_pop_up 
    # enables root menu buttons after closing start_pop_up 
    def on_close():
        close = messagebox.askyesno(title="Exit", message="Are you sure you want to exit?")
        if close:
            activate_root_buttons()
            start_pop_up.destroy()
    start_pop_up.protocol("WM_DELETE_WINDOW",  on_close)

    # Label for the text that asks for users reg num.
    regnum_label = Label(start_pop_up, text="Please enter your registration number", font=("Verdana", 11), fg="black")
    regnum_label.pack(pady=20)

    # Entry box for user to type in reg num
    global entry_text
    global entry_regnum
    entry_text = StringVar()
    entry_regnum = Entry(start_pop_up, width=10, borderwidth=4, font=("Verdana", 9), textvariable=entry_text)
    entry_regnum.pack()

    # Function that limits reg num entry to 6 upper case characters.
    def character_limit(entry_text):
        if len(entry_text.get()) > 0:
            entry_text.set(entry_text.get().upper()[:6])
    entry_text.trace("w", lambda *args: character_limit(entry_text))
    
    # Function for start button, checks if reg num is valid
    def start_click():
        global total_parking_spaces
        date_time = strftime("%m/%d/%Y, %H:%M:%S")
        
        # Create a connection to DB
        conn = sqlite3.connect('park.db')
        
        # Create cursor
        cur = conn.cursor()

        # Enable foreign keys 
        #cur.execute("PRAGMA foreign_keys=1")

        # Check if reg num is valid
        regnum= entry_text.get()
        if re.match(r"^[A-Za-z]{3}[0-9]{2}[0-9A-Za-z]{1}$", regnum):
            # Check if reg num is already in the database
            cur.execute("SELECT car_id FROM car WHERE car_id=?", (regnum,))
            result=cur.fetchone()
            if result:
                messagebox.showerror(title='Already in use,', message=f'{regnum} is already in use!\nPlease try again with a different registration number.')
                start_pop_up.destroy()
                activate_root_buttons()
            # Insert reg num into car and parked_cars table if
            if not result: 
                cur.execute("INSERT INTO car (car_id) VALUES (?)", (regnum,))
                cur.execute("INSERT INTO parked_cars (parked_car) VALUES (?)", (regnum,))
                total_parking_spaces=total_parking_spaces-1
            # Commit changes
                conn.commit()
            # Clear entry box
                entry_regnum.delete(0, END)
                park_space_label.config(text='Available spots: ' + str(total_parking_spaces))
                messagebox.showinfo(title='Park started', message=f'Parking for {regnum} started at {date_time}')
        else:
            messagebox.showerror(title='Not valid', message=f'{regnum} is not a valid registration number\nPlease try again.')
            entry_regnum.delete(0, END)
        # Close window and activate root menu buttons
        start_pop_up.destroy()
        activate_root_buttons()
        
    # Create start button for start_pop_up
    start_button=Button(start_pop_up, command=start_click, height=0, width=30, relief="solid", text="Start parking", font=('Verdana', 10), fg='#F5F5F5', bg='#2E8B57')
    start_button.pack(pady=20)

# Function to see parked car status (connected to 'See status for parked car'-button)
def car_status():
    global status_pop_up
    status_pop_up = Toplevel(root)
    status_pop_up.iconbitmap('phouse.ico')
    status_pop_up.title("Status for parked car")
    status_pop_up.geometry("400x500")
    status_pop_up.resizable(width=False,height=False)
    status_pop_up.config(bg="#F5F5F5")

    # Label for the text that asks for users reg num.
    regnum_label = Label(status_pop_up, text="Please enter your registration number", font=("Verdana", 11), fg="black")
    regnum_label.pack(pady=20)

    global entry_text
    global entry_regnum
    entry_text = StringVar()
    entry_regnum = Entry(status_pop_up, width=10, borderwidth=4, font=("Verdana", 9), textvariable=entry_text)
    entry_regnum.pack()

    # Function that limits reg num entry to 6 upper case characters.
    def character_limit(entry_text):
        if len(entry_text.get()) > 0:
            entry_text.set(entry_text.get().upper()[:6])
    entry_text.trace("w", lambda *args: character_limit(entry_text))

    def status_click():
        # Create a connection to DB
        conn = sqlite3.connect('park.db')
        
        # Create cursor
        cur = conn.cursor()

        regnum= entry_text.get()
        if re.match(r"^[A-Za-z]{3}[0-9]{2}[0-9A-Za-z]{1}$", regnum):
            cur.execute("SELECT CAST ((JulianDay('now','localtime') - JulianDay(start_time)) * 24 * 60 As Integer) FROM parked_cars WHERE parked_car=?", (regnum,))
            parked_time=cur.fetchone()
            cur.execute("SELECT * FROM parked_cars WHERE parked_car=?", (regnum,))
            car_info=cur.fetchone()
            if car_info:
                # Variables to store reg num, start/stop time and price
                car_reg= "Registration number: " + str(car_info[0])
                start_time="Start date and time:" + str(car_info[1])
                stop_time="Stop date and time: " + str(car_info[2])
                total_time="Total parking time: " + str(parked_time[0]) + ' minutes'
                parked_time=int(parked_time)
                print(parked_time)
                #price="Price: " + eval(parked_time*0.25)
            
                # Labels for the variables above
                car_reg_label = Label(status_pop_up, text=car_reg, bg='#F5F5F5', font=("Verdana", 11))
                car_reg_label.pack()
                start_time_label = Label(status_pop_up, text=start_time, bg='#F5F5F5', font=("Verdana", 11))
                start_time_label.pack()
                stop_time_label = Label(status_pop_up, text=stop_time, bg='#F5F5F5', font=("Verdana", 11))
                stop_time_label.pack()
                total_time_label = Label(status_pop_up, text=total_time, bg='#F5F5F5', font=("Verdana", 11))
                total_time_label.pack()
                #price_label = Label(status_pop_up, text=price, bg='#F5F5F5', font=("Verdana", 11))
                #price_label.pack()
                # Clear entry box after click
                entry_regnum.delete(0, END)
            elif not car_info:
                messagebox.showerror(title='Car not found', message=f'Car with registration number: {regnum} not found')
        else:
            messagebox.showerror(title='Not valid', message=f'{regnum} is not a valid registration number\nPlease try again.')
            entry_regnum.delete(0, END)
        # Commit changes
        conn.commit()

    # Create start button for start_pop_up
    status_button=Button(status_pop_up, command=status_click, height=0, width=30, relief="solid", text="Check status", font=('Verdana', 10), fg='#F5F5F5', bg='#3466a5')
    status_button.pack(pady=20)

# Create picture for header
park_image = Image.open("phouse.png")
resized = park_image.resize((190, 140), Image.ANTIALIAS)
new_image=ImageTk.PhotoImage(resized)
lab= Label(root, image=new_image, borderwidth=0)
lab.grid(row=0, column=0, sticky='n')

# Create buttons and their location on the grid
see_prices_button=Button(root, command=prices, height=1, width=70, relief="solid", text="View price list", font=('Verdana', 10), fg='#F5F5F5', bg='#36454F')
see_prices_button.grid(padx= 30, pady= 5, row='4', column='0', sticky='w')

start_parking_button=Button(root, command=start_parking, height=2, width=20, relief="solid", text="Start parking", font=('Verdana', 10), fg='#F5F5F5', bg='#2E8B57')
start_parking_button.grid(padx= 30, pady= 15, row='5', column='0', sticky='w')

status_parking_button=Button(root, command=car_status, height=2, width=22, relief="solid", text="See status for parked car", font=('Verdana', 10), fg='#F5F5F5', bg='#3466a5')
status_parking_button.grid(padx= 30, pady= 15, row='5', column='0', sticky='n')

stop_parking_button=Button(root, height=2, width=20, relief="solid", text="Stop parking", font=('Verdana', 10), fg='#F5F5F5', bg='#8f1d21')
stop_parking_button.grid(padx= 30, pady= 15, row='5', column='0', sticky='e')

# Create black line below logo
c = Canvas(root, height=22,width=620, bg="black")
c.grid(row=1,column=0)

# Create labels
welcome_label=Label(root, text="Welcome to YourPark!\n\nPlease choose from the options below..", font=('Verdana', 10), bg='#F5F5F5', fg="black")
welcome_label.grid(row=3, column=0, sticky='n', padx=10, pady=10)
time_label=Label(root)    
time_label.grid(row=1, column=0, sticky='w')
date_label=Label(root)
date_label.grid(row=1, column=0, sticky='e', padx=13)
park_space_label=Label(root, text='Available spots: ' + str(total_parking_spaces), font=('Verdana', 10), fg="#FFBF00", bg='black')
park_space_label.grid(row=1, column=0, sticky='')

# Call time and date function for root menu
current_time_date()

# Create a connection to DB
conn = sqlite3.connect('park.db')

# Create cursor
cur = conn.cursor()

# Enable foreign keys 
cur.execute("PRAGMA foreign_keys=1")

# SQL COMMANDS: Create the tables for database
def create_tables():
    # Driver table

    cur.execute("""CREATE TABLE IF NOT EXISTS driver (
        email TEXT PRIMARY KEY NOT NULL
            )""")
    # Seeds for driver table
    # cur.execute("""INSERT INTO driver (email) 
    #     VALUES ('tester@test.se' 
    #         )""")
    # #cur.execute("DELETE FROM driver")

    # Car table
    cur.execute("""CREATE TABLE IF NOT EXISTS car (
        car_id TEXT(6) PRIMARY KEY NOT NULL,
        email TEXT,        
        FOREIGN KEY (email) REFERENCES driver(email) 
            )""")
    # Seeds for car table
    # cur.execute("""INSERT INTO car (car_id, email) 
    #     VALUES ('XYZ789', 'tester@test.se'
    #         )""")
    #cur.execute("DELETE FROM car")


    # Parking lot table
    # cur.execute("""CREATE TABLE IF NOT EXISTS parking_lot (
    #     park_name TEXT DEFAULT 'YourPark',
    #     park_address TEXT DEFAULT 'Test Street 17',
    #     park_city TEXT DEFAULT 'Stockholm',
    #     park_zip INT(6) DEFAULT 12345
    #         )""")

    # Om parking_lot table ska användas, ska raden nedan in i parked_cars table
    # FOREIGN KEY (park_name) REFERENCES parking_lot(park_name)

    # cur.execute("""INSERT INTO parking_lot VALUES (
    #         'YourPark', 'Test Address', 'Stockholm', '341639'
    #         )""")

    # Parked cars table
    cur.execute("""CREATE TABLE IF NOT EXISTS parked_cars (
        parked_car TEXT(6) UNIQUE NOT NULL,
        start_time timestamp DATETIME DEFAULT (datetime('now','localtime')),
        stop_time DATETIME DEFAULT 'ACTIVE',
        total_time INT,
        price INT,
        FOREIGN KEY (parked_car) REFERENCES car (car_id)
            )""")

    # cur.execute("""INSERT INTO parked_cars (park_name, parked_car, start_time) 
    #     VALUES ('YourPark','ABC123', datetime('now','localtime')
    #         )""")
    # cur.execute("""UPDATE parked_cars
    #         SET stop_time = datetime('now','localtime')
    #         WHERE parked_car = "XYZ789"
    #         """)

# Call the create tables function
#create_tables()

# Commit changes
conn.commit()

# Close connection
conn.close()

# Run tkinter window
root.mainloop()