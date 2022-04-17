from tkinter import *
import sqlite3
from time import strftime
import re
from tkinter import Tk, Frame, Canvas
from PIL import ImageTk,Image

# Function to validate reg_num
# carReg=("abc123")

# if re.match(r"^[A-Za-z]{3}[0-9]{2}[0-9A-Za-z]{1}$", carReg):
#     print("Valid")
# else:
#     print("Invalid")


# Create tkinter window
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


# Function to show date and keep time dynamic
def current_time_date():
    my_time=strftime(' Local time: %H:%M:%S')
    time_label.config(text=str(my_time), font=("Verdana", 10), fg="White",bg="black")
    time_label.after(1000, current_time_date)
    todays_date= strftime('Date: %d/%m/%y')
    date_label.config(text=str(todays_date), font=("Verdana", 10), fg="White",bg="black")

# Parking spaces variable
total_parking_spaces= 50

# Create picture
park_image = Image.open("phouse.png")
resized = park_image.resize((190, 140), Image.ANTIALIAS)
new_image=ImageTk.PhotoImage(resized)
lab= Label(root, image=new_image, borderwidth=0)
lab.grid(row=0, column=0, sticky='n')

# Create buttons
see_prices_button=Button(root, height=1, width=70, relief="solid", text="View price list", font=('Verdana', 10), fg='#F5F5F5', bg='#36454F')
see_prices_button.grid(padx= 30, pady= 5, row='4', column='0', sticky='w')

start_parking_button=Button(root, height=2, width=20, relief="solid", text="Start parking", font=('Verdana', 10), fg='#F5F5F5', bg='#2E8B57')
start_parking_button.grid(padx= 30, pady= 15, row='5', column='0', sticky='w')

status_parking_button=Button(root, height=2, width=22, relief="solid", text="See status for parked car", font=('Verdana', 10), fg='#F5F5F5', bg='#3466a5')
status_parking_button.grid(padx= 30, pady= 15, row='5', column='0', sticky='n')

stop_parking_button=Button(root, height=2, width=20, relief="solid", text="Stop parking", font=('Verdana', 10), fg='#F5F5F5', bg='#8f1d21')
stop_parking_button.grid(padx= 30, pady= 15, row='5', column='0', sticky='e')

# Create black line below logo
c = Canvas(root, height=22,width=620, bg="black")
c.grid(row=1,column=0)
# Create labels
welcome_label=Label(root, text="Hello and welcome to the parking lot!\n\nPlease choose from the options below..", font=('Verdana', 10), bg='#F5F5F5', fg="black")
welcome_label.grid(row=3, column=0, sticky='n', padx=10, pady=10)
time_label=Label(root)    
time_label.grid(row=1, column=0, sticky='w')
date_label=Label(root)
date_label.grid(row=1, column=0, sticky='e', padx=13)

current_time_date()
park_space_label=Label(root, text='Available spots: ' + str(total_parking_spaces), font=('Verdana', 10), fg="#FFBF00", bg='black')
park_space_label.grid(row=1, column=0, sticky='')


# Create a connection to DB
conn = sqlite3.connect('park.db')

# Create cursor
cur = conn.cursor()

# Create users table
# cur.execute("""CREATE TABLE IF NOT EXISTS car (
#     email text,
#     car_reg_nr text,
#     park_time_start text,
#     park_time_end text,
#     price integer 
#         )""")

# Commit changes
conn.commit()

# Close connection
conn.close()

# Run tkinter window
root.mainloop()