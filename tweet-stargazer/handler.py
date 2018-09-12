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

    image = req["image"]
    file_name = req["filename"]
    login = req["login"]
    print(login, file_name)

    # Take the encoded image and turn into binary bytes
    image_data = base64.standard_b64decode(image)

    polaroid_r = requests.post("http://gateway:8080/function/polaroid", data=image_data)

    f = open("/tmp/"+file_name, 'wb')
    f.write(polaroid_r.content)
    f.close()

    api.update_with_media("/tmp/"+file_name, login + " is a star-gazer for " + os.environ["project"])

    # Log the results
    print("Tweet sent")

    os.remove("/tmp/"+file_name)
