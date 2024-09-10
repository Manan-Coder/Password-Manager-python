from tkinter import *
import ttkbootstrap as tk
import mysql.connector
from tkinter import messagebox

connection = mysql.connector.connect(host="localhost", user="root", password="", database="password")
my_cursor = connection.cursor()

root = tk.Window(themename='cyborg')
root.title("Password Manager")
root.geometry("880x500")

def next():
    import ttkbootstrap as tk1
    def add():
        def insrt():
            web, mail, passw = e_web.get(), e_mail.get(), e_pass.get()
            if web and mail and passw:
                insert_query = "INSERT INTO `pass`(`Web`, `email`, `pass`) VALUES (%s, %s, %s)"
                vals = (web, mail, passw)
                my_cursor.execute(insert_query, vals)
                connection.commit()
                messagebox.showinfo("Password added", "Your password has been saved to database")
                top.destroy()
            else:
                messagebox.showerror("Input Error", "Don't leave the entries blank")

        top = Toplevel()
        e_web = tk1.Entry(top, width=25)
        e_web.insert(0, "Enter website's name")
        e_web.grid(row=2, column=1, padx=25)
        e_web.bind("<FocusIn>", lambda e: e_web.delete(0, END))

        e_mail = tk1.Entry(top, width=25)
        e_mail.insert(0, "Enter e-mail")
        e_mail.grid(row=3, column=1, padx=20)
        e_mail.bind("<FocusIn>", lambda e: e_mail.delete(0, END))

        e_pass = tk1.Entry(top, width=25)
        e_pass.insert(0, "Enter password")
        e_pass.grid(row=4, column=1, padx=20)
        e_pass.bind("<FocusIn>", lambda e: e_pass.delete(0, END))

        btn_smbt = tk1.Button(top, text="Insert the record", style='primary.Tbutton', command=insrt)
        btn_smbt.grid(row=6, column=1, pady=30)

    def show():
        top = Toplevel()
        top.title("View data")
        trv = tk1.Treeview(top, columns=(1, 2, 3), height=15, show="headings")
        trv.column(1, anchor=CENTER, stretch=NO, width=150)
        trv.column(2, anchor=CENTER, stretch=NO, width=350)
        trv.column(3, anchor=CENTER, stretch=NO, width=150)
        trv.heading(1, text="Website name")
        trv.heading(2, text="Email")
        trv.heading(3, text="Password")
        trv.grid(row=0, column=0)
        my_cursor.execute("SELECT * FROM `pass`")
        datas = my_cursor.fetchall()
        for data in datas:
            trv.insert('', 'end', value=(data[0], data[1], data[2]))

    def srch():
        def find():
            website = e_srch.get()
            if website:
                my_cursor.execute("SELECT * FROM `pass` WHERE Web=%s", (website,))
                datas = my_cursor.fetchall()
                f = Toplevel()
                f.title("View data")
                trv = tk1.Treeview(f, columns=(1, 2, 3), height=15, show="headings")
                trv.column(1, anchor=CENTER, stretch=NO, width=150)
                trv.column(2, anchor=CENTER, stretch=NO, width=250)
                trv.column(3, anchor=CENTER, stretch=NO, width=150)
                trv.heading(1, text="Website name")
                trv.heading(2, text="Email")
                trv.heading(3, text="Password")
                trv.grid(row=0, column=0)
                for data in datas:
                    trv.insert('', 'end', value=(data[0], data[1], data[2]))
                top.destroy()
            else:
                messagebox.showerror("Input Error", "Please enter a website name")

        top = Toplevel()
        e_srch = tk1.Entry(top, width=25)
        e_srch.insert(0, "Enter website's name")
        e_srch.grid(row=2, column=1, padx=25)
        e_srch.bind("<FocusIn>", lambda e: e_srch.delete(0, END))

        btn_srch = tk1.Button(top, text="Search the record", style='primary.Tbutton', command=find)
        btn_srch.grid(row=3, column=1, pady=30)

    nw = Toplevel()
    tk1.Label(nw, text="PASSWORD MANAGER", font=("Georgia, Italic", 18)).grid(row=0, column=2, padx=100)

    btn_add = tk1.Button(nw, text="Save a password", style='primary.Tbutton', width=30, command=add)
    btn_add.grid(row=4, column=2, pady=32, columnspan=2)

    btn_shw = tk1.Button(nw, text="Show passwords", style='primary.Tbutton', width=30, command=show)
    btn_shw.grid(row=6, column=2, columnspan=2)

    btn_srch = tk1.Button(nw, text="Search for a password", style='primary.Tbutton', width=30, command=srch)
    btn_srch.grid(row=8, column=2, columnspan=2, pady=30)


