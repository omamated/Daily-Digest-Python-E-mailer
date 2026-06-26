Hello, this is my CS50 Python Final Project.

# Daily Digest Emailer
My Final CS50 Python Project is called Daily Digest Emailer, a python news digest app. It allows users to choose a news source, see headlines, and email news to themself in a single button press. The program stores user data locally and securely in a ".env" file. I built this project because my dad was always rushing around, so by the time he got home and talked to me he wouldn't know any of the news I was talking about, so I eventually created this. It allows users to view headlines offline and all within their email. If the user doesn't find today's news interesting or doesn't care to view it, they can simply not press the send email button.

### Overview
On the first startup, the program will run a setup page that will ask your email and password. Using your email password would not be very safe so you can create an app password as explained on instruction shown during setup. Your news choice will be chosen during this setup phase. Your email, app password, and news choice will all be saved in a .env file. Your news choices are Hacker news, Google news, and AP news. 
<img width="804" height="825" alt="image" src="https://github.com/user-attachments/assets/add74d6f-571b-425e-8f99-c157c09d7c19" />
The dashboard provides you with a preview of today's news and what will be emailed to you cleanly displayed with just the headline and link. The Send Email Now button will send an email to yourself containing today's news headlines. The email contains clickable links, so you can click on them while on the go to read more. The dashboard also contains a reset credentials screen where your .env will be deleted and you can re-enter yor email, app password, and news choice.
<img width="798" height="822" alt="image" src="https://github.com/user-attachments/assets/2e1c2946-ccad-41f0-b4b8-440dcf046b57" />
<img width="1116" height="654" alt="image" src="https://github.com/user-attachments/assets/4966dfee-0ff6-4f6e-bc17-32a6726b5cba" />

### How it works
The main() function in the python script will check to see if an .env exists. This determines whether the user needs the startup page or dashboard page. Custom Tkinter will open the page that is needed and will save all inputs that are given. Based on the choices on startup, the scraping function will return the news from various RSS feeds. FeedParser is used here to download and parse feeds like RSS, Atom, or RDF. BeautifulSoup helps clean the results as it makes a nested tree from raw HTML/XML. The results from the scraping will be saved in a cleaned list to easily display on the Custom Tkinter Dashboard. The Send Email Now button will call a send email function that will send yourself an email using your app password through SMTP servers.

### What Files Do
test_project.py - If you need to check if news sources are being scraped properly you can simply run pytest test_project.py
project.py - The actual daily-digest emailer, run through Command Line Interface by running "python project.py" or however you prefer to run python. (Make sure python is installed obviously)
.env- Stores your credentials securely.

### Design Choices
I chose to use Custom Tkinter as normal tkinter looked very old and not as modern to me. CustomTkinter fufilled me with that modern feel.
I used RSS Feeds and scraping in this project because RSS feeds were simpler for some news sources, but for some I had to scrape.
I decided to do an emailer instead of an texter because my dad, whom I had in mind when designing usually lives in his emails more than his texts.

### Challenges
Some Challenges I faced:
Custom Tkinter wouldn't work in Github Codespaces, I talked with some people on discord and they assured me it would be fine as long as it fufills the requirements. 
Emailing wouldn't authenticate, I tried to make it so you put your email password, but this caoused authentication problems and was very unsecure, so I went to app passwords instead.

### How to Use It
To run the Daily Digest Emailer, do the following.
1. Install the Requirements
pip install -r requirements.txt
2. Run the project
python project.py
3. Setup Email App passwords
Follow the instructions on the setup page to complete this. It will tell you to go here: [Google App Password Support]([url](https://support.google.com/accounts/answer/185833?hl=en)) which will guide you to create an app password, which you will paste in the password field.
