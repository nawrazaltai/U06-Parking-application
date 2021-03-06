"""Parking application"""
# from tkinter import *
from email.mime import image
from tkinter import Label, LabelFrame, Toplevel, StringVar, Entry, END, Button, messagebox, Tk, Canvas, TclError, Message
import tkinter
import customtkinter
import sqlite3
from time import strftime
import re
import time
from turtle import bgcolor
# from tkinter import Tk, Canvas
# from tkinter import messagebox
from PIL import ImageTk, Image
from psycopg import Column

#customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
#customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

# Create main window called root
root = customtkinter.CTk()
# root title
root.title("Parking application")
# root size
#root.geometry("620x650")
#root.attributes("-fullscreen", True)
root.state('zoomed')
# make the window not resizable
root.resizable(width=False, height=False)
# background color for window
root.configure(bg="silver")
# icon for application window (top left corner)
root.iconbitmap('pics/phouse.ico')

# Parking spaces variable
TOTAL_PARKING_SPACES = 50

# Create frame for logo to be placed on
frame_logo = customtkinter.CTkFrame(master=root,
                               width=100,
                               height=100,
                               corner_radius=5,
                               fg_color='',
                               border_width=0,
                               bg_color='silver')
frame_logo.grid(row=0, column=0, sticky='w', pady= 10)

# resize main logo
logo_image = ImageTk.PhotoImage(Image.open("pics/greylogo.png").resize((230, 230), Image.ANTIALIAS))

# Create label for picture and place it on the grid
lab = customtkinter.CTkLabel(master=frame_logo, image=logo_image, borderwidth=0, corner_radius=10, fg_color="silver", bg_color='silver')
lab.grid(row=0, column=0, sticky='w')
lab.grid_rowconfigure(0, weight=1)
lab.grid_columnconfigure(0, weight=1)

# # Frame for date, time, availabe spots
frame_info = customtkinter.CTkFrame(master=root,
                               width=360,
                               height=160,
                               border_color='white',
                               border_width=1,
                               corner_radius=8,
                               fg_color='grey')
frame_info.grid(row=0, column=0, sticky='ne', pady=10, padx=20)
frame_info.grid_columnconfigure(1, weight=0)
frame_info.grid_rowconfigure(1, weight=1)

# Grey frame below logo and time/date
grey_frame = customtkinter.CTkFrame(master=root,
                               width=1290,
                               height=2,
                               corner_radius=1,
                               bg_color='silver',
                               fg_color='grey')
grey_frame.grid(row=1, column=0, padx=0, pady=0, sticky='w')

# Function to disable root buttons
def disable_main_buttons():
    start_button.configure(state=tkinter.DISABLED)
    stop_button.configure(state=tkinter.DISABLED)
    status_button.configure(state=tkinter.DISABLED)

# Function to activate root buttons
def enable_main_buttons():
    start_button.configure(state=tkinter.NORMAL)
    stop_button.configure(state=tkinter.NORMAL)
    status_button.configure(state=tkinter.NORMAL)

# Resize pictures for logos
today_logo = ImageTk.PhotoImage(Image.open("pics/today.png").resize((40, 40), Image.ANTIALIAS))
time_logo = ImageTk.PhotoImage(Image.open("pics/time.png").resize((40, 40), Image.ANTIALIAS))
reg_logo = ImageTk.PhotoImage(Image.open("pics/reg.png").resize((50, 50), Image.ANTIALIAS))
pay_logo = ImageTk.PhotoImage(Image.open("pics/price.png").resize((50, 50), Image.ANTIALIAS))
timer_logo = ImageTk.PhotoImage(Image.open("pics/timer.png").resize((50, 50), Image.ANTIALIAS))
car_status_logo = ImageTk.PhotoImage(Image.open("pics/here.png").resize((50, 50), Image.ANTIALIAS))
start_date_logo = ImageTk.PhotoImage(Image.open("pics/start_date.png").resize((50, 50), Image.ANTIALIAS))
exit_logo = ImageTk.PhotoImage(Image.open("pics/exit.png").resize((30, 30), Image.ANTIALIAS))
back_logo = ImageTk.PhotoImage(Image.open("pics/back.png").resize((30, 30), Image.ANTIALIAS))

