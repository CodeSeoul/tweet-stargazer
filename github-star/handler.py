import requests
import json

def handle(st):
    # parse Github event
    req = json.loads(st)

    if req["action"] != "started":
        print("not a 'stared' event")
        return

    loginName = req["sender"]["login"]

    # Get avatar url
    avatar_req = {}
    avatar_req["avatar_url"] = req["sender"]["avatar_url"]

    # download the avatar binary using getavatar function
    r = requests.post("http://gateway:8080/function/get-avatar", json=avatar_req)

    res = r.json()

    # Figure out the correct extension for the avatar.
    ext = ".jpg"
    if res["contentType"] == "image/png":
        ext = ".png"

    gazer = {}
    gazer["login"] = loginName
    gazer["filename"] = loginName + ext
    gazer["image"] = res["content"]

    r2 = requests.post("http://gateway:8080/function/tweet-stargazer", json=gazer)

    club_res = {}
    club_res["tweet_result"] = r2.text
    club_res["status"] = "success"
    club_res["username"] = req["sender"]["login"]

    # Useful for logging, GitHub's invoker will receive this string
    print(json.dumps(club_res))
