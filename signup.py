from Tkinter import *
import re
from PIL import ImageTk
from database import update_database #used in sign up function

class Signup:
    def __init__(self, signup_box):
            self.signup_box = signup_box
            self.signup_box.title("Sign up") #creates title of the box
            self.signup_box.geometry("320x480-762+250") #creates size and location when spawned
            self.signup_box.resizable(False, False) #makes it not resizable
            self.bg = ImageTk.PhotoImage(file = "signup.jpg") #takes image
            self.bg_image = Label(self.signup_box, image=self.bg) #implements image using label
            self.bg_image.place(x=0, y=0, relwidth=1, relheight=1) #places it on the window

            # Username
            lbl_user = Label(self.signup_box, text="Username", font=("calibri", 12), fg="#F2EFEC", bg="#261B13")
            lbl_user.place(x=120, y=110)
            #create the entry for the username
            self.username = Entry(self.signup_box, font=("calibri", 12), bg="#C0ADA0")
            self.username.place(x=80, y=130, width=150, height=35)

            # Password
            lbl_pass = Label(self.signup_box, text="Password", font=("calibri", 12), fg="#F2EFEC", bg="#261B13")
            lbl_pass.place(x=120, y=170)
            #create the entry for the password
            self.password = Entry(self.signup_box, font=("calibri", 12), bg="#C0ADA0")
            self.password.place(x=80, y=190, width=150, height=35)

            # confirm Password
            lbl_pass = Label(self.signup_box, text="Confirm Password", font=("calibri", 12), fg="#F2EFEC", bg="#261B13")
            lbl_pass.place(x=95, y=230)
            #create the entry for the password
            self.confirm_password = Entry(self.signup_box, font=("calibri", 12), bg="#C0ADA0")
            self.confirm_password.place(x=80, y=250, width=150, height=35)

            #Signup
            signup = Button(self.signup_box, command = self.check_signup, text="Signup",bd=0, font=("redwater banker PERSONAL USE", 12), fg="#C0ADA0", bg="#261B13") #calls sing up function
            signup.place(x=110, y=350)

    def check_signup(self): #validates the username with password

        def isAllPresent(password):
            flag = 0
            while True:
                if (len(password)<6):
                    flag = -1
                    break
                elif not re.search("[a-z]", password):
                    flag = -1
                    break
                elif not re.search("[A-Z]", password):
                    flag = -1
                    break
                elif not re.search("[0-9]", password):
                    flag = -1
                    break
                elif not re.search("(?=.*[-+_!@#$%^&*., ?]).+$" , password):
                    flag = -1
                    break
                elif re.search("\s" , password):
                    flag = -1
                    break
                else:
                    flag = 0
                    return True
                    break
            
            if flag == -1:
                return False
        
        if self.username.get() == "" or self.password.get() == "" or self.confirm_password.get() == "": #checks if fields are empty
            error_box = Toplevel(self.signup_box)
            error_box.title("Error")
            error_message = ("All fields are required")
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

        elif isAllPresent(self.password.get()) == False:  #if passed thsoe two then the user is welcomed
            error_box = Toplevel(self.signup_box)
            error_box.title("Error")
            error_message = ("Passwords must have at least one uppercase, one lowercase, have at least one number, one special character and be atleast 6 characters long")
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

        elif self.password.get() != self.confirm_password.get(): 
            error_box = Toplevel(self.signup_box)
            error_box.title("Error")
            error_message = ("Passwords must be equal")
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

        else:  #if passed thsoe two then the user is welcomed
            welcome_box = Toplevel(self.signup_box) 
            welcome_box.title("Welcome")
            welcome_message= ("Welcome", self.username.get())
            update_database(self.username.get(), self.password.get()) #adds username and password to the database
            welcome_label = Label(welcome_box, text=welcome_message, font=("calibri", 12), fg="#406680") #changed text = error_message to text = welcome_message
            welcome_label.pack(padx=20, pady=10)
            
                            # Center the error message
            welcome_box.update_idletasks() # Updates the dimensions of the Toplevel widget
            w = welcome_box.winfo_width() # Gets the width of the Toplevel widget
            h = welcome_box.winfo_height() # Gets the height of the Toplevel widget
            x = (welcome_box.winfo_screenwidth() // 2) - (w // 2) # Calculates the x-coordinate for centering the Toplevel widget
            y = (welcome_box.winfo_screenheight() // 2) - (h // 2) # Calculates the y-coordinate for centering the Toplevel widget
            welcome_box.geometry('{}x{}+{}+{}'.format(w, h, x, y)) # Sets the geometry of the Toplevel widget to center it on the screen

            #welcome_box.grab_set() #can only interact witht he welcome box


            welcome_box.mainloop()



