from Tkinter import *
import re
from PIL import ImageTk
from signup import Signup
from client import check_database


class Login:
    def __init__(self, root):
        self.loggedin = ""
        self.score = 0
        self.root = root
        self.root.title("Login System")
        self.root.geometry("640x524-600+250") #new window size
        self.root.resizable(False, False) #stop the maximise of the window

        #Background Image
        self.bg =ImageTk.PhotoImage(file = "login.jpg")
        self.bg_image = Label(self.root, image=self.bg)
        self.bg_image.place(x=0, y=0, relwidth=1, relheight=1)

        #Login frame
        Frame_login = Frame(self.root, bg = "white")
        Frame_login.place(x=120, y=150, width="400", height = "300")

        #Title and subtitle
        title = Label(Frame_login, text="Login{Here", font=("redwater banker PERSONAL USE", 24), fg="#805A40", bg="white")
        title.place(x=90, y=30)

        subtitle = Label(Frame_login, text="Members]Login", font=("redwater banker PERSONAL USE", 12), fg="#804046", bg="white")
        subtitle.place(x=120, y=80)

        # Username
        lbl_user = Label(Frame_login, text="Username", font=("calibri", 12), fg="#406680", bg="white")
        lbl_user.place(x=160, y=110)
        #create the entry for the username
        self.username = Entry(Frame_login, font=("calibri", 12), bg="#807A40")
        self.username.place(x=90, y=130, width=236, height=35)

        # Password
        lbl_pass = Label(Frame_login, text="Password", font=("calibri", 12), fg="#406680", bg="white")
        lbl_pass.place(x=160, y=170)
        #create the entry for the password
        self.password = Entry(Frame_login, font=("calibri", 12), bg="#807A40")
        self.password.place(x=90, y=190, width=236, height=35)

        #forget
        forget = Button(Frame_login, text="forgot password?",bd=0, font=("calibri", 12), fg="#404680", bg="white")
        forget.place(x=132, y=250)

        #Login
        login = Button(Frame_login,command = self.check_function, text="Login",bd=0, font=("redwater banker PERSONAL USE", 12), fg="#C0ADA0", bg="#261B13")
        login.place(x=290, y=245)

        #Signup
        signup = Button(Frame_login, command = self.signup_function, text="Signup",bd=0, font=("redwater banker PERSONAL USE", 12), fg="#C0ADA0", bg="#261B13") #calls sing up function
        signup.place(x=40, y=245)


    def check_function(self): #validates the username with password
        if self.username.get() == "" or self.password.get() == "": #checks if fields are empty
            error_box = Toplevel(self.root)
            error_box.title("Error")
            error_message = "All fields are required"
            error_label = Label(error_box, text=error_message, font=("calibri", 12), fg="#406680")
            error_label.pack(padx=20, pady=10)

            # Center the error message
            error_box.update_idletasks() # Updates the dimensions of the Toplevel widget
            w = error_box.winfo_width() # Gets the width of the Toplevel widget
            h = error_box.winfo_height() # Gets the height of the Toplevel widget
            x = (error_box.winfo_screenwidth() // 2) - (w // 2) # Calculates the x-coordinate for centering the Toplevel widget
            y = (error_box.winfo_screenheight() // 2) - (h // 2) # Calculates the y-coordinate for centering the Toplevel widget
            error_box.geometry('{}x{}+{}+{}'.format(w, h, x, y)) # Sets the geometry of the Toplevel widget to center it on the screen

            error_box.grab_set() #can only interact witht he error box

            error_box.mainloop()

        else:
            print self.password.get()
            success =  check_database(self.username.get(), self.password.get())  #if passed thsoe two then the user is welcomed
            if success:
                welcome_box = Toplevel(self.root) 
                welcome_box.title("Welcome")
                welcome_message= ("Welcome", self.username.get())
                self.loggedin = self.username.get()
                #self.score = score
                welcome_label = Label(welcome_box, text=welcome_message, font=("calibri", 12), fg="#406680") #changed text = error_message to text = welcome_message
                welcome_label.pack(padx=20, pady=10)

                                # Center the error message
                welcome_box.update_idletasks() # Updates the dimensions of the Toplevel widget
                w = welcome_box.winfo_width() # Gets the width of the Toplevel widget
                h = welcome_box.winfo_height() # Gets the height of the Toplevel widget
                x = (welcome_box.winfo_screenwidth() // 2) - (w // 2) # Calculates the x-coordinate for centering the Toplevel widget
                y = (welcome_box.winfo_screenheight() // 2) - (h // 2) # Calculates the y-coordinate for centering the Toplevel widget
                welcome_box.geometry('{}x{}+{}+{}'.format(w, h, x, y)) # Sets the geometry of the Toplevel widget to center it on the screen

                welcome_box.grab_set() #can only interact witht he error box


                welcome_box.mainloop()

            else:
                error_box = Toplevel(self.root)
                error_box.title("Error")
                error_message = "Incorrect username or password"
                error_label = Label(error_box, text=error_message, font=("calibri", 12), fg="#406680")
                error_label.pack(padx=20, pady=10)

                # Center the error message
                error_box.update_idletasks() # Updates the dimensions of the Toplevel widget
                w = error_box.winfo_width() # Gets the width of the Toplevel widget
                h = error_box.winfo_height() # Gets the height of the Toplevel widget
                x = (error_box.winfo_screenwidth() // 2) - (w // 2) # Calculates the x-coordinate for centering the Toplevel widget
                y = (error_box.winfo_screenheight() // 2) - (h // 2) # Calculates the y-coordinate for centering the Toplevel widget
                error_box.geometry('{}x{}+{}+{}'.format(w, h, x, y)) # Sets the geometry of the Toplevel widget to center it on the screen
                
                error_box.grab_set() #can only interact witht he error box


                error_box.mainloop()

    def signup_function(self):
        signup_box = Toplevel(self.root) #creates new tkinter box
        signup_obj = Signup(signup_box)
        signup_box.mainloop()

#root = Tk()
#obj = Login(root)
#root.mainloop()

#root.mainloop()
####### feedback improvvemnets centre the errors and welcomes
####### stop access from the main window after top level is clicked
####### make sure no repeated usernames