def show_password():
    e_pass.config(show='' if show_var.get() else '*')


def login():
    usr, passw = e_usr.get(), e_pass.get()
    try:
        insert_query = "SELECT `pass` FROM `user_base` WHERE `email` = %s"
        vals = (usr,)
        my_cursor.execute(insert_query,vals)
        passwrd = my_cursor.fetchone()
        print(passwrd[0])
        if passwrd[0] is None:
            messagebox.showerror("Password Manager", "Account doesn't exists,Sign-up first")
        elif not usr or not passw:
            messagebox.showerror("Password Manager - Login Page", "Don't leave the entries blank")
        elif passw == passwrd[0]:
            root.withdraw()
            messagebox.showinfo("Password Manager - Login Page", "Login successful :)")
            next()
        else:
            messagebox.showerror("Password Manager - Login Page", "Incorrect password, please recheck or forget password incase")

    except:
        messagebox.showerror("Password Manager","Could not find Account,recheck email aur Sign-up")

tk.Label(root, text="PASSWORD MANAGER", font=("Georgia, Italic", 18)).grid(row=1, column=2, padx=50)
tk.Label(root, text="LOGIN PAGE", font=("Georgia, Italic", 15)).grid(row=3, column=2, pady=10)

tk.Label(root, text="Username:", font=("Georgia, Italic", 13)).grid(row=5, column=1, pady=30, padx=10)
tk.Label(root, text="Password:", font=("Georgia, Italic", 13)).grid(row=6, column=1, pady=10, padx=10)

e_usr = tk.Entry(root, width=50)
e_usr.grid(row=5, column=2, padx=20)

e_pass = tk.Entry(root, width=50, show='*')
e_pass.grid(row=6, column=2)

show_var = IntVar()
show_password_check = tk.Checkbutton(root, text="Show Password", variable=show_var, command=show_password)
show_password_check.grid(row=6, column=3, padx=10)

btn = tk.Button(root, text="Login", style="primary.Tbutton", width=40, command=login)
btn.grid(row=7, column=2, pady=30)

def signup():
    def otp():
        email_e = email.get()
        insert_query = "SELECT `pass` FROM `user_base` WHERE `email` = %s"
        vals = (email_e,)
        my_cursor.execute(insert_query,vals)
        pass_g = my_cursor.fetchone()
        if not pass_g:
            import random
            OTP = random.randint(1000, 9999)
            import smtplib
            from email.mime.text import MIMEText

            # Email configuration
            smtp_server = 'smtp.gmail.com'
            smtp_port = 587
            email_address = 'sharmamanan1908@gmail.com'
            email_password = 'tdey zlfa gxge gvzx'
            email_to = email.get()

            # Create the email content
            msg = MIMEText(f'{OTP} is OTP for Password Manager,Enjoy:)')
            msg['Subject'] = f'<No-Reply>{OTP} is OTP for Password Manager'
            msg['From'] = email_address
            msg['To'] = email_to

            # Send the email
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(email_address, email_password)
                server.sendmail(email_address, [email_to], msg.as_string())
                print("Email sent")
            pass_o=pass_sdb.get()
            def check():
                if int(otp_ent.get()) == OTP:
                    f.destroy()
                    t.destroy()
                    messagebox.showinfo("Password Manager","Sign-up successful")
                    insert_query = "INSERT INTO `user_base` (`email`, `pass`) VALUES (%s,%s)"
                    vals = (email_to,pass_o)
                    my_cursor.execute(insert_query,vals)
                    connection.commit()
                else:
                    messagebox.showerror("Password Manager","Incorrect OTP")
            t = Toplevel()
            Label(t,text = "We have sent an OTP on the email address you entered",font =("Georgia, Underline", 10) ).pack()
            Label(t, text=" ", font=("Georgia, Underline", 4)).pack()
            otp_ent = tk.Entry(t,width = 30)
            otp_ent.pack()
            Label(t, text=" ", font=("Georgia, Underline", 10)).pack()
            Button(t,text = "Enter",width=15,command=check).pack()
        else:
            f.destroy()
            messagebox.showerror("Password Manager","An account is already registered with this email,login or forget password incase")


    f=Toplevel()
    f.geometry("600x500")
    Label(f,text = "SIGN-UP",font=("Georgia, Underline", 18)).grid(row = 1,column=1,columnspan=4,padx = 20)
    Label(f,text = "Enter your email:",font=("Georgia, Underline", 12)).grid(row = 3,column=1,pady=50)
    Label(f,text = "Enter your password:",font=("Georgia, Underline", 12)).grid(row = 4,column=1)
    email = tk.Entry(f,width=30)
    email.grid(row=3,column=3,padx=10,columnspan=2)
    pass_sdb = tk.Entry(f,width=30)
    pass_sdb.grid(row=4,column=3,padx=10,columnspan=2)
    Button(f,text="Sign-up",width=30,command=otp).grid(row=7,column=1,pady=30,columnspan=5,padx=10)