# Function to show date
def current_date():
    """This function is for the main menu (root).

    The function shows the current date and stores it in the date_label."""
    # Store current date in the todays_date variable
    todays_date = strftime('%A %d-%m-%Y')

    # Create label for date
    date_label = customtkinter.CTkLabel(master=frame_info,
                               text=f' {todays_date}',
                               text_color= "black",
                               text_font=("Verdana 11"),
                               width=380,
                               height=35,
                               fg_color=("silver"),
                               bg_color=("grey"),
                               corner_radius=5)
    date_label.grid(row=1, column=1, sticky='w', padx=20, pady=5)
    today_lab = customtkinter.CTkLabel(master=date_label, image=today_logo, borderwidth=0, width=10, corner_radius=1, fg_color="silver", bg_color='silver')
    today_lab.grid(row=0, column=0, sticky='w', padx=78)

# Call the time_date function to show time & date on main screen
current_date()

def current_time():
    # Store current timestamp in the my_time variable
    my_time = strftime('%H:%M:%S')

    # Create label for time and keep it dynamic
    time_label = customtkinter.CTkLabel(master=frame_info,
                               text=f'{my_time}',
                               text_color= "black",
                               text_font=("Verdana 11"),
                               width=380,
                               height=35,
                               fg_color=("silver"),
                               bg_color=("grey"),
                               corner_radius=5)
    time_label.grid(row=0, column=1, sticky='nw', padx= 20, pady=5)
    time_logo_label = customtkinter.CTkLabel(master=time_label, image=time_logo, borderwidth=0, width=10, corner_radius=1, fg_color="silver", bg_color='silver')
    time_logo_label.grid(row=0, column=0, sticky='w', padx=128)
    time_label.after(1000, current_time)
current_time()


# Create label for availabe parking spots
space_label = customtkinter.CTkLabel(master=frame_info,
                               text=f"Available parking spots: {TOTAL_PARKING_SPACES}",
                               text_color= "indigo",
                               text_font=("Verdana 12 bold"),
                               width=380,
                               height=45,
                               fg_color=("silver"),
                               bg_color=("grey"),
                               corner_radius=5)
space_label.grid(row=2, column=1, sticky='sw', padx= 20, pady=5)

# Create frame for root buttons
buttons_frame = customtkinter.CTkFrame(master=root,
                               width=780,
                               height=350,
                               border_width=2,
                               border_color='white',
                               corner_radius=15,
                               bg_color='silver',
                               fg_color='#757575')
buttons_frame.grid(row=3, column=0, padx=0, pady=30, sticky='')

# Create label for welcome message
welcome_label = customtkinter.CTkLabel(master=buttons_frame,
                               text="Welcome to YourPark!",
                               text_color= "black",
                               text_font=("Verdana 15 bold"),
                               width=255,
                               height=40,
                               fg_color=("#757575"),
                               bg_color=("#757575"),
                               corner_radius=1)
welcome_label.grid(row=3, column=1, sticky='n', padx=105, pady=8)

# Resize start button logo
start_logo = ImageTk.PhotoImage(Image.open("pics/parking-icon-9.jpg").resize((90, 90), Image.ANTIALIAS))

# Resize logo for start_pop_up
logo_image_in_start = ImageTk.PhotoImage(Image.open("pics/greylogo.png").resize((150, 150), Image.ANTIALIAS))

# Variable for placeholder text belonging to entryboxes asking for regnum.
placeholder_text = 'XXXXXX (6 characters)'

