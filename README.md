# twitter-profile-monitoring-bot
Checks if the monitored account changes the name, screen name, description, profile or banner and then tweets the changes. If the account gets suspended it would also tweet that.

You need a [Twitter developer account](https://developer.twitter.com) and a free account at [pythonanywhere.com](https://www.pythonanywhere.com).

With the free [pythonanywhere](https://www.pythonanywhere.com) account the bot must run in a while loop,
because you have only 1 scheduled tasks and no always-on tasks.
You need to check every once in a while if the bot is running,
because the consoles will be resetting every 1-3 days. It is not the best option, but for for testing purposes it is ok.
> Maybe you edit the bot.py to run as a cron and get a paid [pythonanywhere](https://www.pythonanywhere.com) account, or run the bot on a Raspberry Pi (also as a cron).

# Installation
In your [pythonanywhere](https://www.pythonanywhere.com) account go to consoles and start a bash console.
### Install From Source
```
git clone https://github.com/h0fnar/twitter-profile-monitoring-bot
```
### Install Dependencies
```
cd twitter-profile-monitoring-bot
pip3 install -r requirements.txt
```
# Configuration
### Rename  *.env.example*
> Rename the *.env.example* file to *.env*
```
mv .env.example .env
```
### Edit the environment variables
> Edit the *.env* file with the nano editor, or go to files, twitter-profile-monitoring-bot and edit the *.env* file
```
nano .env
```
Insert your Twitter developer account credentials
```
CONSUMER_KEY="your_consumer_key"
CONSUMER_SECRET="your_consumer_secret"
ACCESS_TOKEN="your_access_token"
ACCESS_TOKEN_SECRET="your_access_token_secret"
```
Insert the user ID of the account you want to monitor
> Get the id from [tweeterid.com](https://tweeterid.com)
```
USER_ID="1234567890"
```
Add hashtag(s) to the tweets
```
HASHTAG="#whois"
```
Check every x minutes
> With a [pythonanywhere](https://www.pythonanywhere.com) free account you have 100 seconds of cpu time for 24 hours.
At 10 minutes setting, the bot will use 4-6% cpu time for 24 hours.
```
MINUTES=15
```
Send tweets to the Twitter API
> False for testing, True to tweet
```
UPDATE_API=False
```
Press Control-X, Y, Return. To save your changes and exit the nano editor.
### Time zone
> The [pythonanywhere](https://www.pythonanywhere.com) server has a different time zone than mine, so i added 2 hours. Edit line 50 in bot.py to your needs.
# Start the bot
```
python3 bot.py

python3 twitter-profile-monitoring-bot/bot.py  # on a new console from home directory
```
Stop the bot with Control-C


