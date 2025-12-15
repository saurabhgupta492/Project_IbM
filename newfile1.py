from tkinter import *
from tkinter import messagebox
import sqlite3
import pyttsx3

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# ---------------- DATABASE -----------------
conn = sqlite3.connect("users.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT
)
""")
conn.commit()

# ------------- SIGN IN WINDOW FUNCTION --------------
def open_signin_window():
    signin_win = Toplevel()
    signin_win.title("Signin")
    icon = PhotoImage(file="icon.png")
    signin_win.iconphoto(True, icon)
    signin_win.icon = icon
    signin_win.geometry('925x500+300+200')
    signin_win.configure(bg='white')
    signin_win.resizable(False, False)

    # LOGIN FUNCTION
    def signin():
        username = user.get()
        password = code.get()
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", 
                       (username, password))
        result = cursor.fetchone()
        if result:
            screen = Toplevel(signin_win)
            screen.title("App")
            icon = PhotoImage(file="icon.png")
            screen.iconphoto(True, icon)
            screen.icon = icon
            screen.geometry('925x500+300+200')
            screen.config(bg="white")
            Label(screen, text=f'Welcome {username} !', bg='#fff', 
                  font=('Calibri(Body)', 40, 'bold')).pack(expand=True)
            screen.after(100, lambda: speak(f"Welcome {username}"))
            signin_win.withdraw()
        else:
            messagebox.showerror("Invalid", "Incorrect Username or Password")

    # ------------------ IMAGE -------------------
    img = PhotoImage(file='login.png')
    Label(signin_win, image=img, bg='white').place(x=50, y=50)
    signin_win.img = img

    frame = Frame(signin_win, width=350, height=390, bg='#fff')
    frame.place(x=480, y=50)

    heading = Label(frame, text='Sign in', fg="#57a1f8", bg='white', 
                    font=('Microsoft Yahei UI Light', 23, 'bold'))
    heading.place(x=100, y=5)

    # Username
    def user_enter(e):
        if user.get() == 'Username':
            user.delete(0, 'end')

    def user_leave(e):
        if user.get() == "":
            user.insert(0, 'Username')

    user = Entry(frame, width=25, fg='black', border=0, bg='white', 
                 font=('Microsoft Yahei UI Light', 11))
    user.place(x=30, y=80)
    user.insert(0, 'Username')
    user.bind("<FocusIn>", user_enter)
    user.bind("<FocusOut>", user_leave)
    Frame(frame, width=295, height=2, bg='black').place(x=25, y=107)

    # Password
    def pass_enter(e):
        if code.get() == 'Password':
            code.delete(0, 'end')
            code.config(show="*")

    def pass_leave(e):
        if code.get() == "":
            code.insert(0, 'Password')
            code.config(show="")

    code = Entry(frame, width=25, fg='black', border=0, bg='white', 
                 font=('Microsoft Yahei UI Light', 11))
    code.place(x=30, y=150)
    code.insert(0, 'Password')
    code.bind("<FocusIn>", pass_enter)
    code.bind("<FocusOut>", pass_leave)
    Frame(frame, width=295, height=2, bg='black').place(x=25, y=177)

    Button(frame, width=39, pady=7, text='Sign in', bg='#57a1f8', 
           fg='white', border=0, command=signin).place(x=35, y=280)

    signin_win.mainloop()


# ---------------- MAIN SIGNUP WINDOW -----------------
root = Tk()
root.title("SignUp")
icon = PhotoImage(file="icon.png")
root.iconphoto(True, icon)
root.icon = icon
root.geometry('925x500+300+200')
root.configure(bg='white')
root.resizable(True, True)

# ------------------ IMAGE ------------------
try:
    img = PhotoImage(file='login.png')
    Label(root, image=img, bg='white').place(x=50, y=50)
    root.img = img  # keep reference
except Exception as e:
    print("Image not found:", e)

frame = Frame(root, width=350, height=390, bg='#fff')
frame.place(x=480, y=50)

heading = Label(frame, text='Sign up', fg="#57a1f8", bg='white', 
                font=('Microsoft Yahei UI Light', 23, 'bold'))
heading.place(x=100, y=5)

# USERNAME
def user_enter(e):
    if user.get() == 'Username':
        user.delete(0, 'end')

def user_leave(e):
    if user.get() == "":
        user.insert(0, 'Username')

user = Entry(frame, width=25, fg='black', border=0, bg='white', 
             font=('Microsoft Yahei UI Light', 11))
user.place(x=30, y=80)
user.insert(0, 'Username')
user.bind("<FocusIn>", user_enter)
user.bind("<FocusOut>", user_leave)
Frame(frame, width=295, height=2, bg='black').place(x=25, y=107)

# PASSWORD
def pass_enter(e):
    if code.get() == 'Password':
        code.delete(0, 'end')
        code.config(show="*")

def pass_leave(e):
    if code.get() == "":
        code.insert(0, 'Password')
        code.config(show="")

code = Entry(frame, width=25, fg='black', border=0, bg='white', 
             font=('Microsoft Yahei UI Light', 11))
code.place(x=30, y=150)
code.insert(0, 'Password')
code.bind("<FocusIn>", pass_enter)
code.bind("<FocusOut>", pass_leave)
Frame(frame, width=295, height=2, bg='black').place(x=25, y=177)

# CONFIRM PASSWORD
def confirm_enter(e):
    if confirm.get() == 'Confirm Password':
        confirm.delete(0, 'end')
        confirm.config(show="*")

def confirm_leave(e):
    if confirm.get() == "":
        confirm.insert(0, 'Confirm Password')
        confirm.config(show="")

confirm = Entry(frame, width=25, fg='black', border=0, bg='white', 
                font=('Microsoft Yahei UI Light', 11))
confirm.place(x=30, y=220)
confirm.insert(0, 'Confirm Password')
confirm.bind("<FocusIn>", confirm_enter)
confirm.bind("<FocusOut>", confirm_leave)
Frame(frame, width=295, height=2, bg='black').place(x=25, y=247)

# SIGNUP FUNCTION
def signup_user():
    username = user.get()
    password = code.get()
    confirm_password = confirm.get()

    if username == "" or username == "Username" or \
       password == "" or password == "Password" or \
       confirm_password == "" or confirm_password == "Confirm Password":
        messagebox.showerror("Error", "All fields are required!")
        return

    if password != confirm_password:
        messagebox.showerror("Error", "Passwords do not match!")
        return

    try:
        cursor.execute("INSERT INTO users(username, password) VALUES(?,?)", 
                       (username, password))
        conn.commit()
        messagebox.showinfo("Success", "Account created successfully!")
    except:
        messagebox.showerror("Error", "Username already exists!")

Button(frame, width=39, pady=7, text='Sign up', bg='#57a1f8', 
       fg='white', border=0, command=signup_user).place(x=35, y=280)

label = Label(frame, text='I have an account', fg='black', bg='white', 
              font=('Microsoft YaHei UI Light', 9))
label.place(x=90, y=340)

Button(frame, width=6, text='Sign in', border=0, bg='white', cursor='hand2', 
       fg='#57a1f8', command=open_signin_window).place(x=200, y=340)

root.mainloop()