# Start parking function
def start_parking_button():

    # Create new window called start_pop_up for start parking-button
    start_pop_up = customtkinter.CTkToplevel(root)
    start_pop_up.iconbitmap('pics/phouse.ico')
    start_pop_up.title("Start parking")
    start_pop_up.geometry("500x600")
    start_pop_up.resizable(width=False, height=False)
    start_pop_up.config(bg="silver")
    # Create frame for logo to be placed on
    frame_logo = customtkinter.CTkFrame(master=start_pop_up,
                               width=50,
                               height=50,
                               corner_radius=5,
                               fg_color='',
                               border_width=0,
                               bg_color='silver')
    frame_logo.grid(row=0, column=0, sticky='nw', pady = 3, padx=0)

    # Create label for picture and place it on the grid
    lab = customtkinter.CTkLabel(master=frame_logo, image=logo_image_in_start, borderwidth=0, corner_radius=10, fg_color="silver", bg_color='silver')
    lab.grid(row=0, column=0, sticky='w', pady=0)
    # lab.grid_rowconfigure(0, weight=1)
    # lab.grid_columnconfigure(0, weight=1)

    def on_close_start():
        start_button.configure(state=tkinter.NORMAL)
        stop_button.configure(state=tkinter.NORMAL)
        status_button.configure(state=tkinter.NORMAL)
        start_pop_up.destroy()

    # Create button to return to main menu
    back_status_button = customtkinter.CTkButton(master=start_pop_up,
                                 width=10,
                                 height=20,
                                 border_width=1,
                                 corner_radius=10,
                                 fg_color='#757575',
                                 hover_color='#757575',
                                 border_color='white',
                                 text="Back to main menu",
                                 text_color='black',
                                 text_color_disabled='grey',
                                 text_font='Verdana 10',
                                 image= back_logo,
                                 compound='left',
                                 command=on_close_start)
    back_status_button.grid(column=0, row=0, pady=12, padx=100, sticky='se')


    # Grey frame (line) below logo in start_pop_up
    grey_frame = customtkinter.CTkFrame(master=start_pop_up,
                               width=600,
                               height=2,
                               corner_radius=1,
                               bg_color='silver',
                               fg_color='grey')
    grey_frame.grid(row=1, column=0, padx=0, pady=0, sticky='w')

    # Frame to place entry box in start_pop_up
    frame = customtkinter.CTkFrame(master=start_pop_up,
                               width=490,
                               height=100,
                               border_width=1,
                               border_color='white',
                               bg_color='silver',
                               fg_color='#757575',
                               corner_radius=10)
    frame.grid(row=2, column= 0,padx=90, pady=20, sticky="w")

    # Label with 'enter reg num below'
    start_label = customtkinter.CTkLabel(master=frame,
                               text="Enter your registration number below",
                               text_color= "black",
                               text_font=("Verdana 10 bold"),
                               width=255,
                               height=40,
                               fg_color=("#757575"),
                               bg_color=("#757575"),
                               corner_radius=1)
    start_label.grid(row=2, column=0, sticky='n', padx=0, pady=8)

    # Entry box for regnum
    entry_text = tkinter.StringVar()
    entry_regnum = customtkinter.CTkEntry(master=frame,
                                textvariable=entry_text,
                                placeholder_text_color='black',
                                placeholder_text='XXXXXX (6 Characters)',
                                width=300,
                                text_color='black',
                                text_font=("Verdana 11"),
                                bg_color='#757575',
                                fg_color='silver',
                                corner_radius=5)
    entry_regnum.grid(row=3, column=0, padx=10, pady=8)
    # Create placeholder text for regnum entry
    entry_regnum.insert(0, placeholder_text)
    entry_regnum.bind("<FocusIn>", lambda args: entry_regnum.delete('0', 'end'))

    def character_limit(entry_text):
        if len(entry_text.get()) > 0:
            entry_text.set(entry_text.get().upper()[:6])
    entry_text.trace("w", lambda *args: character_limit(entry_text))

    def start_click():
        date_time = strftime("%A - %m/%d/%Y, %H:%M:%S")
        global TOTAL_PARKING_SPACES

        # Create a connection to DB
        connection = sqlite3.connect('park.db')

        # Create cursor
        cursor = connection.cursor()

        # Check if reg num is valid
        regnum = entry_text.get()
        if re.match(r"^[A-Za-z]{3}[0-9]{2}[0-9A-Za-z]{1}$", regnum):
            # Check if reg num is already in the database, if yes -> showerror.
            cursor.execute("SELECT car_id FROM car WHERE car_id=?", (regnum,))
            result = cursor.fetchone()
            if result:
                messagebox.showerror(title='Already in use,', message=f'{regnum} is already in use!\nPlease try again with a different registration number.')
                start_pop_up.destroy()
                enable_main_buttons()
            # If reg num is valid and unique insert into car and parked_cars table
            else:
                cursor.execute("INSERT INTO car (car_id) VALUES (?)", (regnum,))
                cursor.execute("INSERT INTO parked_cars (parked_car) VALUES (?)", (regnum,))
                TOTAL_PARKING_SPACES -= 1
            # Commit changes
                connection.commit()
            # Clear entry box
                entry_regnum.delete(0, END)
                space_label.config(text='Available parking spots: ' + str(TOTAL_PARKING_SPACES))
                messagebox.showinfo(title='Park started', message=f'Parking for {regnum} started at {date_time}')
        else:
            messagebox.showerror(title='Not valid', message=f'{regnum} is not a valid registration number!\nPlease try again.')
            entry_regnum.delete(0, END)
        # Close window and activate root menu buttons
        start_pop_up.destroy()
        enable_main_buttons()

    start_click_button = customtkinter.CTkButton(master=frame,
                                 width=300,
                                 height=30,
                                 border_width=1,
                                 corner_radius=10,
                                 fg_color='#378936',
                                 hover_color='#30694B',
                                 border_color='white',
                                 text="Start parking",
                                 text_color='white',
                                 text_color_disabled='grey',
                                 text_font='Verdana 11 bold',
                                 command=start_click)
    start_click_button.grid(row=4, column=0, pady=10, padx=5, sticky='')    
    # Disable root buttons
    disable_main_buttons()

    # Function to activate root buttons when start_pop_up closes
    def on_close():
        start_button.configure(state=tkinter.NORMAL)
        stop_button.configure(state=tkinter.NORMAL)
        status_button.configure(state=tkinter.NORMAL)
        start_pop_up.destroy()
    start_pop_up.protocol("WM_DELETE_WINDOW", on_close)

