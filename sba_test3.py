from tkinter import *
import os
from tkinter import ttk

import sqlite3

conn = sqlite3.connect('user.db')
c = conn.cursor()

def table_test():
    global screen_table
    screen_table = Toplevel(screen)
    screen_table.title("dashboard")
    screen_table.geometry("1000x750")
    conn = sqlite3.connect('user.db')
    c = conn.cursor()
    c.execute("select * from user")
    e = Entry(screen_table, width=15, fg='blue', font=("Consolas", 13))     
    i=1
    for user in c: 
        for j in range(len(user)):
            e = Entry(screen_table, width=15, fg='blue', font=("Consolas", 13)) 
            e.grid(row=i, column=j) 
            e.insert(END, user[j])
        i=i+1

def admin_add_account():
    print("account added")

def delete_admin_screen_records():
    screen_records_admin.destroy()

def show_mainscreen():
    screen.deiconify()

def hide_mainscreen():
    screen.withdraw()

def delete2():
    screen2.destroy()

def delete3():
    screen3.destroy()

def delete4():
    screen4.destroy()

def delete5():
    screen5.destroy()

def log_out():
    screen_mainpage.destroy()
    screen.deiconify()
    
def manage_records():
    global screen_records_admin
    screen_records_admin = Toplevel(screen)
    screen_records_admin.title("dashboard")
    screen_records_admin.geometry("600x500")
    conn = sqlite3.connect('user.db')
    c = conn.cursor()
    c.execute("select * from user")
    records = c.fetchall()
    c.execute("select count(id) from user")
    user_id = c.fetchone()

    
    
    print_records = ''
    for record in records:
        print_records += str(record[0]) + " " + str(record[1])+ " " +str(record[2]) + " " + str(record[3]) + " " + str(record[4]) + " ""\n"

    
    query_label = Label(screen_records_admin, text=print_records, anchor="center", font = ("Consolas", 16))
    query_label.grid(row=1,column=0,columnspan=1)
    add_record = Button(screen_records_admin, text="Register new account", command = admin_add_account).pack()
    add_record.grid(row = user_id, column = 1)
    return_button = Button(screen_records_admin, text="Return", command = delete_admin_screen_records )
    return_button.grid(row = user_id,column = 6)
    conn.commit()
    conn.close()   

        
    




def admin_session():
    global screen_mainpage
    screen_mainpage = Toplevel(screen)
    screen_mainpage.title("dashboard")
    screen_mainpage.geometry("1000x750")
    Label(screen_mainpage, text = "").pack()
    Label(screen_mainpage, text = "Hello "+username1, font = ("Consolas", 20)).pack()
    Label(screen_mainpage, text = "Welcome to AI LAB ", font = ("Consolas", 20)).pack()
    Label(screen_mainpage, text = "").pack()
    Label(screen_mainpage, text = "").pack()
    Label(screen_mainpage, text = "").pack()
    Label(screen_mainpage, text = "").pack()
    Label(screen_mainpage, text = "").pack()
    Label(screen_mainpage, text = "").pack()
    Button(screen_mainpage, text = "Manage Accounts", command = manage_records).pack()
    Label(screen_mainpage, text = "").pack()
    Button(screen_mainpage, text = "View Notes", command = table_test).pack()
    Label(screen_mainpage, text = "").pack()
    Button(screen_mainpage, text = "Log out", command = log_out).pack()

def guest_session():
    global screen_mainpage
    screen_mainpage = Toplevel(screen)
    screen_mainpage.title("dashboard")
    screen_mainpage.geometry("1000x750")
    Label(screen_mainpage, text = "").pack()
    Label(screen_mainpage, text = "Welcome to AI LAB ", font = ("Consolas", 20)).pack()
    Label(screen_mainpage, text = "").pack()
    Label(screen_mainpage, text = "").pack()
    Label(screen_mainpage, text = "").pack()
    Label(screen_mainpage, text = "").pack()
    Label(screen_mainpage, text = "").pack()
    Label(screen_mainpage, text = "").pack()
    Button(screen_mainpage, text = "Create Notes").pack()
    Label(screen_mainpage, text = "").pack()
    Button(screen_mainpage, text = "View Notes").pack()
    Label(screen_mainpage, text = "").pack()
    Button(screen_mainpage, text = "Log out", command = log_out).pack()

    
def login_success():
    global screen3
    screen3 = Toplevel(screen)
    screen3.title("Success")
    screen3.geometry("150x100")
    Label(screen3, text = "Login Success").pack()
    Button(screen3, text = "OK", command = lambda:[session(), delete3(), delete2()]).pack()

def password_not_recognized():
    global screen4
    screen4 = Toplevel(screen)
    screen4.title("Password not recognised")
    screen4.geometry("150x100")
    Label(screen4, text = "Password not recognised").pack()
    Button(screen4, text = "OK", command = delete4).pack()

