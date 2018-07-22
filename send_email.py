""" Runs separately from the rest of the program. Updates next episode info and sends email reminders the day before and day of airing.
    Run daily with cron or equivalent """

import dbActions
import webScraper
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime
import xml.etree.ElementTree as xml


# run with arguments email, password, send to email
def send_mail(show, message):
    """ takes message and sends reminder email. login details are in credentials.xml """
    tree = xml.parse('credentials.xml')
    root = tree.getroot()
    email = root.find('email').text
    password = root.find('password').text
    emailto = root.find('emailto').text
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(email, password)
    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = emailto
    msg['Subject'] = 'Reminder to watch ' + show
    msg.attach(MIMEText(message, 'plain'))
    server.sendmail(email, emailto, msg.as_string())


def new_episode_check():
    """ gets the next airdate of each show and triggers an email reminder if it is airing today or tomorrow """
    for show in shows:
        if show.next_air_date != 'TBD':
            air_date = datetime.datetime.strptime(show.next_air_date, "%Y-%m-%d")
            today = datetime.datetime.today()
            tomorrow = today + datetime.timedelta(days=1)
            if air_date.date() == today.date():
                message = show.title + ' will be airing tonight at ' + show.time + ' on ' + show.network
                send_mail(show.title, message)
            elif air_date.date() == tomorrow.date():
                message = show.title + ' will be airing tomorrow at ' + show.time + ' on ' + show.network
                send_mail(show.title, message)


""" logs into theTVDB API, updates shows, and calls method to check if email should be sent """
token = 'Bearer ' + webScraper.login()
shows = dbActions.get_shows()
for s in shows:
    tmp = webScraper.get_episodes(token, s.show_id)
    s.update(tmp['current_season'], tmp['next_ep_no'], tmp['next_air_date'])
new_episode_check()
