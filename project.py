
#the libraries I need
from bs4 import BeautifulSoup #use this to scrape news https://www.geeksforgeeks.org/python/implementing-web-scraping-python-beautiful-soup/
import requests # also need this to scrape news
import time
from datetime import datetime, date
import feedparser # to parse rss feeds
import webbrowser # open links
import customtkinter # for the gui; normal tkinter isn't too clean and i want to make my gui look clean 
from dotenv import load_dotenv, set_key, find_dotenv #use this for saving the passwords in .env
import schedule # use this to auto run and send email everyday-morning
import os # to check if its the users first time on the software with .env checking
import smtplib #send emails using gmail
from email.message import  EmailMessage #for email messages
def main():
    if os.path.isfile(".env"):
        gui("dashboard")
    else:
        gui("setup")
    schedule.every().day.at("08:00").do(send_email)
def open_link(url):
    webbrowser.open_new_tab(url)
def save_credentials(user,password,choice):
    env_path=".env"
    set_key(env_path, "EMAIL_USERNAME", user)
    set_key(env_path, "EMAIL_PASSWORD", password)
    set_key(env_path, "NEWS_CHOICE", choice)
def gui(s):
    #making the gui 
    app = customtkinter.CTk()
    app.title("Daily Digest News Email Sender")
    app.geometry("800x800")
    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("dark-blue")
    if s == "setup": #if this is there first time ask for email + pass
        label=customtkinter.CTkLabel(app,text="Enter your Gmail credentials \n These wil be saved in a .env file locally \n for your password use and app password from google \n retrieve the app password here:")

        label.pack(pady=20)#this like gives it breathing room
        label_url=customtkinter.CTkLabel(app, text="https://support.google.com/accounts/answer/185833?hl=en", text_color="#4fa5e2")
        label_url.pack(pady=10)
        label_url.bind("<Button-1>",lambda e: open_link("https://support.google.com/accounts/answer/185833?hl=en")
)
        email=customtkinter.CTkEntry(app, placeholder_text="Email")
        email.pack(pady=20)

        password=customtkinter.CTkEntry(app, placeholder_text="Password")
        password.pack(pady=20)

        choice_box = customtkinter.CTkOptionMenu(app, values=["Hacker News", "Google News", "AP News"])

        choice_box.pack(pady=20)

        def save_creds():
            user_email=email.get()
            user_password=password.get()
            news_choice = choice_box.get()
            save_credentials(user_email,user_password,news_choice)
            print("Saving")
            app.destroy()
            gui("dashboard")
        button = customtkinter.CTkButton(app,text='Save Credentials',command=save_creds)
        button.pack(pady=20)

        app.mainloop()
    if s == "dashboard":
        load_dotenv()
        news_content=scrape_news(os.getenv("NEWS_CHOICE"))
        news_text = "\n\n".join([f"{i+1}. {title}\n{link}" for i, (title, link) in enumerate(news_content)])
        text_box = customtkinter.CTkTextbox(app, width=450, height=450, wrap="word")
        text_box.pack(pady=20, padx=20)
        text_box.insert("0.0", news_text)
        text_box.configure(state="disabled")

        def send_email_and_update_status():
            label_status.configure(text="Sending email...")
            app.update_idletasks()

            result = send_email() 
            label_status.configure(text=result, wraplength=400)

        send_email_button = customtkinter.CTkButton(app,text="Send Email Now",command=send_email_and_update_status)
        send_email_button.pack(pady=20)
        label_status = customtkinter.CTkLabel(app, text="")
        label_status.pack(pady=10)
        reset_creds_button = customtkinter.CTkButton(app, text="Reset Credentials", command=lambda: [os.remove(".env"), app.destroy(), gui("setup")])
        reset_creds_button.pack(pady=20)
        app.mainloop()
def scrape_news(news_choice):
    news_items=[]
    if news_choice == "Hacker News":
        url = "https://news.ycombinator.com/" #url of website
        response = requests.get(url) #get the og http request
        soup = BeautifulSoup(response.text, "html.parser") 
        for thing in soup.select("span.titleline > a"): # we use this tag as thats what hackernews tags headlines with (in HTML)
            headline= thing.get_text()
            link = thing['href'] # all links in html start with href
            news_items.append((headline, link))
        return news_items[:10] # this only takes the top 10
    if news_choice == "Google News":
        # rinse and repeat as hacker news but adjust elements for google news
        url = "https://news.google.com/rss" #url of website
        response = requests.get(url) #get the og http request
        soup = BeautifulSoup(response.text, "xml") 
        for item in soup.find_all("item"):
            headline = item.title.get_text()
            link = item.link.get_text()
            news_items.append((headline, link))
        return news_items[:10] 
    if news_choice == "AP News":
            url = "https://feedx.net/rss/ap.xml"
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
            response = requests.get(url, headers=headers, timeout=10)
            
            feed = feedparser.parse(response.content)
            
            news_items = []
            for entry in feed.entries[:10]:
                headline = entry.title
                link = entry.link
                news_items.append((headline, link))
            
            return news_items


    else:
        raise ValueError("No news selected?") # this should be impossible as it's a dropdown but will leave just in case
    return news_items
def send_email():
    load_dotenv()   
    news_choice=os.getenv("NEWS_CHOICE")
    news=scrape_news(news_choice)
    smtp_server="smtp.gmail.com"
    smtp_port=587
    email_user=os.getenv("EMAIL_USERNAME")
    email_password=os.getenv("EMAIL_PASSWORD")
    msg=EmailMessage()
    msg['subject']=f"Your daily news digest"
    msg['from']=email_user
    msg['to']=email_user
    news_content="\n\n".join([f"{i+1}. {title}\n{link}" for i, (title, link) in enumerate(news)])
    msg.set_content(f"Here is your daily news digest from {news_choice}:\n\n{news_content}")
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(email_user, email_password)
            server.send_message(msg)
            return("Email sent successfully.")
    except smtplib.SMTPException as e:
        return(f"Failed to send email: {e}")
    except Exception as e:
        return(f"An error occurred: {e}")

if __name__== "__main__":
    main() 