# Create start button placed at buttons_frame in root
start_button = customtkinter.CTkButton(master=buttons_frame,
                                 width=360,
                                 height=80,
                                 border_width=2,
                                 corner_radius=10,
                                 fg_color='#378936',
                                 hover_color='#30694B',
                                 border_color='white',
                                 text="Start parking",
                                 text_color='white',
                                 text_color_disabled='grey',
                                 text_font='Verdana 12 bold',
                                 image=start_logo,
                                 compound='right',
                                 command=start_parking_button)
start_button.grid(column=0, row=4, pady=20, padx=5, sticky='w')

# Resize status logo
status_logo = ImageTk.PhotoImage(Image.open("pics/checkout.png").resize((100, 100), Image.ANTIALIAS))

def status_parking_button():
    #reg_logo = ImageTk.PhotoImage(Image.open("abc.png").resize((40, 40), Image.ANTIALIAS))
    # Create new window called start_pop_up for start parking-button
    status_pop_up = customtkinter.CTkToplevel(root)
    status_pop_up.iconbitmap('pics/phouse.ico')
    status_pop_up.title("Start parking")
    status_pop_up.geometry("700x600")
    #status_pop_up.state('zoomed')
    status_pop_up.resizable(width=False, height=False)
    status_pop_up.config(bg="silver")
    

    # Disable root buttons while in status_pop_up
    disable_main_buttons()

    # Create frame for logo to be placed on
    frame_logo = customtkinter.CTkFrame(master=status_pop_up,
                               width=50,
                               height=50,
                               corner_radius=5,
                               fg_color='',
                               border_width=0,
                               bg_color='silver')
    frame_logo.grid(row=0, column=0, sticky='nw', pady = 3, padx=0)

    # Create label for p-logo and place it on the grid
    lab = customtkinter.CTkLabel(master=frame_logo, image=logo_image_in_start, borderwidth=0, corner_radius=10, fg_color="silver", bg_color='silver')
    lab.grid(row=0, column=0, sticky='w', pady=0)
    # lab.grid_rowconfigure(0, weight=1)
    # lab.grid_columnconfigure(0, weight=1)

    def on_close():
        status_pop_up.destroy()
        start_button.configure(state=tkinter.NORMAL)
        stop_button.configure(state=tkinter.NORMAL)
        status_button.configure(state=tkinter.NORMAL)

    # Create button to return to main menu
    back_status_button = customtkinter.CTkButton(master=status_pop_up,
                                 width=10,
                                 height=20,
                                 border_width=1,
                                 corner_radius=10,
                                 fg_color='#757575',
                                 hover_color='#757575',
                                 border_color='white',
                                 text="Back to main menu",
                                 text_color='black',
                                 text_color_disabled='grey',
                                 text_font='Verdana 10',
                                 image= back_logo,
                                 compound='left',
                                 command=on_close)
    back_status_button.grid(column=0, row=0, pady=12, padx=10, sticky='se')


    # Grey frame (line) below logo in start_pop_up
    grey_frame = customtkinter.CTkFrame(master=status_pop_up,
                               width=700,
                               height=2,
                               corner_radius=1,
                               bg_color='silver',
                               fg_color='grey')
    grey_frame.grid(row=1, column=0, padx=0, pady=0, sticky='w')

    # Frame to place entry box in status_pop_up
    frame = customtkinter.CTkFrame(master=status_pop_up,
                               width=500,
                               height=100,
                               border_width=1,
                               border_color='white',
                               bg_color='silver',
                               fg_color='#757575',
                               corner_radius=10)
    frame.grid(row=2, column= 0,padx=130, pady=10, sticky="w")

    # Label with 'enter reg num below'
    status_label = customtkinter.CTkLabel(master=frame,
                               text="Enter your registration number below",
                               text_color= "black",
                               text_font=("Verdana 10 bold"),
                               width=255,
                               height=40,
                               fg_color=("#757575"),
                               bg_color=("#757575"),
                               corner_radius=1)
    status_label.grid(row=0, column=0, sticky='n', padx=0, pady=2)

    # Entry box for regnum
    entry_text_status = tkinter.StringVar()
    entry_regnum_status = customtkinter.CTkEntry(master=frame,
                                textvariable=entry_text_status,
                                width=400,
                                text_color='black',
                                text_font=("Verdana 11"),
                                bg_color='#757575',
                                fg_color='silver',
                                corner_radius=5)
    entry_regnum_status.grid(row=1, column=0, padx=10, pady=10, sticky='n')

    # Create placeholder text for regnum entry and delete placeholder text when clicked in entry.
    entry_regnum_status.insert(0, placeholder_text)
    entry_regnum_status.bind("<FocusIn>", lambda args: entry_regnum_status.delete('0', 'end'))
    
    # limit entry text to 6 uppercase chars.
    def character_limit(entry_text):
        if len(entry_text.get()) > 0:
            entry_text.set(entry_text.get().upper()[:6])
    entry_text_status.trace("w", lambda *args: character_limit(entry_text_status))

    def status_click():
        # Disable 'check status'-button when info about car is shown
        status_click_button.configure(state=tkinter.DISABLED)
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
                stop_time = "Parking status: " + str(car_info[2])
                # Show total parking time, if time < 60min ---> show in minutes, if time > 60min ---> show in hours
                if parked_time[0] <= 59:
                    total_time = "Total parking time: " + str(round(parked_time[0])) + ' minutes'
                    #print(total_time)
                elif parked_time[0] >= 60:
                    a = (round(parked_time[0] / 60, 2))
                    b = a - int(a)
                    total_time = "Total parking time: " + str(int(parked_time[0] / 60)) + " hours & " + str(round(b*60)) + " minutes"

                # Variable for pricing for a parked car (0-60min FREE)
                if parked_time[0] <= 60:
                    price = "Current price: " + str(round(parked_time[0] * 0)) + ' SEK'
                # Price for 61 min onwards ---> 0.25kr/min, REMOVES FIRST FREE HOUR)
                elif parked_time[0] >= 61:
                    price = "Current price: " + str(round((parked_time[0] - 60) * (0.25), 1)) + ' SEK'
                    #print(price)

                back_status_button.configure(state=tkinter.DISABLED)

                # Create frame for each info section displayed when clicking check status 
                summary_frame = customtkinter.CTkFrame(master=status_pop_up,
                               width=500,
                               height=100,
                               border_width=1,
                               border_color='white',
                               bg_color='silver',
                               fg_color='#757575',
                               corner_radius=10)
                summary_frame.grid(row=3, column= 0,padx=130, pady=0, sticky='w')
                
                frame1 = customtkinter.CTkFrame(master=summary_frame,
                               width=200,
                               height=200,
                               border_width=1,
                               border_color='white',
                               bg_color='#757575',
                               fg_color='#757575',
                               corner_radius=10)
                frame1.grid(row=5, column= 0,padx=10, pady=5, sticky="w")
                
                frame2 = customtkinter.CTkFrame(master=summary_frame,
                               width=200,
                               height=200,
                               border_width=1,
                               border_color='white',
                               bg_color='#757575',
                               fg_color='#757575',
                               corner_radius=10)
                frame2.grid(row=6, column= 0,padx=10, pady=5, sticky="w")

                frame3 = customtkinter.CTkFrame(master=summary_frame,
                               width=200,
                               height=200,
                               border_width=2,
                               border_color='#1E5631',
                               bg_color='#757575',
                               fg_color='#757575',
                               corner_radius=10)
                frame3.grid(row=7, column= 0,padx=10, pady=5, sticky="w")

                frame4 = customtkinter.CTkFrame(master=summary_frame,
                               width=400,
                               height=200,
                               border_width=1,
                               border_color='white',
                               bg_color='#757575',
                               fg_color='#757575',
                               corner_radius=10)
                frame4.grid(row=8, column= 0, padx=10, pady=5, sticky="w")

                frame5 = customtkinter.CTkFrame(master=summary_frame,
                               width=200,
                               height=200,
                               border_width=1,
                               border_color='white',
                               bg_color='#757575',
                               fg_color='#757575',
                               corner_radius=10)
                frame5.grid(row=9, column= 0,padx=10, pady=5, sticky="w")

                # Create labels for regnum text and logo
                car_reg_label = customtkinter.CTkLabel(frame1, text=car_reg, corner_radius=1, bg_color='#757575', text_font=("Verdana 11"), text_color='black')
                car_reg_label.grid(row=0, column= 0,padx=40, pady=7, sticky="")
                reg_lab = customtkinter.CTkLabel(master=frame1, image=reg_logo, borderwidth=0, width=10, corner_radius=1, bg_color='#757575')
                reg_lab.grid(row=0, column=0, sticky='w', padx=3)
                
                # Create labels for start_time text and logo
                start_time_label = customtkinter.CTkLabel(frame2, text=start_time, bg_color='#757575', text_font=("Verdana 11"), text_color='black')
                start_time_label.grid(row=0, column= 0,padx=40, pady=7, sticky="n")
                start_lab = customtkinter.CTkLabel(master=frame2, image=start_date_logo, borderwidth=0, width=10, corner_radius=1, bg_color='#757575')
                start_lab.grid(row=0, column=0, sticky='w', padx=3)
                
                # Create labels for stop_time/status text and logo
                stop_time_label = customtkinter.CTkLabel(frame3, text=stop_time, bg_color='#757575', text_font=("Verdana 11"), text_color='black')
                stop_time_label.grid(row=0, column= 0,padx=40, pady=7, sticky="w")
                status_lab = customtkinter.CTkLabel(master=frame3, image=car_status_logo, borderwidth=0, width=10, corner_radius=1, bg_color='#757575')
                status_lab.grid(row=0, column=0, sticky='w', padx=3)
                
                # Create labels for total_time text and logo
                total_time_label = customtkinter.CTkLabel(frame4, text=total_time, bg_color='#757575', text_font=("Verdana 11"), text_color='black')
                total_time_label.grid(row=0, column= 0,padx=39, pady=7, sticky="n")
                timer_lab = customtkinter.CTkLabel(master=frame4, image=timer_logo, borderwidth=0, width=10, corner_radius=1, bg_color='#757575')
                timer_lab.grid(row=0, column=0, sticky='w', padx=3)
                
                # Create labels for price text and logo
                price_label = customtkinter.CTkLabel(frame5, text=price, bg_color='#757575', text_font=("Verdana 11"), text_color='black')
                price_label.grid(row=0, column= 0,padx=40, pady=7, sticky="n")
                pay_lab = customtkinter.CTkLabel(master=frame5, image=pay_logo, borderwidth=0, width=10, corner_radius=1, bg_color='#757575')
                pay_lab.grid(row=0, column=0, sticky='w', padx=3)

                # Clear entry box after click on 'check status'
                entry_regnum_status.delete(0, END)

                # Create the 'check car status'-button for status_pop_upz
                exit_status_button = customtkinter.CTkButton(master=status_pop_up,
                                 width=422,
                                 height=40,
                                 border_width=1,
                                 corner_radius=10,
                                 fg_color='#757575',
                                 hover_color='#757575',
                                 border_color='white',
                                 text="Exit",
                                 text_color='black',
                                 text_color_disabled='grey',
                                 text_font='Verdana 11 bold',
                                 image= exit_logo,
                                 compound='right',
                                 command=on_close)
                exit_status_button.grid(column=0, row=4, pady=12, padx=130, sticky='w')

            # If regnum is valid but not in db, show error message.
            elif not car_info:
                messagebox.showerror(title='Car not found', message=f'Car with registration number: {regnum} not found')
                status_pop_up.destroy()
                enable_main_buttons()
        # If regnum is not in valid format, show error message.
        else:
            messagebox.showerror(title='Not valid', message=f'{regnum} is not a valid registration number\nPlease try again.')
            entry_regnum_status.delete(0, END)
            status_pop_up.destroy()
            enable_main_buttons()
        # Commit changes
        con.commit()
    # Create the 'check car status'-button for status_pop_up    
    status_click_button = customtkinter.CTkButton(master=frame,
                                 width=400,
                                 height=30,
                                 border_width=1,
                                 corner_radius=10,
                                 fg_color='#2565AE',
                                 hover_color='#253DA1',
                                 border_color='white',
                                 text="Check car status",
                                 text_color='white',
                                 text_color_disabled='grey',
                                 text_font='Verdana 11 bold',
                                 command=status_click)
    status_click_button.grid(column=0, row=4, pady=10, padx=5)

    # Function to activate root buttons when status_pop_up closes
    def on_close():
        status_pop_up.destroy()
        start_button.configure(state=tkinter.NORMAL)
        stop_button.configure(state=tkinter.NORMAL)
        status_button.configure(state=tkinter.NORMAL)
    #status_pop_up.protocol("WM_DELETE_WINDOW", on_close) ## <-- To close pop up with 'x' button on windows manager.

