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

customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

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
                               border_color='white',
                               border_width=1,
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

# # Function to show date and keep time dynamic at root
def current_time_date():
    """This function is for the main menu (root).

    It keeps the time dynamic and stores it in the time_label.

    The function also shows the current date and stores it in the date_label."""
    # Store current timestamp in the my_time variable
    my_time = strftime(' Local time: %H:%M:%S')

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
    time_label.after(1000, current_time_date)
    time_label.grid(row=0, column=1, sticky='nw', padx= 20, pady=5)

    # Store current date in the todays_date variable
    todays_date = strftime('Date: %A %d-%m-%Y')

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

# Call the time_date function to show time & date on main screen
current_time_date()

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

# Resize start logo
start_logo = ImageTk.PhotoImage(Image.open("parking-icon-9.jpg").resize((90, 90), Image.ANTIALIAS))

# Start parking function
def start_parking_button():

    # Create new window called start_pop_up for start parking-button
    start_pop_up = customtkinter.CTkToplevel(root)
    start_pop_up.iconbitmap('phouse.ico')
    start_pop_up.title("Start parking")
    start_pop_up.geometry("400x200")
    start_pop_up.resizable(width=False, height=False)
    start_pop_up.config(bg="silver")

    # Disable root buttons
    disable_main_buttons()



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
status_logo = ImageTk.PhotoImage(Image.open("checkout.png").resize((100, 100), Image.ANTIALIAS))

def status_parking_button():
    print("button pressed")
status_button = customtkinter.CTkButton(master=buttons_frame,
                                 width=380,
                                 height=80,
                                 border_width=2,
                                 corner_radius=10,
                                 fg_color='#2565AE', #009dff
                                 hover_color='#253DA1',
                                 border_color='white',
                                 text="Parked car status",
                                 text_color='white',
                                 text_color_disabled='grey',
                                 text_font='Verdana 12 bold',
                                 image=status_logo,
                                 compound='right',
                                 command=status_parking_button)
status_button.grid(column=1, row=4, pady= 0, padx=0)

# Resize stop logo
stop_logo = ImageTk.PhotoImage(Image.open("barrier.png").resize((80, 80), Image.ANTIALIAS))

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


# run the application
root.mainloop()