def frget():
    def forget():
        email_e = email.get()
        insert_query = "SELECT `pass` FROM `user_base` WHERE `email` = %s"
        vals = (email_e,)
        my_cursor.execute(insert_query,vals)
        pass_g = my_cursor.fetchone()
        if pass_g:
            import random
            OTP = random.randint(1000, 9999)
            import smtplib
            from email.mime.text import MIMEText

            # Email configuration
            smtp_server = 'smtp.gmail.com'
            smtp_port = 587
            email_address = yout_email
            email_password = your app specific password
            email_to = email.get()

            # Create the email content
            msg = MIMEText(f'{OTP} is OTP for Password Manager Password Reset,Enjoy:)')
            msg['Subject'] = f'<No-Reply>{OTP} is OTP for Password Reset'
            msg['From'] = email_address
            msg['To'] = email_to

            # Send the email
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(email_address, email_password)
                server.sendmail(email_address, [email_to], msg.as_string())
                print("Email sent")
            def check():
                if int(otp_ent.get()) == OTP:
                    f.destroy()
                    t.destroy()
                    def update():
                        update_query = "UPDATE `user_base` SET `pass` = %s WHERE `email` = %s"
                        vals = (pass_n.get(), email_to)
                        my_cursor.execute(update_query, vals)
                        connection.commit()
                        messagebox.showinfo("Password Manager","Password updated successfully")
                        m.destroy()
                    m=Toplevel()
                    m.geometry("600x250")
                    Label(m, text="FORGET PASSWORD", font=("Georgia, Underline", 18)).grid(row=1, column=1,                                                                   columnspan=4, padx=20)
                    Label(m, text="Enter the new password", font=("Georgia, Underline", 12)).grid(row=3, column=1, pady=50)
                    pass_n = tk.Entry(m, width=30)
                    pass_n.grid(row=3, column=3, padx=10, columnspan=2)
                    Button(m, text="Update", width=30,command = update).grid(row=5, column=1, pady=10, columnspan=5, padx=10)

                else:
                    messagebox.showerror("Password Manager","Incorrect OTP")
            t = Toplevel()
            Label(t,text = "We have sent an OTP on the email address you entered",font =("Georgia, Underline", 10) ).pack()
            Label(t, text=" ", font=("Georgia, Underline", 4)).pack()
            otp_ent = tk.Entry(t,width = 30)
            otp_ent.pack()
            Label(t, text=" ", font=("Georgia, Underline", 10)).pack()
            Button(t,text = "Enter",width=15,command=check).pack()
        else:
            f.destroy()
            messagebox.showerror("Password Manager","Any account is not registered with this email,Signup first")


    f = Toplevel()
    f.geometry("600x250")
    Label(f, text="FORGET PASSWORD", font=("Georgia, Underline", 18)).grid(row=1, column=1, columnspan=4, padx=20)
    Label(f, text="Enter your email:", font=("Georgia, Underline", 12)).grid(row=3, column=1, pady=50)
    email = tk.Entry(f, width=30)
    email.grid(row=3, column=3, padx=10, columnspan=2)
    Button(f, text="Forget", width=30,command= forget).grid(row=5, column=1, pady=10, columnspan=5, padx=10)


signp = tk.Label(root,text = "Sign-up",font=("Georgia, Underline", 8),bootstyle = "primary ")
signp.grid(row=8,column=2)
signp.bind("<Button-1>",lambda e:signup())


fget = tk.Label(root,text = "Forget Password?",font=("Georgia, Underline", 8),bootstyle = "primary ")
fget.grid(row=9,column=2,pady=2)
fget.bind("<Button-1>",lambda e:frget())
root.mainloop()