# Create status button for root
status_button = customtkinter.CTkButton(master=buttons_frame,
                                 width=380,
                                 height=80,
                                 border_width=2,
                                 corner_radius=10,
                                 fg_color='#2565AE',
                                 hover_color='#253DA1',
                                 border_color='white',
                                 text="Parked car status",
                                 text_color='white',
                                 text_color_disabled='grey',
                                 text_font='Verdana 12 bold',
                                 image=status_logo,
                                 compound='right',
                                 command=status_parking_button)
status_button.grid(column=1, row=4, pady=8, padx=0)

# Resize stop logo
stop_logo = ImageTk.PhotoImage(Image.open("pics/barrier.png").resize((80, 80), Image.ANTIALIAS))

def stop_parking_button():
    print("button pressed")
stop_button = customtkinter.CTkButton(master=buttons_frame,
                                 width=360,
                                 height=80,
                                 border_width=2,
                                 corner_radius=10,
                                 fg_color='#D1001F',
                                 hover_color='#BC5449',
                                 border_color='white',
                                 text="Checkout",
                                 text_color='white',
                                 text_color_disabled='grey',
                                 text_font='Verdana 12 bold',
                                 image=stop_logo,
                                 compound='right',
                                 command=stop_parking_button)
stop_button.grid(column=2, row=4, pady= 0, padx=5, sticky='e')

