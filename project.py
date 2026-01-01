#the libraries I need
import requests #use this to scrape news https://pypi.org/project/requests/
import customtkinter # for the gui; normal tkinter isn't clean and i want to make my gui look clean 
from dotenv import load_dotenv, set_key #use this for saving the passwords in .env
import schedule # use this to auto run and send email everyday-morning
import os # to check if its the users first time on the software with .env checking
def main():
    if os.path.isfile(".env"):
        gui()
    else:
        gui("setup")


def gui(s):
    #making the gui 
    app = customtkinter.CTk()
    app.title("Daily Digest News Email Sender")
    app.geometry("600x600")
    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("dark-blue")
    if s == "setup": #if this is there first time ask for email + pass
        label=customtkinter.CTkLabel(app,text="Enter your Gmail credentials")
        label.pack(pady=20)#this like gives it breathing room
        email=customtkinter.CTkEntry(app, placeholder_text="Email")
        email.pack(pady=20)

        password=customtkinter.CTkEntry(app, placeholder_text="Password")
        password.pack(pady=20)

        choice_box = customtkinter.CTkOptionMenu(app, values=["Hacker News", "Google News", "Yahoo News"])

        choice_box.pack(pady=20)

        def save_creds():
            user_email=email.get()
            user_password=password.get()
            news_choice = choice_box.get()
            print("Saving")
            app.destroy()
            
        button = customtkinter.CTkButton(app,text='Save Credentials',command=save_creds)
        button.pack(pady=20)

        app.mainloop()



    
main()