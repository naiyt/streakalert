import urllib2
import re
import config
import smtplib
from email.mime.text import MIMEText
from email.parser import Parser
from sys import argv
from bs4 import BeautifulSoup

'''
And now for something utterly pointless! Just a tiny script that you can set a daily cron job
on to remind you to commit something to GitHub by the end of the day so you don't
lose your current streak. Takes in your GitHub username as an argument.

Set the email it should come from and the email it should go to in "config.py".

Set the minimum number of current streaks you must be above before it starts emailing
in config.py as well.

'''

def determine_streak(username):
    '''Scrapes your current streak from GitHub; there wasn't an API call that I could find for this'''
    url = "https://github.com/{}".format(username)
    soup = BeautifulSoup(urllib2.urlopen(url))
    streak_div = soup.findAll('div', {'class':  'col contrib-streak-current'})[0]
    num = streak_div.findAll('span', {'class': 'num'})[0].text
    num = re.match(r'([0-9]+)', num)
    if num:
        return num.group(1)


def alert(streak):
    '''Sends you the email, if you're above the threshold and haven't committed today'''
    if config.min_streak_alerts <= streak:
        body = """
        Just a friendly reminder to commit something, so you don't lose your {} day streak on Github.
        """.format(streak)
        msg = MIMEText(body)
        msg['From'] = config.from_email
        msg['To'] = config.to_email
        msg['Subject'] = "Don't lose your {} day streak on GitHub!".format(streak)

        s = smtplib.SMTP('localhost')
        s.sendmail(config.from_email, [config.to_email], msg.as_string())
        s.quit()

def contributed_today(user):
    '''Determines if you've already contributed something today'''
    url = "https://github.com/users/{}/contributions_calendar_data".format(user)
    contributions = urllib2.urlopen(url).read()
    contributions = contributions[1:-2]
    todays_contributions = int(contributions.split(',')[-1])
    if todays_contributions > 0:
       return True
    else:
       return False


if __name__ == '__main__':
    if len(argv) < 2:
        print "Usage: streaks.py <github username>"
        exit()
    user = argv[1]
    if contributed_today(user) is False:
        curr_streak = determine_streak(user)
        alert(curr_streak)