# Create frame inside buttons_frame for the price list information
price_frame = customtkinter.CTkFrame(master=buttons_frame,
                               width=500,
                               height=150,
                               corner_radius=10,
                               border_width=3,
                               border_color='white',
                               fg_color='grey')
price_frame.grid(row=5, column=1, padx=0, pady=30, sticky='n')

# Create label for the price list
price_label = customtkinter.CTkLabel(master=buttons_frame,
                               text="Price list:\n\nMinute 0 - 60 are FREE of charge.\n"
                               "\n\nFrom minute 61 onwards the price is 0.25 SEK/min (15 SEK/hour).",
                               text_color= "black",
                               text_font=("Verdana 10"),
                               width=10,
                               height=40,
                               bg_color=("grey"),
                               corner_radius=10)
price_label.grid(row=5, column=1, sticky='n', padx=0, pady=50)


# Create a connection to DB
conn = sqlite3.connect('park.db')

# Create cursor
cur = conn.cursor()

# Update total parking spaces depending on amount of parked cars stored i the db.
cur.execute("SELECT COUNT (*) FROM parked_cars")
parked_cars_amount = cur.fetchall()
TOTAL_PARKING_SPACES = TOTAL_PARKING_SPACES - parked_cars_amount[0][0]
space_label.configure(text='Available parking spots: ' + str(TOTAL_PARKING_SPACES))

# Enable foreign keys
# cur.execute("PRAGMA foreign_keys=1")

# SQL COMMANDS: Create the tables for database
# def create_tables():
#     """This function is used to create the tables for db"""
#     # Driver table

#     cur.execute("""CREATE TABLE IF NOT EXISTS driver (
#         email TEXT PRIMARY KEY NOT NULL
#             )""")

#     # Car table
#     cur.execute("""CREATE TABLE IF NOT EXISTS car (
#         car_id TEXT(6) PRIMARY KEY NOT NULL,
#         email TEXT,
#         FOREIGN KEY (email) REFERENCES driver(email)
#             )""")

#     # Parked cars table
#     cur.execute("""CREATE TABLE IF NOT EXISTS parked_cars (
#         parked_car TEXT(6) UNIQUE NOT NULL,
#         start_time timestamp DATETIME DEFAULT (datetime('now','localtime')),
#         stop_time DATETIME DEFAULT 'ACTIVE',
#         total_time INT,
#         price INT,
#         FOREIGN KEY (parked_car) REFERENCES car (car_id)
#             )""")

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

# run the application
root.mainloop()