def user_not_found():
    global screen5
    screen5 = Toplevel(screen)
    screen5.title("User not found")
    screen5.geometry("300x200")
    Label(screen5, text = "User not found").pack()
    Button(screen5, text = "Retry", command = delete5).pack()    




    
def register_user():
    
    
    username_info = username.get()
    password_info = password.get()
    confirm_password_info = confirm_password.get()

    hide_mainscreen()
    if password_info == confirm_password_info:
        
        query_vals = (username_info,password_info)
        command_handler.execute("INSERT INTO users (username,password,privilege,status) VALUES (%s,%s,'guest','active')",query_vals)
        db.commit()

        username_entry.delete(0, END)
        password_entry.delete(0, END)
        confirm_password_entry.delete(0, END)

        Label(screen1, text = "Registration complete", fg = "green", font = ("consolas", 11)).pack()
    else:
        
        Label(screen1, text = "Confirm password does not match", fg = "red", font = ("consolas", 11)).pack()
        
        password_entry.delete(0, END)
        confirm_password_entry.delete(0, END)
        Button(screen1, text = "Retry", command =  register())
        
        


def login_verify():
    global username1
    username1 = username_verify.get()
    password1 = password_verify.get()
    username_entry1.delete(0, END)
    password_entry1.delete(0, END)
    hide_mainscreen()
    
    cursor = c.execute("SELECT * FROM user WHERE username = ? AND password = ?", (username1, password1))
    result = c.fetchone()
    if result is None:
        user_not_found()
        show_mainscreen()
    
    else:
        cursor = c.execute("SELECT * FROM user WHERE username = ? AND privilege = 'admin'", (username1,))
        if result is None:
            guest_session()
            
            
        else:
            admin_session()
        
    
def register():
    global screen1
    screen1 = Toplevel(screen)
    screen1.title("Register")
    screen1.geometry("600x500")
    
    global username
    global password
    global confirm_password
    global username_entry
    global password_entry
    global confirm_password_entry
    username = StringVar()
    password = StringVar()
    confirm_password = StringVar()
   

    Label(screen1, text = "Enter details below").pack()
    Label(screen1, text = "").pack()
    Label(screen1, text = "Username * ").pack()
    Label(screen1, text = "").pack()
    username_entry = Entry(screen1, textvariable = username)
    username_entry.pack()
    Label(screen1, text = "").pack()
    Label(screen1, text = "Password * ").pack()
    password_entry = Entry(screen1, textvariable = password)
    password_entry.pack()
    Label(screen1, text = "").pack()
    Label(screen1, text = "Confirm Password * ").pack()
    confirm_password_entry = Entry(screen1, textvariable = confirm_password)
    confirm_password_entry.pack()
    Label(screen1, text = "").pack()
    Button(screen1, text = "Register", width = 10, height = 1, command = register_user).pack()

def login():
    global screen2
    screen2 = Toplevel(screen)
    screen2.title("Login:")
    screen2.geometry("600x500")
    Label(screen2, text = "Enter details below").pack()
    Label(screen2, text = "").pack()

    global username_verify
    global password_verify
    username_verify = StringVar()
    password_verify = StringVar()

    global username_entry1
    global password_entry1
    Label(screen2, text = "Username * ").pack()
    username_entry1 = Entry(screen2, textvariable = username_verify)
    username_entry1.pack()
    Label(screen2, text = "").pack()
    Label(screen2, text = "Password * ").pack()
    password_entry1 = Entry(screen2, textvariable = password_verify)
    password_entry1.pack()
    password_entry1.config(show="*")
    Label(screen2, text = "").pack()
    Button(screen2, text = "Login", width = 10, height = 1, command = login_verify).pack()
    
    
    
def main_screen():
    global screen
    screen = Tk()
    screen.geometry("600x500")
    screen.title("AI LAB")
    global username_verify
    global password_verify
    global password_entry1
    global username_entry1
    username_verify = StringVar()
    password_verify = StringVar()
    Label(text = "AI LAB", bg = "blue",width = "300", height = "2", fg = "white", font = ("Consolas", 20)).pack()
    Label(text = "").pack()
    Label(text = "").pack()
    Label(text = "").pack()
    Label(text = "").pack()
    
    Label(text = "Username * ").pack()
    username_entry1 = Entry(textvariable = username_verify)
    username_entry1.pack()
    Label(text = "").pack()
    Label(text = "Password * ").pack()
    password_entry1 = Entry(textvariable = password_verify)
    password_entry1.pack()
    password_entry1.config(show="*")
    Label(text = "").pack()
    
    Button(text = "Login", width = "15", height = "2", bg = "#90EE90", command = login_verify).pack()
    Label(text = "").pack()
    Label(text = "").pack()
    Label(text = "").pack()
    Label(text = "").pack()
    Label(text = "New to here? Register").pack()
    Button(text = "Register", width = "10", height = "1", command = register).pack()
    Label(text = "").pack()
    
    
    screen.mainloop()
    
main_screen()
