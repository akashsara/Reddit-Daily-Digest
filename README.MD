# Reddit Daily Digest

---

## What is it?

## Installation

1. Download & install [Python3](https://www.python.org/downloads/).
2. Clone or download this repository.
3. Navigate to this repository and run `pip install -r requirements.txt`
4. Get yourself a Reddit client ID and client secret. [Refer this.](https://github.com/reddit-archive/reddit/wiki/oauth2-quick-start-example)
5. Get yourself a Gmail app-specific password. [Refer this.](https://support.google.com/accounts/answer/185833?hl=en). If you don't use Gmail, you'll have to modify the code to use your mail server. Or just create a temporary account or something.
6. Modify `sample_config.py` to use the stuff you got above. Also include the subreddits to search and the keywords you want to use. And of course enter the mail ID to send mails to.
7. Rename `sample_config.py` to `config.py`.
8. Run the script: `python3 bot.py`
9. Enjoy your daily digest!

## Running it Everyday

So obviously this makes sense only if you run it every day (Or you could always adapt the code for your own nefarious purposes). So how do you do that? Well you have a couple of options. The first is to set up a cron job (UNIX) or schedule a task (Windows) (Sorry Mac users, I dunno what the equivalent for you is). Or you can schedule it to run on a server everyday. Personally, I've scheduled it on [PythonAnywhere](http://pythonanywhere.com/). The free versions allows for exactly one such script to be scheduled. 

## Can I use this in my own scripts/packages/software?

Yup. Feel free to do anything with this script. Be sure to credit me/this repo though. And if you make something cool, do share it. :)

## What does it actually do?

1. Retrieves the 1000 (API limitation) most recent posts from a subreddit.
2. Iterates through each post.
	2.1. Checks if the post is from today. (00:00:00:00 to now)
	2.2. Checks if any keywords are in the post's title.
	2.3. If both conditions are met, saves the post information.
3. Makes a nicely formatted message to mail.
4. Sends the mail.

## Okay, but why? 

Laziness. There's a couple of subreddits that I follow only for posts related to certain topics but too lazy to look through them everyday. So might as well get a daily digest no? 