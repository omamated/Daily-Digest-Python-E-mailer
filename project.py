#the libraries I need
from bs4 import BeautifulSoup #use this to scrape news https://www.geeksforgeeks.org/python/implementing-web-scraping-python-beautiful-soup/
import requests # also need this to scrape news
import time
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
def save_credentials(user,password,choice):
    env_path=".env"
    set_key(env_path, "EMAIL_USERNAME", user)
    set_key(env_path, "EMAIL_PASSWORD", password)
    set_key(env_path, "NEWS_CHOICE", choice)

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

        choice_box = customtkinter.CTkOptionMenu(app, values=["Hacker News", "Google News", "CNN News"])

        choice_box.pack(pady=20)

        def save_creds():
            user_email=email.get()
            user_password=password.get()
            news_choice = choice_box.get()
            save_credentials(user_email,user_password,news_choice)
            print("Saving")
            app.destroy()
            #gui("dashboard")
        button = customtkinter.CTkButton(app,text='Save Credentials',command=save_creds)
        button.pack(pady=20)

        app.mainloop()
    if s == "dashboard":
        print("hi")
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
    if news_choice == "CNN News":
        session = requests.Session()

        # rinse and repeat as hacker news but adjust elements for CNN news
        url = "https://rss.cnn.com/rss/cnn_topstories.rss" #url of website
        headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive"
        }
        time.sleep(2)
        response = session.get(url, headers=headers, timeout=10)
        print(response.status_code)
        soup = BeautifulSoup(response.text, "xml") 
        for item in soup.find_all("item"):
            headline = item.title.get_text()
            link = item.link.get_text()
            news_items.append((headline, link))
        return news_items[:10] 
    else:
        raise ValueError("No news selected?") # this should be impossible as it's a dropdown but will leave just in case
    return news_items
def send_email():
    load_dotenv()   
    news_choice=os.getenv("NEWS_CHOICE")
    news=scrape_news(news_choice)


    
main()
news_items=scrape_news("Hacker News")
print(news_items)