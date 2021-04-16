import praw
import smtplib
from datetime import datetime, date
from config import REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, USER_AGENT
from config import EMAIL, PASSWORD, MAIL_TO
from config import KEYSEARCH

# Globals
reddit = praw.Reddit(client_id = REDDIT_CLIENT_ID, client_secret = REDDIT_CLIENT_SECRET, user_agent = USER_AGENT)

def process_text(text):
    """
    Strips irritants from the given text, lowercases it and returns.

    :param text: text to be processed
    :return: irritant-stripped, lower-cased text
    """
    strip_characters = [
        '.', ',', '?', '&', '"', "'", '!', ')', '(', '[', ']', '{', '}', ';', ':'
    ]
    for character in strip_characters:
        text = text.replace(character, '')
    return text.lower()

def get_min_date():
    """
    Returns today's date with time set to 12 AM.

    :return: datetime object with today's date and time set to 00:00:00:00
    """
    date = datetime.now()
    return datetime(date.year, date.month, date.day - 1, date.hour, date.minute, date.second)

def get_titles(targets, min_date):
    """
    Retrieves the 1000 most recent posts from each subreddit. 
    If the post is from today, check if there is any keyword match. 
    If there is a match, add it to a list of matches for that subreddit. 
    Once this is done for each subreddit, return a dictionary of the format:
    {
        'subreddit': ['list of matching posts']    
    }
    where each post in the list is a dictionary of the format:
    {
        'title': title,
        'score': score,
        'comments': number_of_comments,
        'date': date_posted,
        'url': url
    }

    :param targets: Dictionary containing subreddits and subreddit-specific keywords to look for.
    :param min_date: Today's date with time set to 00:00:00:00
    :return: A dictionary containing a dictionary for each subreddit with matched posts. See format above.
    """
    result = dict()
    for subreddit in targets:
        result[subreddit] = []
        for submission in reddit.subreddit(subreddit).new(limit=1000):
            date = datetime.fromtimestamp(submission.created_utc)
            if date >= min_date:
                submission_title = process_text(submission.title)
                for keyword in targets[subreddit]:
                    if keyword in submission_title:
                        item = {
                            'title': submission.title,
                            'score': submission.score,
                            'comments': len(submission.comments),
                            'date': date,
                            'url': submission.shortlink
                        }
                        result[subreddit].append(item)
                        break
    return result

def make_message(result):
    """
    Makes a neat list of each line in the mail to be sent.
    :param result: the results of our reddit search
    :return: A string containing the full message to be mailed.
    """
    message = [
        'Subject: Reddit Daily Digest',
        'Hello there,',
        f'This is your reddit daily digest for {date.today()}.',
    ]
    for subreddit in result:
        message.append(f'----------{subreddit}----------')
        for item in result[subreddit]:
            message.append(item['title'])
            message.append(f'Score: {item["score"]}')
            message.append(f'Comments: {item["comments"]}')
            message.append(f'Date: {item["date"]}')
            message.append(f'URL: {item["url"]}')
            message.append('\n')
    return ('\n'.join(message)).encode('ascii', 'replace')

def send_mail(message):
    """
    Uses the Python SMTPLib to send a mail.
    :param message: Message to be sent.
    """
    try:
        smtpObj = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        smtpObj.login(EMAIL, PASSWORD)
        smtpObj.sendmail(EMAIL, MAIL_TO, message)
        smtpObj.quit()
    except Exception as e:
        now = datetime.datetime.now()
        date = now.strftime('\n%d-%m-%Y %H:%M:%S')
        with open(r'.\errorlog.txt', 'a', encoding='utf-8') as errorLog:
            errorLog.write(date)
            errorLog.write('\nCould not send mail to one or more recepients!')
            errorLog.write(e)

if __name__ == '__main__':
    targets = dict()
    for subreddit in KEYSEARCH:
        targets[subreddit] = [
            process_text(keyword) for keyword in KEYSEARCH[subreddit]
        ]
    min_date = get_min_date()
    result = get_titles(targets, min_date)
    message = make_message(result)
    send_mail(message)
