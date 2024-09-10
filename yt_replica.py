import ttkbootstrap as tk1
from tkinter import messagebox, Toplevel, IntVar, END
import mysql.connector
from tkinter import *

root = tk1.Window(themename="cyborg")
root.geometry("880x500")
usrnm = "Manan123"
passwr = "1908"

# Database connection
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="password"
)
my_cursor = connection.cursor()

a = IntVar(value=0)


def click_bind(e):
    email = cb.get()
    query = "SELECT `pass` FROM `pass` WHERE `email` = %s"
    my_cursor.execute(query, (email,))
    pas = my_cursor.fetchone()
    e_pass.delete(0, END)
    if pas:
        e_pass.insert(0, pas[0])


def show_password():
    e_pass.config(show='' if show_var.get() else '*')


def take():
    def login():
        usr, passw = e_pass_usr.get(), e_pass_pass.get()
        print(f"Popup Username entered: {usr}")
        print(f"Popup Password entered: {passw}")

        if not usr or not passw:
            messagebox.showerror("Password Manager - Login Page", "Don't leave the entries blank")
        elif usr == usrnm and passw == passwr:
            top.withdraw()
            messagebox.showinfo("Password Manager - Login Page", "Login successful :)")
            a.set(1)  # Update the variable to show the dropdown
            update()
        else:
            messagebox.showerror("Password Manager - Login Page", "Invalid username or password, please recheck")

    top = Toplevel()
    top.geometry("880x350")
    tk1.Label(top, text="PASSWORD MANAGER", font=("Georgia", 18)).grid(row=1, column=2, padx=50)
    tk1.Label(top, text="LOGIN PAGE", font=("Georgia", 15)).grid(row=3, column=2, pady=10)

    tk1.Label(top, text="Username: ", font=("Georgia", 13)).grid(row=5, column=1, pady=30, padx=10)
    tk1.Label(top, text="Password: ", font=("Georgia", 13)).grid(row=6, column=1, pady=10, padx=10)

    e_pass_usr = tk1.Entry(top, width=50)
    e_pass_usr.grid(row=5, column=2, padx=20)

    e_pass_pass = tk1.Entry(top, width=50, show="*")
    e_pass_pass.grid(row=6, column=2)

    btn = tk1.Button(top, text="Login", style="primary.TButton", width=40, command=login)
    btn.grid(row=7, column=2, pady=30)


def login():

    usr = e_usr.get()
    passw = e_pass.get()
    usr_cb = cb.get()

    print(f"Main Username entered: {usr}")
    print(f"Main Password entered: {passw}")
    print(f"Main ComboBox value: {usr_cb}")

    if a.get() == 0:

        my_cursor.execute("SELECT `pass` FROM `yt` WHERE `usrnm` = %s", (usr,))
        pass_db = my_cursor.fetchone()

        my_cursor.execute("SELECT `pass` FROM `pass` WHERE `email`=%s", (usr,))
        pass_pass = my_cursor.fetchone()

        if pass_db and passw == pass_db[0]:
            root.destroy()
            messagebox.showinfo("Youtube", "Login successful :)")
        elif pass_pass is None:
            value = messagebox.askquestion("Password Manager","This password is not saved in the Password Manager. Do you want to save the password in the Password Manager?")
            if value == "yes":
                my_cursor.execute("INSERT INTO `pass`(`Web`, `email`, `pass`) VALUES (%s, %s, %s)",("Youtube", usr, passw))

        elif not usr or not passw:
            messagebox.showerror("Youtube","Don't leave the entries blank")
        else:
            messagebox.showerror("Youtube", "Invalid username or password, please recheck")

    elif a.get() == 1:

        my_cursor.execute("SELECT `pass` FROM `yt` WHERE `usrnm` = %s", (usr_cb,))
        pass_cdb = my_cursor.fetchone()


        if pass_cdb and passw == pass_cdb[0]:
            root.destroy()
            messagebox.showinfo("Password Manager - Login Page", "Login successful :)")
        else:
            messagebox.showerror("Password Manager - Login Page", "Invalid username or password, please recheck")
    else:
        messagebox.showerror("Password Manager - Login Page", "Don't leave the entries blank")

    print(a.get())


def update():
    if a.get() == 0:
        e_usr.grid(row=5, column=2, padx=20)
        cb.grid_forget()
    else:
        e_usr.grid_forget()
        cb.grid(row=5, column=2, padx=20)


# Main window UI
tk1.Label(root, text="YOUTUBE", font=("Georgia", 18)).grid(row=1, column=2, padx=50)
tk1.Label(root, text="LOGIN PAGE", font=("Georgia", 15)).grid(row=3, column=2, pady=10)

tk1.Label(root, text="Username: ", font=("Georgia", 13)).grid(row=5, column=1, pady=30, padx=10)
tk1.Label(root, text="Password: ", font=("Georgia", 13)).grid(row=6, column=1, pady=10, padx=10)

e_usr = tk1.Entry(root, width=50)
e_pass = tk1.Entry(root, width=50, show="*")

e_usr.grid(row=5, column=2, padx=20)
e_pass.grid(row=6, column=2)

try:
    my_cursor.execute("SELECT * FROM `pass` WHERE `Web` = 'Youtube';")
    datas = my_cursor.fetchall()
    val = [data[1] for data in datas]
    cb = tk1.Combobox(root, values=val, width=48)
    cb.bind("<<ComboboxSelected>>", click_bind)
except mysql.connector.Error as err:
    messagebox.showerror("Database Error", f"Error fetching data from the database: {err}")

btn = tk1.Button(root, text="Login", style="primary.TButton", width=40, command=login)
btn.grid(row=7, column=2, pady=30)

menubar = tk1.Menu(root)
dropDown = tk1.Menu(menubar, tearoff=0)
dropDown.add_command(label="Login", command=take)
show_var = IntVar()
show_password_check = tk1.Checkbutton(root, text="Show Password", variable=show_var, command=show_password)
show_password_check.grid(row=6, column=3, padx=10)
menubar.add_cascade(label="Password Manager", menu=dropDown)
root.config(menu=menubar)

update()

root.mainloop()
