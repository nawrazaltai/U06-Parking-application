"""Parking application"""
# from tkinter import *
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

customtkinter.set_appearance_mode("light")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

# Create main window called root
root = customtkinter.CTk()
# root title
root.title("Parking application")
# root size
#root.geometry("620x650")
root.attributes("-fullscreen", True)
#root.state('zoomed')
# make the window not resizable
root.resizable(width=False, height=False)
# background color for window
root.configure(bg="silver")
# icon for application window (top left corner)
root.iconbitmap('phouse.ico')

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

# resize logo
logo_image = ImageTk.PhotoImage(Image.open("greylogo.png").resize((230, 230), Image.ANTIALIAS))

# Create label for picture and place it on the grid
lab = customtkinter.CTkLabel(master=frame_logo, image=logo_image, borderwidth=0, corner_radius=10, fg_color="silver", bg_color='silver')
lab.grid(row=0, column=0, sticky='w')
lab.grid_rowconfigure(0, weight=1)
lab.grid_columnconfigure(0, weight=1)

# # Frame for date, time, availabe spots
frame_info = customtkinter.CTkFrame(master=root,
                               width=360,
                               height=160,
                               corner_radius=8,
                               fg_color='grey')
frame_info.grid(row=0, column=0, sticky='ne', pady=10, padx=20)
frame_info.grid_columnconfigure(1, weight=0)
frame_info.grid_rowconfigure(1, weight=1)


# # Grey frame below logo and time/date
grey_frame = customtkinter.CTkFrame(master=root,
                               width=1290,
                               height=2,
                               corner_radius=1,
                               bg_color='silver',
                               fg_color='grey')
grey_frame.grid(row=1, column=0, padx=0, pady=0, sticky='w')

# # Function to show date and keep time dynamic at root
def current_time_date():
    """This function is for the main menu (root).

    It keeps the time dynamic and stores it in the time_label.

    The function also shows the current date and stores it in the date_label."""
    my_time = strftime(' Local time: %H:%M:%S')
    # time_label.config(text=str(my_time), font=("Verdana", 10), fg="White", bg="black")
    # time_label.after(1000, current_time_date)
    # todays_date = strftime('Date: %d/%m/%y')
    # date_label.config(text=str(todays_date), font=("Verdana", 10), fg="White", bg="black")
    time_label = customtkinter.CTkLabel(master=frame_info,
                               text=f'{my_time}',
                               text_color= "black",
                               text_font=("Verdana 11"),
                               width=380,
                               height=35,
                               fg_color=("silver"),
                               bg_color=("grey"),
                               corner_radius=5)
    time_label.after(1000, current_time_date)
    time_label.grid(row=0, column=1, sticky='nw', padx= 20, pady=5)

    todays_date = strftime('Date: %d-%m-%Y')
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

# Call the time_date function to show time & date on main screen
current_time_date()

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

welcome_label = customtkinter.CTkLabel(master=root,
                               text="Welcome to YourPark!",
                               text_color= "black",
                               text_font=("Verdana 15 bold"),
                               width=255,
                               height=40,
                               fg_color=("silver"),
                               bg_color=("silver"),
                               corner_radius=1)
welcome_label.grid(row=3, column=0, sticky='s', padx=105, pady=8)

start_logo = ImageTk.PhotoImage(Image.open("parking-icon-9.jpg").resize((90, 90), Image.ANTIALIAS))

def start_button():
    print("button pressed")
button = customtkinter.CTkButton(master=root,
                                 width=380,
                                 height=80,
                                 border_width=2,
                                 corner_radius=10,
                                 fg_color='#378936',
                                 hover_color='#30694B',
                                 border_color='black',
                                 text="Start parking",
                                 text_color='white',
                                 text_font='Verdana 12 bold',
                                 image=start_logo,
                                 compound='right',
                                 command=start_button)
button.grid(column=0, row=4, pady=20, padx=50, sticky='w')

status_logo = ImageTk.PhotoImage(Image.open("status.png").resize((100, 100), Image.ANTIALIAS))
def status_button():
    print("button pressed")
button = customtkinter.CTkButton(master=root,
                                 width=380,
                                 height=80,
                                 border_width=2,
                                 corner_radius=10,
                                 fg_color='#1035AC',
                                 hover_color='#0E4D92',
                                 border_color='black',
                                 text="Car status",
                                 text_color='white',
                                 text_font='Verdana 12 bold',
                                 image=status_logo,
                                 compound='right',
                                 command=status_button)
button.grid(column=0, row=4, pady= 0, padx=50)

stop_logo = ImageTk.PhotoImage(Image.open("checkout.png").resize((100, 100), Image.ANTIALIAS))
def stop_button():
    print("button pressed")
button = customtkinter.CTkButton(master=root,
                                 width=380,
                                 height=80,
                                 border_width=2,
                                 corner_radius=10,
                                 fg_color='red',
                                 hover_color='#BC5449',
                                 border_color='black',
                                 text="Checkout",
                                 text_color='white',
                                 text_font='Verdana 12 bold',
                                 image=stop_logo,
                                 compound='right',
                                 command=stop_button)
button.grid(column=0, row=4, pady= 0, padx=50, sticky='e')



root.mainloop()