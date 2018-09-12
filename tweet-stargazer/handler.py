import tweepy
import os
import requests
import json
import base64

def handle(st):
    req = json.loads(st)

    auth = tweepy.OAuthHandler(os.environ["consumer_key"], os.environ["consumer_secret"])
    auth.set_access_token(os.environ["access_token"], os.environ["access_token_secret"])

    api = tweepy.API(auth)

    # Figure out the correct extension for the avatar.
    ext = ".jpg"
    if req["contentType"] == "image/png":
        ext = ".png"
    file_name = req["login"] + ext

    # Take the encoded image and turn into binary bytes
    image_data = base64.standard_b64decode(req["image"])

    f = open("/tmp/"+file_name, 'wb')
    f.write(image_data)
    f.close()

    api.update_with_media("/tmp/"+file_name, req["login"] + " is a star-gazer for " + req["repository"])

    # Log the results
    print("Tweet sent")

    os.remove("/tmp/"+file_name)
