#!/usr/bin/python3

import tweepy
import requests
import time
import os
import sys
import json
from dotenv import load_dotenv

os.chdir(sys.path[0])

info = '''\
----------------------------------
  ╔╦╗┬ ┬┬┌┬┐┌┬┐┌─┐┬─┐  ╔╗ ┌─┐┌┬┐
   ║ ││││ │  │ ├┤ ├┬┘  ╠╩╗│ │ │ 
   ╩ └┴┘┴ ┴  ┴ └─┘┴└─  ╚═╝└─┘ ┴ 
       Profile Monitoring
     Version 1.0 ©h0fnar2022
----------------------------------\
'''

# take environment variables from .env.
load_dotenv()

# Your Twitter developer account credentials
consumer_key = os.getenv("CONSUMER_KEY")
consumer_secret = os.getenv("CONSUMER_SECRET")
access_token = os.getenv("ACCESS_TOKEN")
access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")

# User ID of the account you want to monitor
user_id = os.getenv("USER_ID")

# Add hashtag(s) to the tweets
hashtag = os.getenv("HASHTAG")

# Check every x minutes
minutes = os.getenv("MINUTES")
minutes = int(minutes)

# Send tweets to the Twitter API (False for testing, True to tweet)
update_api = os.getenv("UPDATE_API", 'False').lower() in ('true', '1', 't')

##########################################################################################


def local_time():
    local = time.time()
    t = local + 7200  # add 2 hours (if pythonanywhere server has different time)
    t = time.ctime(t)
    return t


# check if 'data.json' exits, if not, create it
path = 'data.json'
isExist = os.path.exists(path)
if not isExist:

    data_start = {
        "name": '',
        "screen_name": '',
        "description": '',
        "banner": '',
        "profile": ''
    }

    # JSON save:
    with open('data.json', 'w') as fp:
        json.dump(data_start, fp, sort_keys=False, indent=4)

print(info)
count = 0
print_user_info = True
run_bot = True

# authorization of consumer key and consumer secret
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
# set access to user's access key and access secret
auth.set_access_token(access_token, access_token_secret)
# calling the api
api = tweepy.API(auth)

while run_bot:
    try:
        # fetching the user
        user = api.get_user(user_id=user_id)

        # fetching the screen name
        screen_name = user.screen_name

        # print once
        if print_user_info:
            print('  Monitoring: ' + '@' + str(screen_name))
            print('----------------------------------')
            print_user_info = False

        # fetching the stuff
        name_new = user.name
        screen_name_new = user.screen_name
        description_new = user.description
        banner_new = user.profile_banner_url
        profile_new = user.profile_image_url

        ##################################################################################

        name_changed = False
        screen_name_changed = False
        description_changed = False
        banner_changed = False
        profile_changed = False

        # JSON load:
        with open('data.json', 'r') as fp:
            data = json.load(fp)

        # check name
        name_old = data['name']
        if name_new != name_old:
            name_changed = True
            data['name'] = name_new

        # check screen_name
        screen_name_old = data['screen_name']
        if screen_name_new != screen_name_old:
            screen_name_changed = True
            data['screen_name'] = screen_name_new

        # check description
        description_old = data['description']
        if description_new != description_old:
            description_changed = True
            data['description'] = description_new

        # check banner
        banner_old = data['banner']
        if banner_new != banner_old:
            banner_changed = True
            data['banner'] = banner_new

        # check profile
        profile_old = data['profile']
        if profile_new != profile_old:
            profile_changed = True
            data['profile'] = profile_new

        # JSON save:
        with open('data.json', 'w') as fp:
            json.dump(data, fp, sort_keys=False, indent=4)

        ##################################################################################

        # make tweet
        make_tweet = False

        # name
        if name_changed:
            make_tweet = True

        # screen name
        if screen_name_changed:
            make_tweet = True

        # description
        if description_changed:
            make_tweet = True

        # post the Tweet
        if make_tweet:
            tweet = hashtag
            tweet = tweet + '\n'
            tweet = tweet + name_new
            tweet = tweet + '\n'
            tweet = tweet + '@ ' + screen_name_new
            tweet = tweet + '\n'
            tweet = tweet + description_new
            status = api.update_status(status=tweet) if update_api else 0
            print("Tweet:\n" + str(tweet))

        # post new Banner
        if banner_changed:
            # download banner
            URL = banner_new
            image = requests.get(URL).content
            f = open('img/banner_temp.jpg', 'wb')
            f.write(image)
            f.close()
            # tweet banner img
            filename = 'img/banner_temp.jpg'
            media = api.media_upload(filename) if update_api else 0
            tweet = "New Banner! " + hashtag
            post_result = api.update_status(status=tweet, media_ids=[media.media_id]) if update_api else 0
            print("Banner changed!")

        # post new Profile
        if profile_changed:
            # download profile
            profile_new = profile_new.replace('_normal.jpg', '.jpg')
            URL = profile_new
            image = requests.get(URL).content
            f = open('img/profile_temp.jpg', 'wb')
            f.write(image)
            f.close()
            # tweet profile img
            filename = 'img/profile_temp.jpg'
            media = api.media_upload(filename) if update_api else 0
            tweet = "New Profile! " + hashtag
            post_result = api.update_status(status=tweet, media_ids=[media.media_id]) if update_api else 0
            print("Profile changed!")

        count += 1

        my_time = local_time()
        print(str(count) + "  " + my_time)

        time.sleep(minutes * 60)  # seconds * 60

##########################################################################################

    except tweepy.errors.HTTPException as e:

        my_time = local_time()

        # get the error code (63 is suspended account)
        code = e.api_errors[0]['code']

        # make tweet if account is suspended
        if code == 63:

            # JSON load:
            with open('data.json', 'r') as fp:
                data = json.load(fp)

            name_old = data['name']
            screen_name_old = data['screen_name']

            # post the Tweet
            tweet = hashtag
            tweet = tweet + '\n'
            tweet = tweet + name_old
            tweet = tweet + '\n'
            tweet = tweet + '@ ' + screen_name_old
            tweet = tweet + '\n'
            tweet = tweet + "Account is suspended!!!"
            # tweet 404 img
            filename = "img/404.jpg"
            media = api.media_upload(filename) if update_api else 0
            post_result = api.update_status(status=tweet, media_ids=[media.media_id]) if update_api else 0
            print("Tweet:\n" + str(tweet))
            print("Bot stopped!!!")
            count += 1
            print(str(count) + "  " + my_time)
            run_bot = False
            
        else:
            print("Tweepy Error!!!")
            print(e)
            count += 1
            print(str(count) + "  " + my_time)
            time.sleep(15)

    except KeyboardInterrupt:
        print(' Interrupted!!!')
        run_bot = False

