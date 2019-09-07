from datetime import datetime

def BMS():
    screenToFind = ["PVR Forum Sujana Mall: Kukatpally, Hyderabad", "Cinepolis: Manjeera Mall, Kukatpally", "Devi 70MM: RTC X Roads",
                    "PVR: Inorbit, Cyberabad", "Shanti 70MM: Narayanguda", "Viswanath 70MM Theater: Kukatpally"] #select theater list
    toEmailList = ["mailid1", "mailid2", "mailid3"]  # Can be multiple email ids ["email1","email2","email3"]
    fromEmail = "your mail id"
    passwordOfFromEmail = "your mail password"


    def notifyUser():
        # openUrl()
        Found_Screens_String = "Theatres Found : "
        for i in range(0,len(Found_Screens)):
            Found_Screens_String += ", " +str(Found_Screens[i])
        sendEmail(fromEmail, passwordOfFromEmail, toEmailList, Found_Screens_String + ' Found!!', "Jaldi Book Karo")


    def openUrl():
        import webbrowser
        webbrowser.open(url)


    def sendEmail(user, pwd, recipient, subject, body):
        import smtplib
        FROM = user
        TO = recipient if type(recipient) is list else [recipient]
        SUBJECT = subject
        TEXT = body

        # Prepare actual message
        message = """From: %s\nTo: %s\nSubject: %s\n\n%s
        """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.ehlo()
            server.starttls()
            server.login(user, pwd)
            server.sendmail(FROM, TO, message)
            server.close()
            print('successfully sent the mail')
        except Exception as x:
            print("failed to send mail")
            print(x)


    # print("BMS Scrape started at " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    import requests

    url = "https://in.bookmyshow.com/buytickets/saaho-hyderabad/movie-hyd-ET00056595-MT/20190830/"
    request = requests.get(url)
    htmlContent = request.text

    from bs4 import BeautifulSoup

    soup = BeautifulSoup(htmlContent, "html.parser")
    venueList = soup.find('ul', {'id': 'venuelist'})
    found = False
    availableList = ""
    Found_Screens = []
    for link in venueList.find_all('li'):
        screenName = link.get('data-name')
        for i in range(0,len(screenToFind)):
            screenToFindLower = screenToFind[i].lower()
            if (screenName.lower().find(screenToFindLower) > -1):
                Found_Screens.append(screenToFindLower)
                found = True
                # break

    if (found == False):
        print('Not found')
    else:
        print(Found_Screens)
        notifyUser()
        print("Found")


Tmrw = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
# Now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
for i in range(0,9,2):
    BMS()